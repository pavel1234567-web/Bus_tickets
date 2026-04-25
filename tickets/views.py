"""
Views for bus tickets application.

This module contains all the views for the bus ticketing system:
- Home page with route search
- Route search results
- Seat selection and booking
- Payment processing
- Ticket management
- PDF generation
"""

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse, HttpResponse, StreamingHttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods, require_POST
from django.utils import timezone
from django.urls import reverse_lazy, reverse
from django.template.loader import render_to_string
from django.conf import settings
from django.db import transaction
from django.core.cache import cache
from rest_framework import viewsets, status
import json
import os
import time
import uuid
from datetime import datetime, timedelta
from .models import Route, Schedule, Ticket, Booking, Payment, PassengerInfo
from .forms import SearchForm, BookingForm

# Template filter for adding days to date
def add_days(value, days):
    """Add days to a date"""
    if isinstance(value, str):
        try:
            value = datetime.strptime(value, '%Y-%m-%d').date()
        except:
            return value
    return value + timedelta(days=days)
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated, AllowAny
from rest_framework.response import Response
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from io import BytesIO
import json
import uuid

from .models import Route, Bus, Schedule, Ticket, Booking, Payment
from .forms import BookingForm, SearchForm
from django.core import serializers
from django.views.decorators.http import require_http_methods


def home(request):
    """
    Home page with route search functionality.
    """
    form = SearchForm()
    
    # Get popular routes for display
    popular_routes = Route.objects.filter(is_active=True).order_by('departure_city', 'arrival_city')[:6]
    
    # Get all cities for quick search
    departure_cities = Route.objects.filter(is_active=True).values_list('departure_city', flat=True).distinct()
    arrival_cities = Route.objects.filter(is_active=True).values_list('arrival_city', flat=True).distinct()
    all_cities = sorted(list(set(departure_cities) | set(arrival_cities)))
    
    # Fallback cities if database is empty
    if not all_cities:
        all_cities = [
            'Moscow', 'St. Petersburg', 'Kazan', 'Nizhny Novgorod',
            'Samara', 'Yekaterinburg', 'Sochi', 'Rostov-on-Don'
        ]
    
    # Get all routes data for quick search
    routes_data = []
    for route in Route.objects.filter(is_active=True):
        routes_data.append({
            'departure_city': route.departure_city,
            'arrival_city': route.arrival_city,
            'distance': str(route.distance),
            'estimated_time': str(route.estimated_time),
            'base_price': str(route.base_price)
        })
    
    # Fallback routes if database is empty
    if not routes_data:
        routes_data = [
            {'departure_city': 'Moscow', 'arrival_city': 'St. Petersburg', 'distance': '700', 'estimated_time': '8 hours', 'base_price': '2500.00'},
            {'departure_city': 'Moscow', 'arrival_city': 'Kazan', 'distance': '800', 'estimated_time': '12 hours', 'base_price': '1800.00'},
            {'departure_city': 'St. Petersburg', 'arrival_city': 'Moscow', 'distance': '700', 'estimated_time': '8 hours', 'base_price': '2500.00'},
            {'departure_city': 'Kazan', 'arrival_city': 'Moscow', 'distance': '800', 'estimated_time': '12 hours', 'base_price': '1800.00'}
        ]
    
    context = {
        'form': form,
        'popular_routes': popular_routes,
        'cities': all_cities
    }
    return render(request, 'tickets/home_simple.html', context)


def search_routes(request):
    """
    Enhanced search for bus routes with flexible filter combinations.
    """
    if request.method == 'GET':
        form = SearchForm(request.GET)
        
        if form.is_valid():
            departure_city = form.cleaned_data.get('departure_city', '').strip()
            arrival_city = form.cleaned_data.get('arrival_city', '').strip()
            departure_date = form.cleaned_data.get('departure_date')
            
            # Work directly with schedules to prevent duplication
            # Build base schedule query with city filters
            schedules_query = Schedule.objects.filter(is_active=True)
            
            # Apply city filters directly to schedules through route relationship
            if departure_city and arrival_city:
                # Both cities specified - exact route search
                schedules_query = schedules_query.filter(
                    route__departure_city__iexact=departure_city,
                    route__arrival_city__iexact=arrival_city,
                    route__is_active=True
                )
                search_type = "specific_route"
            elif departure_city:
                # Only departure city specified - all routes from this city
                schedules_query = schedules_query.filter(
                    route__departure_city__iexact=departure_city,
                    route__is_active=True
                )
                search_type = "from_city"
            elif arrival_city:
                # Only arrival city specified - all routes to this city
                schedules_query = schedules_query.filter(
                    route__arrival_city__iexact=arrival_city,
                    route__is_active=True
                )
                search_type = "to_city"
            else:
                # No cities specified - show all active schedules
                schedules_query = schedules_query.filter(route__is_active=True)
                search_type = "all_routes"
            
            # Apply date filtering if specified
            if departure_date:
                # Use timezone-aware filtering for exact date match
                from django.utils import timezone
                start_of_day = timezone.make_aware(timezone.datetime.combine(departure_date, timezone.datetime.min.time()))
                end_of_day = start_of_day + timezone.timedelta(days=1)
                
                schedules_query = schedules_query.filter(
                    departure_time__gte=start_of_day,
                    departure_time__lt=end_of_day
                )
            else:
                # If no specific date, only show future schedules (from today)
                from django.utils import timezone
                today = timezone.now().date()
                start_of_today = timezone.make_aware(timezone.datetime.combine(today, timezone.datetime.min.time()))
                
                schedules_query = schedules_query.filter(
                    departure_time__gte=start_of_today
                )
            
            # Get schedules with proper ordering and relationships
            schedules = schedules_query.select_related('route', 'bus').order_by('departure_time')
            
            # Fix any arrival_time year issues (ensure arrival_time has same year as departure_time when appropriate)
            for schedule in schedules:
                # If arrival_time year is different from departure_time year and they should be the same day
                if schedule.arrival_time.date() != schedule.departure_time.date() and schedule.arrival_time.time() > schedule.departure_time.time():
                    # This might be a same-day arrival with wrong year, fix it
                    from datetime import datetime, time
                    if schedule.arrival_time.year != schedule.departure_time.year:
                        # Create corrected arrival_time with same year as departure_time
                        corrected_arrival = datetime.combine(
                            schedule.departure_time.date(),
                            schedule.arrival_time.time()
                        )
                        # Add route duration if needed
                        if schedule.route.estimated_time:
                            corrected_arrival = schedule.departure_time + schedule.route.estimated_time
                        schedule.arrival_time = corrected_arrival
            
            # Get unique routes from schedules for alternative dates logic
            routes = Route.objects.filter(id__in=schedules.values_list('route_id', flat=True)).distinct()
            
            # Check if we have schedules for the requested date
            has_schedules_for_date = schedules.exists()
            
            # Always search for alternative dates when we have a specific date and city filters
            alternative_dates = []
            if departure_date and (departure_city or arrival_city):
                # Search for schedules on future dates only (from today to +14 days)
                from datetime import timedelta
                import datetime
                
                # ALWAYS start from today, regardless of departure_date
                today = timezone.now().date()
                start_date = today  # Always start from today
                end_date = today + datetime.timedelta(days=14)  # Search 14 days from today
                
                # DEBUG: Print date filtering info
                # print(f"DEBUG: Alternative dates search:")
                # print(f"  Today: {today}")
                # print(f"  Start date: {start_date}")
                # print(f"  End date: {end_date}")
                # print(f"  Departure date: {departure_date}")
                
                # Build alternative dates query with proper timezone handling
                from django.utils import timezone
                start_of_search_range = timezone.make_aware(timezone.datetime.combine(start_date, timezone.datetime.min.time()))
                end_of_search_range = timezone.make_aware(timezone.datetime.combine(end_date, timezone.datetime.max.time()))
                
                # Exclude the original date range as well
                original_start = timezone.make_aware(timezone.datetime.combine(departure_date, timezone.datetime.min.time()))
                original_end = original_start + timezone.timedelta(days=1)
                
                alt_schedules_query = Schedule.objects.filter(
                    route__in=routes,
                    is_active=True,
                    departure_time__gte=start_of_search_range,
                    departure_time__lte=end_of_search_range,
                ).exclude(
                    departure_time__gte=original_start,
                    departure_time__lt=original_end
                ).select_related('route', 'bus').order_by('departure_time')
                
                # DEBUG: Show actual schedules found
                # print(f"DEBUG: Found {alt_schedules_query.count()} alternative schedules:")
                # for schedule in alt_schedules_query[:5]:  # Show first 5
                #     print(f"  - {schedule.departure_time.date()} ({schedule.departure_time}) - {schedule.route.departure_city} to {schedule.route.arrival_city}")
                
                # Group alternative schedules by date with deduplication
                alt_schedules_by_date = {}
                seen_alt_schedules = set()  # Track unique alternative schedules
                
                for schedule in alt_schedules_query:
                    # Create unique identifier for schedule (route + bus + departure_time)
                    schedule_id = f"{schedule.route.id}_{schedule.bus.id}_{schedule.departure_time.isoformat()}"
                    
                    if schedule_id not in seen_alt_schedules:
                        seen_alt_schedules.add(schedule_id)
                        date_str = schedule.departure_time.date().strftime('%d.%m.%Y')
                        if date_str not in alt_schedules_by_date:
                            alt_schedules_by_date[date_str] = []
                        alt_schedules_by_date[date_str].append(schedule)
                
                # Create alternative dates info
                for date_str, date_schedules in alt_schedules_by_date.items():
                    if date_schedules:  # Only include dates with schedules
                        alternative_dates.append({
                            'date': date_str,
                            'count': len(date_schedules),
                            'first_schedule': date_schedules[0],
                            'price_range': {
                                'min': min(s.current_price for s in date_schedules),
                                'max': max(s.current_price for s in date_schedules)
                            }
                        })
                
                # Sort alternative dates by date
                alternative_dates.sort(key=lambda x: x['date'])
            
            # DEBUG: Show main schedules found
            # print(f"DEBUG: Found {schedules.count()} main schedules:")
            # for schedule in schedules[:5]:  # Show first 5
            #     print(f"  - {schedule.departure_time.date()} ({schedule.departure_time}) - {schedule.route.departure_city} to {schedule.route.arrival_city}")
            
            # Group schedules by date for better organization and deduplicate
            schedules_by_date = {}
            seen_schedules = set()  # Track unique schedules to prevent duplicates
            
            for schedule in schedules:
                # Create unique identifier for schedule (route + bus + departure_time)
                schedule_id = f"{schedule.route.id}_{schedule.bus.id}_{schedule.departure_time.isoformat()}"
                
                if schedule_id not in seen_schedules:
                    seen_schedules.add(schedule_id)
                    date_str = schedule.departure_time.date().strftime('%d.%m.%Y')
                    if date_str not in schedules_by_date:
                        schedules_by_date[date_str] = []
                    schedules_by_date[date_str].append(schedule)
            
            # Check if we have schedules for the requested date
            has_results = schedules.count() > 0
            
            # Create search context information
            search_context = {
                'type': search_type,
                'departure_city': departure_city if departure_city else None,
                'arrival_city': arrival_city if arrival_city else None,
                'departure_date': departure_date,
                'description': _get_search_description(search_type, departure_city, arrival_city, departure_date)
            }
            
            # Build URL for alternative dates if no results found
            alternative_dates_url = None
            if not has_results and (departure_city or arrival_city):
                params = []
                if departure_city:
                    params.append(f"from={departure_city}")
                if arrival_city:
                    params.append(f"to={arrival_city}")
                if departure_date:
                    params.append(f"date={departure_date.strftime('%Y-%m-%d')}")
                alternative_dates_url = f"{reverse('tickets:alternative_dates')}?{'&'.join(params)}"
            
            context = {
                'form': form,
                'schedules_by_date': schedules_by_date,
                'all_schedules': schedules,
                'routes': routes,
                'search_context': search_context,
                'has_results': has_results,
                'alternative_dates_url': alternative_dates_url,
                'total_routes': routes.count(),
                'total_schedules': schedules.count(),
            }
            
            return render(request, 'tickets/search_results.html', context)
    
    # If form is invalid or not GET, redirect to home
    return redirect('tickets:home')


