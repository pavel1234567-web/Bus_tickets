"""
URL configuration for tickets application.

This module defines all the URL patterns for the bus ticketing system:
- Home and search pages
- Booking and payment flows
- Ticket management
- API endpoints
"""

from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views

app_name = 'tickets'

urlpatterns = [
    # Main pages
    path('', views.home, name='home'),
    path('search/', views.search_routes, name='search_routes'),
    path('alternative-dates/', views.alternative_dates, name='alternative_dates'),
    path('schedule/<int:schedule_id>/', views.schedule_detail, name='schedule_detail'),
    
    # Booking flow
    path('booking/<int:booking_id>/', views.booking_detail, name='booking_detail'),
    path('booking/<int:booking_id>/update/', views.update_booking, name='update_booking'),
    path('booking/<int:booking_id>/delete/', views.delete_booking, name='delete_booking'),
    path('booking/<int:booking_id>/download-pdf/', views.download_ticket_pdf, name='download_ticket_pdf'),
    path('booking/<int:booking_id>/send-to-user/', views.send_ticket_to_user, name='send_ticket_to_user'),
    path('booking/<int:booking_id>/send-to-custom-email/', views.send_ticket_to_custom_email, name='send_ticket_to_custom_email'),
    
    # Real-time seat updates
    path('schedule/<int:schedule_id>/seat-updates/', views.seat_updates_sse, name='seat_updates_sse'),
    path('schedule/<int:schedule_id>/trigger-update/', views.trigger_seat_update, name='trigger_seat_update'),
    path('schedule/<int:schedule_id>/test-cache/', views.test_cache_status, name='test_cache_status'),
    
    # Seat locking for concurrent selection prevention
    path('schedule/<int:schedule_id>/lock-seat/', views.lock_seat, name='lock_seat'),
    path('schedule/<int:schedule_id>/unlock-seat/', views.unlock_seat, name='unlock_seat'),
    
    # Test endpoints
    path('test-api/', views.test_api, name='test_api'),
    path('test-email/', views.test_email_config, name='test_email_config'),
    
    path('booking/<int:booking_id>/complete/', views.complete_anonymous_booking, name='complete_anonymous_booking'),
    path('booking/<int:booking_id>/confirm/', views.booking_confirmation, name='booking_confirmation'),
    path('booking/<int:booking_id>/payment/', views.process_payment, name='process_payment'),
    path('booking/<int:booking_id>/pdf/', views.download_ticket_pdf, name='download_ticket_pdf'),
    path('booking/<int:booking_id>/send-to-booking-email/', views.send_ticket_to_booking_email, name='send_ticket_to_booking_email'),
    
    # Ticket download
    path('booking/<int:booking_id>/download-pdf/', views.download_ticket_pdf, name='download_ticket_pdf'),
    
    # Authentication
    path('login/', auth_views.LoginView.as_view(template_name='tickets/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(http_method_names=['post']), name='logout'),
    path('register/', views.register, name='register'),
    
    # API endpoints
    path('api/routes/', views.RouteViewSet.as_view({'get': 'list'}), name='api_routes'),
    path('api/schedules/', views.ScheduleViewSet.as_view({'get': 'list'}), name='api_schedules'),
    path('api/schedule/<int:schedule_id>/seats/', views.check_seat_availability, name='api_check_seats'),
    
    # Ajax search endpoints
    path('api/search/routes/', views.ajax_search_routes, name='ajax_search_routes'),
    path('api/search/cities/', views.ajax_search_cities, name='ajax_search_cities'),
    
    # Seat selection
    path('seat-selection/<int:schedule_id>/', views.seat_selection, name='seat_selection'),
    path('api/seat-status/<int:schedule_id>/', views.get_seat_status, name='get_seat_status'),
    path('api/temp-booking/', views.create_temp_booking, name='create_temp_booking'),
    path('api/update-seat/<int:schedule_id>/', views.update_seat_status, name='update_seat_status'),
    
    # User profile
    path('profile/', views.user_profile, name='user_profile'),
    path('profile/bookings/', views.user_bookings, name='user_bookings'),
    
    # Static pages
    path('about/', views.about_us, name='about_us'),
    path('contact/', views.contact, name='contact'),
]