def _get_search_description(search_type, departure_city, arrival_city, departure_date):
    """
    Generate human-readable search description.
    """
    descriptions = []
    
    if search_type == "specific_route":
        descriptions.append(f"Routes from {departure_city} to {arrival_city}")
    elif search_type == "from_city":
        descriptions.append(f"All routes from {departure_city}")
    elif search_type == "to_city":
        descriptions.append(f"All routes to {arrival_city}")
    else:
        descriptions.append("All available routes")
    
    if departure_date:
        date_str = departure_date.strftime('%B %d, %Y')
        descriptions.append(f"with schedules for {date_str}")
        descriptions.append("(routes operating on this date or without specific date)")
    else:
        descriptions.append("for all dates")
    
    return " ".join(descriptions)


def schedule_detail(request, schedule_id):
    """
    Display detailed information about a specific schedule with seat selection.
    """
    schedule = get_object_or_404(Schedule, id=schedule_id, is_active=True)
    
    # Get seat status
    seat_status = schedule.get_seat_status()
    
    # Get seat layout from bus configuration
    if schedule.bus.seat_layout_config:
        # Use custom layout from SeatLayout model
        layout_data = schedule.bus.seat_layout_config.get_layout_display()
        seat_layout = []
        
        for row_data in layout_data:
            row = []
            for seat in row_data:
                if seat and seat in seat_status:
                    row.append({
                        'number': seat,
                        'status': seat_status[seat]
                    })
                elif seat:
                    # Seat exists in layout but no status yet (available)
                    row.append({
                        'number': seat,
                        'status': 'available'
                    })
                else:
                    # Empty space (null in layout)
                    row.append(None)
            seat_layout.append(row)
    else:
        # Fallback to original auto-generated layout
        seat_layout = []
        seats_per_row = schedule.bus.seats_per_row
        seats = list(seat_status.keys())
        seats.sort()
        
        for i in range(0, len(seats), seats_per_row):
            row = []
            for j in range(seats_per_row):
                if i + j < len(seats):
                    seat_num = seats[i + j]
                    row.append({
                        'number': seat_num,
                        'status': seat_status[seat_num]
                    })
                else:
                    row.append(None)
            seat_layout.append(row)
    
    context = {
        'schedule': schedule,
        'seat_layout': seat_layout,
        'seat_status': seat_status,
    }
    
    return render(request, 'tickets/schedule_detail.html', context)




def booking_detail(request, booking_id):
    """
    Display booking details and payment options.
    Works for both authenticated and anonymous users.
    """
    # Force fresh data from database
    booking = get_object_or_404(Booking, id=booking_id)
    booking.refresh_from_db()
    
    # Check if booking belongs to current user or is anonymous
    user = getattr(request, 'user', None)
    is_authenticated = getattr(user, 'is_authenticated', False) if user else False
    
    if not is_authenticated and booking.user:
        messages.error(request, 'Access denied. This booking belongs to another user.')
        return redirect('tickets:home')
    
    if is_authenticated and booking.user and booking.user != user:
        messages.error(request, 'Access denied. This booking belongs to another user.')
        return redirect('tickets:home')
    
    # Determine if user is anonymous or authenticated
    is_anonymous = not is_authenticated or booking.user is None
    
    # Initialize appropriate form
    if is_anonymous:
        from .forms import AnonymousBookingForm
        form = AnonymousBookingForm(initial={
            'first_name': booking.first_name,
            'last_name': booking.last_name,
            'email': booking.email,
            'phone': booking.phone
        })
    else:
        from .forms import BookingForm
        form = BookingForm(initial={
            'first_name': booking.first_name,
            'last_name': booking.last_name,
            'email': booking.email,
            'phone': booking.phone
        })
    
    context = {
        'booking': booking,
        'tickets': booking.tickets.all(),
        'form': form,
        'is_anonymous': is_anonymous,
    }
    
    return render(request, 'tickets/booking_detail.html', context)


@require_POST
def process_payment(request, booking_id):
    """
    Process payment for a booking.
    Works for both authenticated and anonymous users.
    """
    booking = get_object_or_404(Booking, id=booking_id)
    
    # Check if booking belongs to current user or is anonymous
    user = getattr(request, 'user', None)
    is_authenticated = getattr(user, 'is_authenticated', False) if user else False
    
    if not is_authenticated and booking.user:
        messages.error(request, 'Access denied. This booking belongs to another user.')
        return redirect('tickets:home')
    
    if is_authenticated and booking.user and booking.user != user:
        messages.error(request, 'Access denied. This booking belongs to another user.')
        return redirect('tickets:home')
    
    if booking.is_paid:
        messages.warning(request, 'Ta rezerwacja zostala juz oplacone.')
        return redirect('booking_detail', booking_id=booking_id)
    
    try:
        # Create payment record
        payment = Payment.objects.create(
            booking=booking,
            amount=booking.total_price,
            payment_method='card',  # In real app, this would come from form
            status='completed',
            transaction_id=f"TXN{uuid.uuid4().hex[:12].upper()}"
        )
        
        # Update booking status
        booking.is_paid = True
        booking.save()
        
        # Update ticket statuses
        for ticket in booking.tickets.all():
            ticket.status = 'paid'
            ticket.save()
        
        # Send confirmation email
        send_booking_confirmation_email(booking)
        
        messages.success(request, 'Platnosc zostala przetworzona pomyslnie. Potwierdzenie zostalo wyslane na email.')
        return redirect('booking_confirmation', booking_id=booking_id)
        
    except Exception as e:
        messages.error(request, 'Wystapil blad podczas przetwarzania platnosci. Prosze sprobowac ponownie.')
        return redirect('booking_detail', booking_id=booking_id)


def booking_confirmation(request, booking_id):
    """
    Display booking confirmation after successful payment.
    """
    booking = get_object_or_404(Booking, id=booking_id)
    
    # Check if booking belongs to current user or is anonymous
    if not request.user.is_authenticated or (booking.user and booking.user != request.user):
        messages.error(request, 'Nie masz dostepu do tej rezerwacji.')
        return redirect('tickets:home')
    
    context = {
        'booking': booking,
        'tickets': booking.tickets.all(),
    }
    
    return render(request, 'tickets/booking_confirmation.html', context)


@login_required
@require_POST
def delete_booking(request, booking_id):
    """
    Delete a booking and release tickets.
    Only allows deletion of unpaid bookings.
    """
    booking = get_object_or_404(Booking, id=booking_id)
    
    # Check if booking belongs to current user
    if not request.user.is_authenticated or booking.user != request.user:
        messages.error(request, 'Доступ запрещен.')
        return redirect('tickets:user_bookings')
    
    # Only allow deletion of unpaid bookings
    if booking.is_paid:
        messages.error(request, 'Нельзя удалить оплаченное бронирование.')
        return redirect('tickets:user_bookings')
    
    try:
        with transaction.atomic():
            # Release tickets back to available
            tickets = booking.tickets.all()
            for ticket in tickets:
                ticket.status = 'available'
                ticket.save()
            
            # Delete the booking
            booking.delete()
            
            messages.success(request, 'Бронирование успешно удалено.')
            
    except Exception as e:
        messages.error(request, f'Ошибка при удалении бронирования: {str(e)}')
    
    return redirect('tickets:user_bookings')


def update_booking(request, booking_id):
    """
    Update booking information for authenticated users.
    """
    booking = get_object_or_404(Booking, id=booking_id)
    
    # Check if booking belongs to current user
    if not request.user.is_authenticated or booking.user != request.user:
        messages.error(request, 'Access denied to this booking.')
        return redirect('tickets:home')
    
    if request.method == 'POST':
        from .forms import BookingForm
        form = BookingForm(request.POST)
        
        if form.is_valid():
            # Update booking with passenger information
            booking.first_name = form.cleaned_data['first_name']
            booking.last_name = form.cleaned_data['last_name']
            booking.email = form.cleaned_data['email']
            booking.phone = form.cleaned_data['phone']
            booking.save()
            
            # Create or update PassengerInfo
            
            passenger_info, created = PassengerInfo.objects.get_or_create(
                booking=booking,
                defaults={
                    'first_name': form.cleaned_data['first_name'],
                    'last_name': form.cleaned_data['last_name'],
                    'email': form.cleaned_data['email'],
                    'phone': form.cleaned_data['phone']
                }
            )
            
            if not created:
                # Update existing PassengerInfo
                passenger_info.first_name = form.cleaned_data['first_name']
                passenger_info.last_name = form.cleaned_data['last_name']
                passenger_info.email = form.cleaned_data['email']
                passenger_info.phone = form.cleaned_data['phone']
                passenger_info.save()
            
            messages.success(request, 'Booking information updated successfully!')
            return redirect('tickets:booking_detail', booking_id=booking_id)
    else:
        from .forms import BookingForm
        form = BookingForm(initial={
            'first_name': booking.first_name,
            'last_name': booking.last_name,
            'email': booking.email,
            'phone': booking.phone
        })
    
    return render(request, 'tickets/booking_detail.html', {
        'booking': booking,
        'form': form,
        'is_anonymous': False,
        'tickets': booking.tickets.all(),
    })


def complete_anonymous_booking(request, booking_id):
    """
    Complete anonymous booking by updating passenger information and sending email.
    """
    booking = get_object_or_404(Booking, id=booking_id)
    
    # Check if booking is anonymous
    if booking.user:
        messages.error(request, 'This booking is not anonymous.')
        return redirect('tickets:home')
    
    if request.method == 'POST':
        from .forms import AnonymousBookingForm
        form = AnonymousBookingForm(request.POST)
        
        if form.is_valid():
            # Update booking with passenger information
            booking.first_name = form.cleaned_data['first_name']
            booking.last_name = form.cleaned_data['last_name']
            booking.email = form.cleaned_data['email']
            booking.phone = form.cleaned_data['phone']
            booking.save()
            
            # Create or update PassengerInfo
            passenger_info, created = PassengerInfo.objects.get_or_create(
                booking=booking,
                defaults={
                    'first_name': form.cleaned_data['first_name'],
                    'last_name': form.cleaned_data['last_name'],
                    'email': form.cleaned_data['email'],
                    'phone': form.cleaned_data['phone']
                }
            )
            
            if not created:
                # Update existing PassengerInfo
                passenger_info.first_name = form.cleaned_data['first_name']
                passenger_info.last_name = form.cleaned_data['last_name']
                passenger_info.email = form.cleaned_data['email']
                passenger_info.phone = form.cleaned_data['phone']
                passenger_info.save()
            
            # Send email with ticket
            # Check email backend and provide appropriate message
            from django.conf import settings
            is_console_backend = 'console' in settings.EMAIL_BACKEND.lower()
            
            try:
                send_booking_email(booking)
                if is_console_backend:
                    messages.info(request, f'Booking confirmed! Email content displayed in server console for testing. Your booking reference is {booking.booking_reference}. You can download your PDF ticket below.')
                else:
                    messages.success(request, 'Tickets sent to your email! You can also download PDF.')
            except ValueError as ve:
                messages.error(request, f'Email error: {str(ve)}. Please check your email address.')
            except Exception as e:
                import traceback
                # print(f"Email sending error in complete_anonymous_booking: {str(e)}")
                # print(f"Traceback: {traceback.format_exc()}")
                
                if is_console_backend:
                    messages.info(request, f'Booking confirmed! Email content displayed in server console. Your booking reference is {booking.booking_reference}. You can download your PDF ticket below.')
                else:
                    # Provide user-friendly error message with alternatives
                    error_msg = str(e)
                    if "authentication" in error_msg.lower():
                        user_msg = "Email server authentication failed. Please download your PDF ticket below."
                    elif "connection" in error_msg.lower():
                        user_msg = "Cannot connect to email server. Please download your PDF ticket below."
                    elif "timeout" in error_msg.lower():
                        user_msg = "Email server timeout. Please download your PDF ticket below."
                    else:
                        user_msg = "Email sending failed. Please download your PDF ticket below."
                    
                    messages.warning(request, f'Booking confirmed! {user_msg} Your booking reference is {booking.booking_reference}.')
            
            return redirect('tickets:booking_detail', booking_id=booking_id)
    else:
        from .forms import AnonymousBookingForm
        form = AnonymousBookingForm(initial={
            'first_name': booking.first_name,
            'last_name': booking.last_name,
            'email': booking.email,
            'phone': booking.phone
        })
    
    return render(request, 'tickets/booking_detail.html', {
        'booking': booking,
        'form': form,
        'is_anonymous': True,
        'tickets': booking.tickets.all(),
    })


def generate_ticket_pdf(booking):
    """
    Generate PDF ticket with improved styling and Cyrillic support.
    Used by both download and email functions.
    """
    from io import BytesIO
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.units import inch
    from reportlab.lib.colors import black, blue, gray, lightgrey
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    import os
    
    # Register fonts that support Cyrillic
    try:
        # Try to use Arial (supports Cyrillic)
        pdfmetrics.registerFont(TTFont('Arial', 'arial.ttf'))
        pdfmetrics.registerFont(TTFont('Arial-Bold', 'arialbd.ttf'))
        pdfmetrics.registerFont(TTFont('Arial', 'Arial.ttf'))
        pdfmetrics.registerFont(TTFont('Arial-Bold', 'Arialbd.ttf'))
        font_normal = 'Arial'
        font_bold = 'Arial-Bold'
    except:
        try:
            # Try DejaVu (supports Cyrillic)
            pdfmetrics.registerFont(TTFont('DejaVu', 'DejaVuSans.ttf'))
            pdfmetrics.registerFont(TTFont('DejaVu-Bold', 'DejaVuSans-Bold.ttf'))
            font_normal = 'DejaVu'
            font_bold = 'DejaVu-Bold'
        except:
            # Fallback to Helvetica (won't support Cyrillic properly)
            font_normal = 'Helvetica'
            font_bold = 'Helvetica-Bold'
    
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    
    # Header with better styling
    p.setFont(font_bold, 32)
    p.setFillColor(blue)
    p.drawString(100, height - 100, "БИЛЕТ НА АВТОБУС")
    
    # Add decorative line
    p.setStrokeColor(blue)
    p.setLineWidth(3)
    p.line(100, height - 115, width - 100, height - 115)
    
    # Booking Information Box
    p.setFillColor(lightgrey)
    p.rect(80, height - 180, width - 160, 80, fill=1, stroke=0)
    p.setFillColor(black)
    p.setFont(font_normal, 12)
    p.drawString(100, height - 160, "Номер брони: " + str(booking.booking_reference))
    p.drawString(100, height - 140, f"Дата бронирования: {booking.created_at.strftime('%d.%m.%Y %H:%M')}")
    p.drawString(100, height - 120, f"Статус: {'ОПЛАЧЕНО' if booking.is_paid else 'ОЖИДАНИЕ ОПЛАТЫ'}")
    
    # Passenger Information Box
    p.setFillColor(lightgrey)
    p.rect(80, height - 280, width - 160, 80, fill=1, stroke=0)
    p.setFillColor(black)
    p.setFont(font_normal, 12)
    p.drawString(100, height - 260, f"Имя: {booking.first_name} {booking.last_name}")
    p.drawString(100, height - 240, f"Email: {booking.email}")
    if booking.phone:
        p.drawString(100, height - 220, f"Телефон: {booking.phone}")
    
    # Route Information
    p.setFillColor(lightgrey)
    p.rect(80, height - 380, width - 160, 80, fill=1, stroke=0)
    p.setFillColor(black)
    p.setFont(font_normal, 12)
    
    # Get first ticket for route info
    first_ticket = booking.tickets.first()
    if first_ticket:
        route = first_ticket.schedule.route
        schedule = first_ticket.schedule
        
        p.drawString(100, height - 340, f"Маршрут: {route.departure_city} - {route.arrival_city}")
        p.drawString(100, height - 325, f"Отправление: {schedule.departure_time.strftime('%d.%m.%Y %H:%M')}")
        p.drawString(100, height - 310, f"Прибытие: {schedule.arrival_time.strftime('%d.%m.%Y %H:%M')}")
        p.drawString(100, height - 295, f"Автобус: {schedule.bus.registration_number}")
    
    # Ticket Details
    y_position = height - 450
    
    for i, ticket in enumerate(booking.tickets.all()):
        p.setFont(font_normal, 12)
        p.drawString(100, y_position, f"Билет {i+1}: Место {ticket.seat_number}")
        p.drawString(120, y_position - 18, f"Цена: {ticket.price:.2f} руб.")
        p.drawString(120, y_position - 36, f"Статус: {ticket.get_status_display()}")
        y_position -= 60
    
    # Total Price
    p.setFont(font_bold, 16)
    p.drawString(100, y_position, f"ИТОГО: {booking.total_price:.2f} руб.")
    
    # Footer with better styling
    p.setFont(font_normal, 10)
    p.setFillColor(gray)
    p.drawString(100, 80, "Спасибо, что выбрали наш автобусный сервис!")
    p.drawString(100, 65, "Пожалуйста, прибывайте на вокзал за 30 минут до отправления.")
    p.drawString(100, 50, "Для поддержки: +7 (800) 123-45-67 или support@bustickets.com")
    
    p.save()
    pdf_data = buffer.getvalue()
    buffer.close()
    return pdf_data


def send_booking_email(booking):
    """
    Send booking confirmation email with detailed PDF attachment.
    """
    from django.conf import settings
    
    # Validate email configuration
    if not hasattr(settings, 'EMAIL_HOST') or not settings.EMAIL_HOST:
        raise ValueError("Email server not configured properly")
    
    if not hasattr(settings, 'EMAIL_HOST_USER') or not settings.EMAIL_HOST_USER:
        raise ValueError("Email user not configured properly")
    
    subject = f'Bus Ticket Booking - {booking.booking_reference}'
    
    # Generate PDF using the same function as download
    pdf_data = generate_ticket_pdf(booking)
    
    # Create detailed email
    from django.core.mail import EmailMessage
    
    # HTML email body
    tickets_info = ""
    for i, ticket in enumerate(booking.tickets.all()):
        tickets_info += f"""
        <ul>
            <li><strong>Route:</strong> {ticket.schedule.route.departure_city} - {ticket.schedule.route.arrival_city}</li>
            <li><strong>Departure:</strong> {ticket.schedule.departure_time.strftime('%d.%m.%Y %H:%M')}</li>
            <li><strong>Seat:</strong> {ticket.seat_number}</li>
        </ul>
        """
    
    html_content = f"""
    <html>
    <head></head>
    <body>
        <h2>Bus Ticket Booking Confirmation</h2>
        <p>Dear {booking.first_name} {booking.last_name},</p>
        <p>Thank you for your booking! Your tickets are attached to this email.</p>
        
        <h3>Booking Details:</h3>
        <ul>
            <li><strong>Reference:</strong> {booking.booking_reference}</li>
            <li><strong>Status:</strong> {'Paid' if booking.is_paid else 'Pending Payment'}</li>
            <li><strong>Total Amount:</strong> {booking.total_price:.2f} RUB</li>
        </ul>
        
        <h3>Route Information:</h3>
        {tickets_info}
        
        <p><strong>Important:</strong> Please arrive at the station 30 minutes before departure.</p>
        <p>Have a safe journey!</p>
        
        <p>Best regards,<br>Bus Tickets Team</p>
    </body>
    </html>
    """
    
    # Validate email address
    if not booking.email:
        raise ValueError("No email address provided for booking")
    
    # print(f"Attempting to send email to: {booking.email}")
    # print(f"Booking reference: {booking.booking_reference}")
    # print(f"PDF size: {len(pdf_data)} bytes")
    
    email = EmailMessage(
        subject,
        html_content,
        settings.DEFAULT_FROM_EMAIL,
        [booking.email]
    )
    email.content_subtype = "html"
    email.attach(f'ticket_{booking.booking_reference}.pdf', pdf_data, 'application/pdf')
    
    try:
        result = email.send()
        # print(f"Email sent successfully. Result: {result}")
        # print(f"Email sent to {booking.email} with PDF attachment")
    except Exception as email_error:
        # print(f"Email sending failed: {str(email_error)}")
        
        # Try alternative method with different settings
        try:
            from django.core.mail import get_connection
            connection = get_connection(
                backend='django.core.mail.backends.smtp.EmailBackend',
                host=settings.EMAIL_HOST,
                port=settings.EMAIL_PORT,
                username=settings.EMAIL_HOST_USER,
                password=settings.EMAIL_HOST_PASSWORD,
                use_ssl=settings.EMAIL_USE_SSL,
                use_tls=False,  # Try without TLS
                timeout=30
            )
            
            email.connection = connection
            result = email.send()
            # print(f"Email sent successfully with alternative method. Result: {result}")
        except Exception as alt_error:
            # print(f"Alternative email sending also failed: {str(alt_error)}")
            
            # Fallback: Save email content to console/log for manual sending
            # print("\n=== EMAIL CONTENT FOR MANUAL SENDING ===")
            # print(f"To: {booking.email}")
            # print(f"Subject: {subject}")
            # print(f"Body: {html_content}")
            # print(f"PDF Attachment: ticket_{booking.booking_reference}.pdf ({len(pdf_data)} bytes)")
            # print("=== END EMAIL CONTENT ===\n")
            
            # Raise the original error but provide fallback
            raise Exception(f"Email sending failed. Content saved to console. Original error: {str(email_error)}")


def download_ticket_pdf(request, booking_id):
    """
    Generate and download detailed PDF ticket.
    """
    booking = get_object_or_404(Booking, id=booking_id)
    
    # Check if booking belongs to current user or is anonymous
    user = getattr(request, 'user', None)
    is_authenticated = getattr(user, 'is_authenticated', False) if user else False
    
    # Debug logging
    # print(f"PDF Download Request - Booking ID: {booking_id}")
    # print(f"User authenticated: {is_authenticated}")
    # print(f"Booking user: {booking.user}")
    # print(f"Request user: {user}")
    
    # Allow access if:
    # 1. User is authenticated and booking belongs to them, OR
    # 2. User is anonymous and booking has no user (anonymous booking)
    if is_authenticated and booking.user and booking.user != user:
        # print("Access denied: Authenticated user trying to access another user's booking")
        messages.error(request, 'Access denied to this booking.')
        return redirect('tickets:home')
    
    if not is_authenticated and booking.user:
        # print("Access denied: Anonymous user trying to access authenticated user's booking")
        messages.error(request, 'Access denied to this booking.')
        return redirect('tickets:home')
    
    # print("Access granted to PDF download")
    # Check if booking is paid
    if not booking.is_paid:
        # print("Access denied: Booking not paid")
        messages.error(request, 'PDF download is only available after payment completion.')
        return redirect('tickets:booking_detail', booking_id=booking.id)
    
    # print("Access granted to PDF download")
    
    # Generate PDF using the same function as email
    pdf_data = generate_ticket_pdf(booking)
    
    # Create HTTP response
    from django.http import HttpResponse
    response = HttpResponse(pdf_data, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="ticket_{booking.booking_reference}.pdf"'
    return response


def send_booking_confirmation_email(booking):
    """
    Send booking confirmation email with PDF attachment.
    """
    subject = f'Potwierdzenie rezerwacji - {booking.booking_reference}'
    
    # Generate HTML email content
    html_content = render_to_string('tickets/email/booking_confirmation.html', {
        'booking': booking,
        'tickets': booking.tickets.all(),
    })
    
    # Generate PDF for attachment
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    styles = getSampleStyleSheet()
    story = []
    
    # Similar PDF generation as in download_ticket_pdf
    # ... (PDF generation code here)
    
    try:
        send_mail(
            subject=subject,
            message='Twoja rezerwacja zostala potwierdzona. Szczegoly w zalaczeniu.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[booking.email],
            html_message=html_content,
            fail_silently=False,
        )
    except Exception as e:
        # Log error but don't fail the request
        # print(f"Error sending email: {e}")
        pass


# API Views
class RouteViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for routes.
    """
    queryset = Route.objects.filter(is_active=True)
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        queryset = Route.objects.filter(is_active=True)
        departure_city = self.request.query_params.get('departure_city')
        arrival_city = self.request.query_params.get('arrival_city')
        
        if departure_city:
            queryset = queryset.filter(departure_city__icontains=departure_city)
        if arrival_city:
            queryset = queryset.filter(arrival_city__icontains=arrival_city)
        
        return queryset


class ScheduleViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for schedules.
    """
    queryset = Schedule.objects.filter(is_active=True)
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        queryset = Schedule.objects.filter(is_active=True).select_related('route', 'bus')
        route_id = self.request.query_params.get('route_id')
        date = self.request.query_params.get('date')
        
        if route_id:
            queryset = queryset.filter(route_id=route_id)
        if date:
            queryset = queryset.filter(departure_time__date=date)
        
        return queryset


@api_view(['GET'])
@permission_classes([IsAuthenticatedOrReadOnly])
def check_seat_availability(request, schedule_id):
    """
    API endpoint to check seat availability for a schedule.
    """
    schedule = get_object_or_404(Schedule, id=schedule_id, is_active=True)
    seat_status = schedule.get_seat_status()
    
    return Response({
        'schedule_id': schedule.id,
        'total_seats': schedule.bus.total_seats,
        'available_seats': schedule.available_seats,
        'seat_status': seat_status
    })


def register(request):
    """
    User registration view.
    """
    if request.method == 'POST':
        from .forms import CustomUserCreationForm
        from django.contrib.auth import login
        
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('tickets:home')
    else:
        from .forms import CustomUserCreationForm
        form = CustomUserCreationForm()
    
    return render(request, 'tickets/register.html', {'form': form})


@login_required
def user_profile(request):
    """
    User profile view.
    """
    if request.method == 'POST':
        from .forms import UserProfileForm
        
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            # Save the user profile
            user = form.save()
            
            # Update all related bookings with new user info
            Booking.objects.filter(user=user).update(
                first_name=user.first_name,
                last_name=user.last_name,
                email=user.email
            )
            
            # Update all related PassengerInfo records
            PassengerInfo.objects.filter(booking__user=user).update(
                first_name=user.first_name,
                last_name=user.last_name,
                email=user.email
            )
            
            messages.success(request, 'Profile updated successfully!')
            return redirect('tickets:user_profile')
    else:
        from .forms import UserProfileForm
        form = UserProfileForm(instance=request.user)
    
    context = {
        'form': form,
        'user_bookings': Booking.objects.filter(user=request.user).order_by('-created_at')[:5]
    }
    return render(request, 'tickets/profile.html', context)


@login_required
def user_bookings(request):
    """
    User bookings history view.
    """
    bookings = Booking.objects.filter(user=request.user).order_by('-created_at')
    
    context = {
        'bookings': bookings
    }
    return render(request, 'tickets/bookings.html', context)


@api_view(['GET'])
@permission_classes([IsAuthenticatedOrReadOnly])
def ajax_search_routes(request):
    """
    Ajax API endpoint for route search.
    Returns routes that start with the given query string.
    """
    query = request.GET.get('q', '').strip()
    
    if len(query) < 2:
        return JsonResponse({'routes': []})
    
    # Search routes where departure city starts with query
    routes = Route.objects.filter(
        is_active=True,
        departure_city__icontains=query
    ).order_by('departure_city', 'arrival_city')[:10]
    
    # Format response data
    route_data = []
    for route in routes:
        route_data.append({
            'id': route.id,
            'departure_city': route.departure_city,
            'arrival_city': route.arrival_city,
            'distance': route.distance,
            'estimated_time': route.estimated_time,
            'base_price': float(route.base_price),
            'display_name': f"{route.departure_city} - {route.arrival_city}"
        })
    
    return JsonResponse({'routes': route_data})


@api_view(['GET'])
@permission_classes([IsAuthenticatedOrReadOnly])
def ajax_search_cities(request):
    """
    Ajax API endpoint for city search.
    Returns cities that start with the given query string.
    """
    query = request.GET.get('q', '').strip()
    
    if len(query) < 2:
        return JsonResponse({'cities': []})
    
    # Get unique departure cities
    departure_cities = Route.objects.filter(
        is_active=True,
        departure_city__icontains=query
    ).values_list('departure_city', flat=True).distinct()[:10]
    
    # Get unique arrival cities
    arrival_cities = Route.objects.filter(
        is_active=True,
        arrival_city__icontains=query
    ).values_list('arrival_city', flat=True).distinct()[:10]
    
    # Combine and deduplicate cities
    all_cities = list(set(list(departure_cities) + list(arrival_cities)))
    all_cities.sort()
    
    return JsonResponse({'cities': all_cities[:15]})


def seat_selection(request, schedule_id):
    """
    Seat selection page with real-time updates.
    """
    schedule = get_object_or_404(Schedule, id=schedule_id)
    route = schedule.route
    bus = schedule.bus
    
    # Get seat layout from bus configuration
    if bus.seat_layout_config:
        # Use custom layout from SeatLayout model
        layout_data = bus.seat_layout_config.get_layout_display()
        seat_layout = []
        
        for row_data in layout_data:
            for seat in row_data:
                if seat:
                    seat_layout.append(seat)
    else:
        # Fallback to auto-generated layout
        seat_layout = []
        seats_per_row = bus.seats_per_row
        total_seats = bus.total_seats
        
        for i in range(1, total_seats + 1):
            seat_layout.append(i)
    
    context = {
        'schedule': schedule,
        'route': route,
        'bus': bus,
        'schedule_id': schedule_id,
        'seat_layout': seat_layout,  # Pass seat layout to template
        'total_seats': bus.total_seats,
        'seats_per_row': bus.seats_per_row
    }
    return render(request, 'tickets/seat_selection.html', context)


@csrf_exempt
def create_temp_booking(request):
    """
    Create temporary booking for selected seats with atomic locking.
    Prevents concurrent users from selecting the same seats.
    """
    from django.db import transaction
    
    if request.method != 'POST':
        return JsonResponse({'error': 'Only POST method allowed'}, status=405)
    
    try:
        # Parse JSON data
        if not request.body:
            return JsonResponse({'error': 'No request body found'}, status=400)
        
        try:
            import json
            data = json.loads(request.body.decode('utf-8'))
        except json.JSONDecodeError as e:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
        
        # Extract data
        schedule_id = data.get('schedule_id')
        seats = data.get('seats', [])
        passenger = data.get('passenger', {})
        
        if not schedule_id or not seats:
            return JsonResponse({'error': 'Missing required data'}, status=400)
        
        # Get schedule
        schedule = get_object_or_404(Schedule, id=schedule_id)
        
        # Clear any existing locks for this session first
        from django.core.cache import cache
        import time
        
        # Check and lock seats
        locked_seats = []
        failed_seats = []
        
        # Try to lock all seats atomically
        with transaction.atomic():
            for seat_number in seats:
                # print(f"DEBUG: Processing seat {seat_number}", flush=True)
                
                # Check if seat is already booked in database
                is_booked = Ticket.objects.filter(schedule=schedule, seat_number=seat_number, status__in=['booked', 'paid']).exists()
                # print(f"DEBUG: Seat {seat_number} is_booked: {is_booked}", flush=True)
                
                if is_booked:
                    failed_seats.append(seat_number)
                    continue
                
                # Check if seat is already locked in cache
                lock_key = f"seat_lock_{schedule_id}_{seat_number}"
                existing_lock = cache.get(lock_key)
                # print(f"DEBUG: Seat {seat_number} existing_lock: {existing_lock}", flush=True)
                
                if existing_lock:
                    # Check if lock belongs to current user/session (same logic as lock_seat)
                    user_id = request.user.id if request.user.is_authenticated else None
                    session_id = request.session.session_key or 'anonymous'
                    
                    # print(f"DEBUG: Lock user_id: {existing_lock.get('user_id')}, current user_id: {user_id}", flush=True)
                    # print(f"DEBUG: Lock session_id: {existing_lock.get('session_id')}, current session_id: {session_id}", flush=True)
                    
                    if (existing_lock.get('user_id') == user_id and 
                        existing_lock.get('session_id') == session_id):
                        # print(f"DEBUG: Seat {seat_number} already locked by same user", flush=True)
                        # Already locked by this user - treat as successfully locked
                        locked_seats.append(seat_number)
                        continue
                    
                    # Check if lock is expired (older than 30 seconds)
                    lock_age = time.time() - existing_lock.get('timestamp', 0)
                    # print(f"DEBUG: Lock age: {lock_age:.2f} seconds", flush=True)
                    
                    if lock_age > 30:
                        # print(f"DEBUG: Removing expired lock for seat {seat_number}", flush=True)
                        cache.delete(lock_key)  # Remove expired lock
                    else:
                        # print(f"DEBUG: Seat {seat_number} is locked by another user", flush=True)
                        failed_seats.append(seat_number)
                        continue
                
                # Lock the seat for 30 seconds
                # print(f"DEBUG: Locking seat {seat_number}", flush=True)
                cache.set(lock_key, {
                    'user_id': request.user.id if request.user.is_authenticated else None,
                    'timestamp': time.time(),
                    'session_id': request.session.session_key or 'anonymous'
                }, timeout=30)
                
                locked_seats.append(seat_number)
                # print(f"DEBUG: Successfully locked seat {seat_number}", flush=True)
        
        if failed_seats:
            # Release locks on successfully locked seats
            for seat_number in locked_seats:
                lock_key = f"seat_lock_{schedule_id}_{seat_number}"
                cache.delete(lock_key)
            
            return JsonResponse({
                'error': 'Some seats are no longer available',
                'unavailable_seats': failed_seats
            }, status=400)
        
        # Create booking with atomic transaction
        try:
            with transaction.atomic():
                # Generate unique booking reference
                import uuid
                booking_ref = f"BT{uuid.uuid4().hex[:8].upper()}"
                
                # Get user info
                user = getattr(request, 'user', None)
                is_authenticated = getattr(user, 'is_authenticated', False) if user else False
                
                # Get passenger info
                first_name = passenger.get('first_name', '')
                last_name = passenger.get('last_name', '')
                email = passenger.get('email', '')
                phone = passenger.get('phone', '')
                
                # Calculate total price
                total_price = schedule.current_price * len(locked_seats)
                
                # Create tickets first to ensure they can be created
                created_tickets = []
                for seat_number in locked_seats:
                    ticket = Ticket.objects.create(
                        schedule=schedule,
                        seat_number=seat_number,
                        status='booked',
                        price=schedule.current_price,
                        booking_reference=booking_ref
                    )
                    created_tickets.append(ticket)
                
                # Now create booking (this will only be committed if tickets were created successfully)
                if is_authenticated:
                    booking = Booking.objects.create(
                        user=user,
                        booking_reference=booking_ref,
                        first_name=user.first_name or first_name,
                        last_name=user.last_name or last_name,
                        email=user.email or email,
                        phone=phone or '',
                        total_price=total_price,
                        is_paid=False
                    )
                else:
                    booking = Booking.objects.create(
                        booking_reference=booking_ref,
                        first_name=first_name,
                        last_name=last_name,
                        email=email,
                        phone=phone,
                        total_price=total_price,
                        is_paid=False
                    )
                
                # Link tickets to booking
                for ticket in created_tickets:
                    booking.tickets.add(ticket)
                
                # Verify that booking has tickets
                if not booking.tickets.exists():
                    raise ValueError("Failed to create tickets for booking")
                
                # Create PassengerInfo for all users
                if is_authenticated:
                    PassengerInfo.objects.create(
                        booking=booking,
                        first_name=user.first_name or '',
                        last_name=user.last_name or '',
                        email=user.email or '',
                        phone=phone or ''
                    )
                else:
                    PassengerInfo.objects.create(
                        booking=booking,
                        first_name=first_name,
                        last_name=last_name,
                        email=email,
                        phone=phone
                    )
                
                # If we get here, everything was created successfully
                return JsonResponse({
                    'success': True,
                    'booking_id': booking.id,
                    'booking_reference': booking_ref,
                    'tickets': [{'id': t.id, 'seat_number': t.seat_number} for t in created_tickets],
                    'total_price': booking.total_price
                })
            
        except Exception as e:
            # Release all locks on error
            for seat_number in locked_seats:
                lock_key = f"seat_lock_{schedule_id}_{seat_number}"
                cache.delete(lock_key)
            return JsonResponse({'error': str(e)}, status=500)
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
def send_ticket_to_user(request, booking_id):
    """
    Send ticket to authenticated user's email.
    """
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Only POST method allowed'}, status=405)
    
    try:
        # Check if user is authenticated
        if not request.user.is_authenticated:
            return JsonResponse({'success': False, 'error': 'Authentication required'}, status=401)
        
        # Get booking
        booking = get_object_or_404(Booking, id=booking_id)
        
        # Check if user owns this booking or is staff
        if booking.user != request.user and not request.user.is_staff:
            return JsonResponse({'success': False, 'error': 'Access denied'}, status=403)
        
        # Check if booking is paid
        if not booking.is_paid:
            return JsonResponse({'success': False, 'error': 'Email sending is only available after payment completion'}, status=400)
        
        # Check email backend and provide appropriate message
        from django.conf import settings
        is_console_backend = 'console' in settings.EMAIL_BACKEND.lower()
        
        try:
            # Use existing send_booking_email function
            send_booking_email(booking)
            if is_console_backend:
                message = f'Email content displayed in server console for testing. Your booking reference is {booking.booking_reference}.'
            else:
                message = 'Ticket sent to your email! You can also download PDF below.'
            
            return JsonResponse({
                'success': True,
                'message': message
            })
            
        except ValueError as ve:
            return JsonResponse({
                'success': False,
                'error': f'Email error: {str(ve)}. Please check your email address.'
            }, status=400)
        except Exception as e:
            import traceback
            # print(f"Email sending error in send_ticket_to_user: {str(e)}")
            # print(f"Traceback: {traceback.format_exc()}")
            
            if is_console_backend:
                message = f'Email content displayed in server console. Your booking reference is {booking.booking_reference}.'
            else:
                error_msg = str(e)
                if "authentication" in error_msg.lower():
                    message = "Email server authentication failed. Please download your PDF ticket below."
                elif "connection" in error_msg.lower():
                    message = "Cannot connect to email server. Please download your PDF ticket below."
                elif "timeout" in error_msg.lower():
                    message = "Email server timeout. Please download your PDF ticket below."
                else:
                    message = "Email sending failed. Please download your PDF ticket below."
            
            return JsonResponse({
                'success': True,  # Return success so user gets the message
                'message': message
            })
        
    except Exception as e:
        # print(f"Error in send_ticket_to_user: {str(e)}")
        return JsonResponse({
            'success': False,
            'error': 'Server error. Please try again.'
        }, status=500)


@csrf_exempt
def send_ticket_to_custom_email(request, booking_id):
    """
    Send ticket to custom email address (user's choice).
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'Only POST method allowed'}, status=405)
    
    try:
        # Check if user is authenticated
        if not request.user.is_authenticated:
            return JsonResponse({'error': 'Authentication required'}, status=401)
        
        # Get booking
        booking = get_object_or_404(Booking, id=booking_id)
        
        # Check if user owns this booking or is staff
        if booking.user != request.user and not request.user.is_staff:
            return JsonResponse({'error': 'Access denied'}, status=403)
        
        # Check if booking is paid
        if not booking.is_paid:
            return JsonResponse({'error': 'Email sending is only available after payment completion'}, status=400)
        
        # Parse JSON data
        try:
            import json
            data = json.loads(request.body.decode('utf-8'))
            target_email = data.get('email', '').strip()
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
        
        # Validate email
        if not target_email:
            return JsonResponse({'error': 'Email address is required'}, status=400)
        
        import re
        email_regex = r'^[^\s@]+@[^\s@]+\.[^\s@]+$'
        if not re.match(email_regex, target_email):
            return JsonResponse({'error': 'Invalid email address'}, status=400)
        
        # Check email backend and provide appropriate message
        from django.conf import settings
        is_console_backend = 'console' in settings.EMAIL_BACKEND.lower()
        
        try:
            # Temporarily update booking email for sending
            original_email = booking.email
            booking.email = target_email
            booking.save(update_fields=['email'])
            
            # Use existing send_booking_email function
            send_booking_email(booking)
            
            # Restore original email
            booking.email = original_email
            booking.save(update_fields=['email'])
            
            if is_console_backend:
                message = f'Email content displayed in server console for testing. Your booking reference is {booking.booking_reference}.'
            else:
                message = f'Ticket sent successfully to {target_email}!'
            
            return JsonResponse({
                'success': True,
                'message': message
            })
            
        except ValueError as ve:
            return JsonResponse({
                'success': False,
                'error': f'Email error: {str(ve)}. Please check your email address.'
            }, status=400)
        except Exception as e:
            import traceback
            # print(f"Email sending error in send_ticket_to_custom_email: {str(e)}")
            # print(f"Traceback: {traceback.format_exc()}")
            
            if is_console_backend:
                message = f'Email content displayed in server console. Your booking reference is {booking.booking_reference}.'
            else:
                error_msg = str(e)
                if "authentication" in error_msg.lower():
                    message = "Email server authentication failed. Please download your PDF ticket below."
                elif "connection" in error_msg.lower():
                    message = "Cannot connect to email server. Please download your PDF ticket below."
                elif "timeout" in error_msg.lower():
                    message = "Email server timeout. Please download your PDF ticket below."
                else:
                    message = "Email sending failed. Please download your PDF ticket below."
            
            return JsonResponse({
                'success': True,  # Return success so user gets the message
                'message': message
            })
        
    except Exception as e:
        # print(f"Error sending ticket to custom email: {str(e)}")
        import traceback
        traceback.print_exc()
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
def lock_seat(request, schedule_id):
    """
    Lock a seat for selection to prevent concurrent selection.
    Returns success if seat can be locked, error if already locked or booked.
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'Only POST method allowed'}, status=405)
    
    try:
        data = json.loads(request.body)
        seat_number = data.get('seat_number')
        
        if not seat_number:
            return JsonResponse({'error': 'Seat number required'}, status=400)
        
        # Get schedule
        schedule = get_object_or_404(Schedule, id=schedule_id)
        
        # Check if seat is already booked
        if Ticket.objects.filter(schedule=schedule, seat_number=seat_number).exists():
            return JsonResponse({
                'success': False,
                'error': 'Seat is already booked',
                'status': 'booked'
            }, status=400)
        
        # Try to lock the seat
        from django.core.cache import cache
        import time
        
        lock_key = f"seat_lock_{schedule_id}_{seat_number}"
        existing_lock = cache.get(lock_key)
        
        if existing_lock:
            # Check if lock belongs to current user/session
            user_id = request.user.id if request.user.is_authenticated else None
            session_id = request.session.session_key or 'anonymous'
            
            if (existing_lock.get('user_id') == user_id and 
                existing_lock.get('session_id') == session_id):
                # Already locked by this user
                return JsonResponse({
                    'success': True,
                    'message': 'Seat already locked by you',
                    'locked_by': 'self'
                })
            else:
                # Locked by someone else
                return JsonResponse({
                    'success': False,
                    'error': 'Seat is locked by another user',
                    'status': 'locked'
                }, status=400)
        
        # Lock the seat for 30 seconds
        cache.set(lock_key, {
            'user_id': request.user.id if request.user.is_authenticated else None,
            'timestamp': time.time(),
            'session_id': request.session.session_key or 'anonymous'
        }, timeout=30)
        
        return JsonResponse({
            'success': True,
            'message': 'Seat locked successfully',
            'locked_until': time.time() + 30
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
def unlock_seat(request, schedule_id):
    """
    Unlock a seat (usually when user deselects it).
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'Only POST method allowed'}, status=405)
    
    try:
        data = json.loads(request.body)
        seat_number = data.get('seat_number')
        
        if not seat_number:
            return JsonResponse({'error': 'Seat number required'}, status=400)
        
        # Remove lock from cache
        from django.core.cache import cache
        lock_key = f"seat_lock_{schedule_id}_{seat_number}"
        cache.delete(lock_key)
        
        return JsonResponse({
            'success': True,
            'message': 'Seat unlocked successfully'
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@api_view(['GET'])
@permission_classes([IsAuthenticatedOrReadOnly])
def get_seat_status(request, schedule_id):
    """
    Get current seat status for a schedule.
    """
    try:
        # print(f"DEBUG: get_seat_status called for schedule {schedule_id}")
        schedule = get_object_or_404(Schedule, id=schedule_id)
        # print(f"DEBUG: Schedule found: {schedule}")
        
        # Get all tickets for this schedule
        tickets = Ticket.objects.filter(schedule=schedule)
        # print(f"DEBUG: Found {tickets.count()} tickets for this schedule")
        
        seats = {}
        
        # Generate seat layout (assuming 40 seats)
        for i in range(1, 41):
            seat_number = str(i)
            ticket = tickets.filter(seat_number=seat_number).first()
            
            status = 'available'
            if ticket:
                if ticket.status == 'paid':
                    status = 'paid'
                elif ticket.status == 'booked':
                    status = 'booked'
            
            seats[seat_number] = {
                'number': seat_number,
                'status': status,
                'ticket_id': ticket.id if ticket else None
            }
        
        # print(f"DEBUG: Generated seat status for {len(seats)} seats")
        return JsonResponse({'seats': seats})
        
    except Exception as e:
        # print(f"DEBUG: Exception in get_seat_status: {str(e)}")
        # print(f"DEBUG: Exception type: {type(e).__name__}")
        # import traceback
        # traceback.print_exc()
        return JsonResponse({'error': str(e)}, status=500)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@require_http_methods(["POST"])
def update_seat_status(request, schedule_id):
    """
    Update seat status (for admin use).
    """
    if not request.user.is_staff:
        return JsonResponse({'error': 'Admin access required'}, status=403)
    
    try:
        data = json.loads(request.body)
        seat_number = data.get('seat_number')
        new_status = data.get('status')
        
        if not seat_number or not new_status:
            return JsonResponse({'error': 'Seat number and status are required'}, status=400)
        
        schedule = get_object_or_404(Schedule, id=schedule_id)
        ticket = Ticket.objects.filter(
            schedule=schedule,
            seat_number=seat_number
        ).first()
        
        if ticket:
            ticket.status = new_status
            ticket.save()
        else:
            # Create new ticket if it doesn't exist
            Ticket.objects.create(
                schedule=schedule,
                seat_number=seat_number,
                price=schedule.current_price,
                status=new_status
            )
        
        # Broadcast update to connected clients
        broadcast_seat_update(schedule_id, seat_number, new_status)
        
        return JsonResponse({
            'success': True,
            'seat_number': seat_number,
            'status': new_status
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def process_payment(request, booking_id):
    """
    Process payment for a booking using LiPay or PayPal.
    """
    booking = get_object_or_404(Booking, id=booking_id)
    
    # Check if booking is already paid
    if booking.is_paid:
        messages.error(request, 'This booking has already been paid for.')
        return redirect('tickets:booking_detail', booking_id=booking_id)
    
    if request.method == 'POST':
        payment_method = request.POST.get('payment_method')
        
        if not payment_method:
            messages.error(request, 'Please select a payment method.')
            return redirect('tickets:booking_detail', booking_id=booking_id)
        
        try:
            # Check if payment already exists for this booking
            existing_payment = Payment.objects.filter(booking=booking).first()
            if existing_payment:
                # Update existing payment
                existing_payment.amount = booking.total_price
                existing_payment.payment_method = payment_method
                existing_payment.status = 'pending'
                existing_payment.transaction_id = f"TXN_{timezone.now().strftime('%Y%m%d%H%M%S')}_{booking_id}"
                existing_payment.save()
                payment = existing_payment
            else:
                # Create new payment record
                payment = Payment.objects.create(
                    booking=booking,
                    amount=booking.total_price,
                    payment_method=payment_method,
                    status='pending',
                    transaction_id=f"TXN_{timezone.now().strftime('%Y%m%d%H%M%S')}_{booking_id}"
                )
            
            # Process payment based on method
            if payment_method == 'lipay':
                # Simulate LiPay payment processing
                payment.status = 'completed'
                payment.paid_at = timezone.now()
                payment.save()
                
                # Update booking status
                booking.is_paid = True
                booking.save()
                
                # Update ticket statuses
                booking.tickets.update(status='paid')
                
                messages.success(request, 'Payment completed successfully with LiPay!')
                
            elif payment_method == 'paypal':
                # Simulate PayPal payment processing
                payment.status = 'completed'
                payment.paid_at = timezone.now()
                payment.save()
                
                # Update booking status
                booking.is_paid = True
                booking.save()
                
                # Update ticket statuses
                booking.tickets.update(status='paid')
                
                messages.success(request, 'Payment completed successfully with PayPal!')
            
            # Redirect to booking confirmation
            return redirect('tickets:booking_detail', booking_id=booking_id)
            
        except Exception as e:
            messages.error(request, f'Payment processing failed: {str(e)}')
            return redirect('tickets:booking_detail', booking_id=booking_id)
    
    # If GET request, redirect to booking detail
    return redirect('tickets:booking_detail', booking_id=booking_id)


def alternative_dates(request):
    """
    View for displaying alternative dates when no schedules found for requested date
    """
    from django.utils import timezone
    from datetime import timedelta
    from collections import defaultdict
    
    # Get search parameters
    from_city = request.GET.get('from', '')
    to_city = request.GET.get('to', '')
    original_date_str = request.GET.get('date', '')
    
    # Parse original date
    original_date = None
    if original_date_str:
        try:
            original_date = datetime.strptime(original_date_str, '%Y-%m-%d').date()
        except ValueError:
            original_date = timezone.now().date()
    else:
        original_date = timezone.now().date()
    
    # Search for alternative dates (next 14 days from today)
    today = timezone.now().date()
    end_date = today + timedelta(days=14)
    
    # Build base schedule query with city filters
    schedules_query = Schedule.objects.filter(is_active=True)
    
    if from_city and to_city:
        # Both cities specified - exact route search
        schedules_query = schedules_query.filter(
            route__departure_city__iexact=from_city,
            route__arrival_city__iexact=to_city,
            route__is_active=True
        )
    elif from_city:
        # Only departure city specified
        schedules_query = schedules_query.filter(
            route__departure_city__iexact=from_city,
            route__is_active=True
        )
    elif to_city:
        # Only arrival city specified
        schedules_query = schedules_query.filter(
            route__arrival_city__iexact=to_city,
            route__is_active=True
        )
    
    # Filter schedules for the next 14 days (excluding the original date)
    start_of_search = timezone.make_aware(datetime.combine(today, datetime.min.time()))
    end_of_search = timezone.make_aware(datetime.combine(end_date, datetime.min.time()))
    
    schedules_query = schedules_query.filter(
        departure_time__gte=start_of_search,
        departure_time__lt=end_of_search
    ).exclude(
        departure_time__date=original_date
    )
    
    # Get schedules with relationships
    schedules = schedules_query.select_related('route', 'bus').order_by('departure_time')
    
    # Group schedules by date and calculate prices
    alternative_dates = defaultdict(list)
    for schedule in schedules:
        date = schedule.departure_time.date()
        price = float(schedule.current_price)
        
        alternative_dates[date].append({
            'schedule': schedule,
            'price': price
        })
    
    # Prepare alternative dates data
    alternative_dates_list = []
    for date, schedule_list in sorted(alternative_dates.items()):
        if date >= today:  # Only show future dates
            prices = [item['price'] for item in schedule_list]
            min_price = min(prices)
            
            alternative_dates_list.append({
                'date': date,
                'schedules': [item['schedule'] for item in schedule_list],
                'min_price': f"{min_price:.0f}",
                'max_price': f"{max(prices):.0f}"
            })
    
    context = {
        'from_city': from_city,
        'to_city': to_city,
        'original_date': original_date,
        'alternative_dates': alternative_dates_list,
        'search_form': SearchForm(initial={
            'departure_city': from_city,
            'arrival_city': to_city,
            'departure_date': original_date_str
        })
    }
    
    return render(request, 'tickets/alternative_dates.html', context)


@csrf_exempt
def seat_updates_sse(request, schedule_id):
    """
    Server-Sent Events endpoint for real-time seat status updates.
    """
    try:
        def event_stream():
            try:
                # Generate unique client ID
                import uuid
                client_id = str(uuid.uuid4())
                
                # Send initial connection event
                yield f"data: {json.dumps({'type': 'connected', 'client_id': client_id, 'schedule_id': schedule_id})}\n\n"
                
                # Track sent updates to avoid duplicates
                sent_updates = set()
                
                while True:
                    current_time = time.time()
                    
                    # Get updates from cache
                    update_key = f"seat_updates_{schedule_id}"
                    updates = cache.get(update_key, [])
                    
                    if updates:
                        # Send only new updates
                        for update in updates:
                            update_id = f"{update.get('seat_number')}_{update.get('timestamp')}"
                            if update_id not in sent_updates:
                                yield f"data: {json.dumps({'type': 'seat_update', 'data': update})}\n\n"
                                sent_updates.add(update_id)
                    
                    # Send heartbeat every 30 seconds
                    yield f"data: {json.dumps({'type': 'heartbeat', 'timestamp': current_time})}\n\n"
                    
                    # Sleep briefly to prevent excessive CPU usage
                    time.sleep(2)
                    
            except GeneratorExit:
                # Client disconnected
                pass
            except Exception as e:
                # Send error message
                yield f"data: {json.dumps({'type': 'error', 'message': str(e)})}\n\n"
        
        response = StreamingHttpResponse(
            event_stream(),
            content_type='text/event-stream'
        )
        response['Cache-Control'] = 'no-cache'
        response['X-Accel-Buffering'] = 'no'  # Disable buffering for nginx
        
        return response
        
    except Exception as e:
        # Return error response if something goes wrong
        return JsonResponse({
            'error': f'SSE endpoint error: {str(e)}',
            'schedule_id': schedule_id
        }, status=500)


@csrf_exempt
def trigger_seat_update(request, schedule_id):
    """
    Manual trigger for seat updates (for testing).
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            seat_number = data.get('seat_number')
            status = data.get('status')
            
            # Trigger the signal
            from .signals import seat_status_changed
            seat_status_changed.send(
                sender=Ticket,
                schedule_id=schedule_id,
                seat_number=seat_number,
                status=status,
                ticket_id=None
            )
            
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Invalid method'})


@csrf_exempt
def test_api(request):
    """
    Simple test API endpoint to verify server is working.
    """
    # print(f"=== TEST API CALLED ===", flush=True)
    # print(f"Method: {request.method}", flush=True)
    # print(f"Body: {request.body}", flush=True)
    
    if request.method == 'POST':
        try:
            import json
            data = json.loads(request.body.decode('utf-8'))
            # print(f"DEBUG: Test API received data: {data}")
            return JsonResponse({
                'success': True,
                'message': 'Test API working',
                'received_data': data
            })
        except Exception as e:
            # print(f"DEBUG: Test API error: {e}")
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=400)
    else:
        return JsonResponse({
            'message': 'Test API endpoint - use POST request'
        })


@csrf_exempt
def test_email_config(request):
    """
    Test email configuration and connectivity
    """
    from django.conf import settings
    from django.core.mail import send_mail
    
    results = {}
    
    # Check basic configuration
    results['EMAIL_HOST'] = getattr(settings, 'EMAIL_HOST', 'Not configured')
    results['EMAIL_PORT'] = getattr(settings, 'EMAIL_PORT', 'Not configured')
    results['EMAIL_USE_SSL'] = getattr(settings, 'EMAIL_USE_SSL', 'Not configured')
    results['EMAIL_HOST_USER'] = getattr(settings, 'EMAIL_HOST_USER', 'Not configured')
    results['EMAIL_BACKEND'] = getattr(settings, 'EMAIL_BACKEND', 'Not configured')
    
    # Test basic email sending
    try:
        send_mail(
            'Test Email from BusTickets',
            'This is a test email to verify email configuration.',
            settings.DEFAULT_FROM_EMAIL,
            ['test@example.com'],
            fail_silently=False,
        )
        results['test_send'] = 'Success - email sent (but may not be delivered to test address)'
    except Exception as e:
        results['test_send'] = f'Failed: {str(e)}'
    
    return JsonResponse(results)


@csrf_exempt
def test_cache_status(request, schedule_id):
    """
    Test endpoint to check cache status.
    """
    from django.core.cache import cache
    
    update_key = f"seat_updates_{schedule_id}"
    updates = cache.get(update_key, [])
    
    return JsonResponse({
        'schedule_id': schedule_id,
        'updates_count': len(updates),
        'updates': updates[-5:] if updates else [],  # Show last 5 updates
        'cache_keys': [key for key in cache._cache.keys() if f'schedule_{schedule_id}' in key] if hasattr(cache, '_cache') else []
    })


def about_us(request):
    """
    View for the About Us page.
    """
    return render(request, 'tickets/about_us.html')


def contact(request):
    """
    View for the Contact page with feedback form.
    """
    if request.method == 'POST':
        # Handle form submission
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        subject = request.POST.get('subject', '').strip()
        message = request.POST.get('message', '').strip()
        
        # Validate form data
        errors = {}
        
        if not name:
            errors['name'] = 'Пожалуйста, введите ваше имя'
        
        if not email:
            errors['email'] = 'Пожалуйста, введите ваш email'
        else:
            import re
            email_regex = r'^[^\s@]+@[^\s@]+\.[^\s@]+$'
            if not re.match(email_regex, email):
                errors['email'] = 'Пожалуйста, введите корректный email адрес'
        
        if not subject:
            errors['subject'] = 'Пожалуйста, введите тему сообщения'
        
        if not message:
            errors['message'] = 'Пожалуйста, введите сообщение'
        
        if errors:
            return render(request, 'tickets/contact.html', {
                'errors': errors,
                'form_data': {
                    'name': name,
                    'email': email,
                    'subject': subject,
                    'message': message
                }
            })
        
        # Save message to database
        try:
            from .models import ContactMessage
            
            contact_message = ContactMessage.objects.create(
                name=name,
                email=email,
                subject=subject,
                message=message,
                status='new'
            )
            
            messages.success(request, 'Ваше сообщение успешно отправлено! Мы свяжемся с вами в ближайшее время.')
            return redirect('tickets:contact')
                
        except Exception as e:
            messages.error(request, f'Произошла ошибка при сохранении сообщения: {str(e)}')
            return render(request, 'tickets/contact.html', {
                'form_data': {
                    'name': name,
                    'email': email,
                    'subject': subject,
                    'message': message
                }
            })
    
    return render(request, 'tickets/contact.html')


def broadcast_seat_update(schedule_id, seat_number, status):
    """
    Broadcast seat updates to connected clients.
    Now uses the signal system.
    """
    from .signals import seat_status_changed
    seat_status_changed.send(
        sender=Ticket,
        schedule_id=schedule_id,
        seat_number=seat_number,
        status=status,
        ticket_id=None
    )


@require_POST
def send_ticket_to_booking_email(request, booking_id):
    """
    Send ticket to booking email for anonymous users.
    """
    try:
        import json
        data = json.loads(request.body.decode('utf-8'))
        email = data.get('email')
        
        # Get booking
        booking = get_object_or_404(Booking, id=booking_id)
        
        # Verify this is an anonymous booking and email matches
        if booking.user:
            return JsonResponse({
                'success': False,
                'message': 'This booking belongs to a registered user.'
            }, status=400)
        
        if booking.email != email:
            return JsonResponse({
                'success': False,
                'message': 'Email does not match booking email.'
            }, status=400)
        
        # Check if booking is paid
        if not booking.is_paid:
            return JsonResponse({
                'success': False,
                'message': 'Email sending is only available after payment completion.'
            }, status=400)
        
        # Check email backend and provide appropriate message
        from django.conf import settings
        is_console_backend = 'console' in settings.EMAIL_BACKEND.lower()
        
        try:
            send_booking_email(booking)
            if is_console_backend:
                message = f'Email content displayed in server console for testing. Your booking reference is {booking.booking_reference}.'
            else:
                message = 'Ticket sent to your email! You can also download PDF below.'
            
            return JsonResponse({
                'success': True,
                'message': message
            })
            
        except ValueError as ve:
            return JsonResponse({
                'success': False,
                'message': f'Email error: {str(ve)}. Please check your email address.'
            }, status=400)
        except Exception as e:
            import traceback
            # print(f"Email sending error in send_ticket_to_booking_email: {str(e)}")
            # print(f"Traceback: {traceback.format_exc()}")
            
            if is_console_backend:
                message = f'Email content displayed in server console. Your booking reference is {booking.booking_reference}.'
            else:
                error_msg = str(e)
                if "authentication" in error_msg.lower():
                    message = "Email server authentication failed. Please download your PDF ticket below."
                elif "connection" in error_msg.lower():
                    message = "Cannot connect to email server. Please download your PDF ticket below."
                elif "timeout" in error_msg.lower():
                    message = "Email server timeout. Please download your PDF ticket below."
                else:
                    message = "Email sending failed. Please download your PDF ticket below."
            
            return JsonResponse({
                'success': True,  # Return success so user gets the message
                'message': message
            })
            
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'message': 'Invalid request format.'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': 'Server error. Please try again.'
        }, status=500)
