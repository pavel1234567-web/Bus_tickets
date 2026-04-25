"""
Admin configuration for bus tickets application.

This module provides comprehensive admin interface for managing:
- Routes and bus schedules
- Bus configurations and seat layouts
- Ticket booking and management
- Payment tracking
"""

from django.contrib import admin, messages
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.utils import timezone
from datetime import timedelta
from .models import Route, Bus, Schedule, Ticket, Booking, Payment, ContactMessage, SeatLayout


@admin.register(SeatLayout)
class SeatLayoutAdmin(admin.ModelAdmin):
    """
    Admin interface for managing bus seat layouts.
    """
    list_display = ['name', 'total_seats', 'seats_per_row', 'is_active', 'created_at', 'layout_preview']
    list_filter = ['is_active', 'total_seats', 'seats_per_row', 'created_at']
    search_fields = ['name', 'description']
    list_editable = ['is_active']
    readonly_fields = ['created_at', 'updated_at', 'layout_preview', 'layout_visualization']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description', 'is_active')
        }),
        ('Configuration', {
            'fields': ('total_seats', 'seats_per_row')
        }),
        ('Layout Data', {
            'fields': ('layout_data', 'layout_visualization')
        }),
        ('Preview', {
            'fields': ('layout_preview',)
        }),
        ('System Information', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def layout_preview(self, obj):
        """Display layout preview in list view"""
        layout = obj.get_layout_display()
        if not layout:
            return "No layout"
        
        html = '<div style="font-family: monospace; font-size: 10px;">'
        max_rows_to_show = 3  # Limit rows for list view
        for i, row in enumerate(layout[:max_rows_to_show]):
            html += '<div>'
            for seat in row:
                if seat:
                    html += f'<span style="display: inline-block; width: 20px; text-align: center; border: 1px solid #ccc; margin: 1px; font-size: 9px;">{seat}</span>'
                else:
                    html += '<span style="display: inline-block; width: 20px; margin: 1px;"></span>'
            html += '</div>'
        if len(layout) > max_rows_to_show:
            html += f'<div style="font-size: 9px; color: #666;">...+{len(layout)-max_rows_to_show} rows</div>'
        html += '</div>'
        return mark_safe(html)
    
    layout_preview.short_description = 'Layout preview'

    def layout_visualization(self, obj):
        """Display detailed layout visualization"""
        layout = obj.get_layout_display()
        if not layout:
            return "No layout configured"
        
        html = '<div style="font-family: monospace; background: #f5f5f5; padding: 10px; border-radius: 5px;">'
        for row in layout:
            html += '<div style="margin-bottom: 2px;">'
            for seat in row:
                if seat:
                    html += f'<span style="display: inline-block; width: 40px; text-align: center; border: 1px solid #333; margin: 2px; background: white; font-weight: bold;">{seat}</span>'
                else:
                    html += '<span style="display: inline-block; width: 40px; margin: 2px;"></span>'
            html += '</div>'
        html += '</div>'
        return mark_safe(html)
    
    layout_visualization.short_description = 'Layout visualization'

    def save_model(self, request, obj, form, change):
        """Override save to auto-generate layout_data if not provided"""
        if not obj.layout_data or (change and 'layout_data' in form.changed_data and not obj.layout_data):
            # Auto-generate layout based on total_seats and seats_per_row
            obj.layout_data = obj.generate_default_layout()
        
        super().save_model(request, obj, form, change)


class OldUnpaidBookingFilter(admin.SimpleListFilter):
    """
    Custom filter to show unpaid bookings older than 10 minutes
    """
    title = 'статус оплаты'
    parameter_name = 'payment_age'
    
    def lookups(self, request, model_admin):
        return (
            ('old_unpaid', 'Неоплаченные (>10 мин)'),
            ('recent_unpaid', 'Неоплаченные (≤10 мин)'),
            ('all_unpaid', 'Все неоплаченные'),
        )
        
    
    def queryset(self, request, queryset):
        ten_minutes_ago = timezone.now() - timedelta(minutes=10)
        
        if self.value() == 'old_unpaid':
            return queryset.filter(is_paid=False, created_at__lt=ten_minutes_ago)
        elif self.value() == 'recent_unpaid':
            return queryset.filter(is_paid=False, created_at__gte=ten_minutes_ago)
        elif self.value() == 'all_unpaid':
            return queryset.filter(is_paid=False)
        
        return queryset


@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):
    """
    Admin interface for managing bus routes.
    """
    list_display = ['full_name', 'departure_address', 'arrival_address', 'departure_date', 'distance', 'estimated_time', 'base_price', 'is_active', 'created_at']
    list_filter = ['is_active', 'departure_city', 'arrival_city', 'departure_date']
    search_fields = ['name', 'departure_city', 'arrival_city']
    list_editable = ['is_active', 'base_price', 'departure_date']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'departure_city', 'arrival_city', 'departure_address', 'arrival_address')
        }),
        ('Schedule Information', {
            'fields': ('departure_date',)
        }),
        ('Route Details', {
            'fields': ('distance', 'estimated_time', 'base_price')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
        ('System Information', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Bus)
class BusAdmin(admin.ModelAdmin):
    """
    Admin interface for managing buses with seat layout visualization.
    """
    list_display = ['registration_number', 'bus_type', 'seat_layout_name', 'total_seats', 'seats_per_row', 'has_ac', 'has_wifi', 'has_toilet', 'is_active', 'created_at']
    list_filter = ['bus_type', 'is_active', 'has_ac', 'has_wifi', 'has_toilet', 'seat_layout_config', 'created_at']
    search_fields = ['registration_number']
    list_editable = ['is_active']
    readonly_fields = ['created_at', 'seat_layout_display']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('registration_number', 'bus_type', 'seat_layout_config')
        }),
        ('Seat Configuration', {
            'fields': ('total_seats', 'seats_per_row')
        }),
        ('Amenities', {
            'fields': ('has_ac', 'has_wifi', 'has_toilet')
        }),
        ('Description', {
            'fields': ('description',)
        }),
        ('Seat Layout Preview', {
            'fields': ('seat_layout_display',)
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
        ('System Information', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )

    def seat_layout_name(self, obj):
        """Display seat layout name"""
        if obj.seat_layout_config:
            return obj.seat_layout_config.name
        return "Default"
    seat_layout_name.short_description = 'Seat Layout'

    def seat_layout_display(self, obj):
        """Display seat layout in admin"""
        layout = obj.seat_layout
        html = '<div style="font-family: monospace;">'
        for row in layout:
            html += '<div>'
            for seat in row:
                if seat:
                    html += f'<span style="display: inline-block; width: 40px; text-align: center; border: 1px solid #ccc; margin: 2px;">{seat}</span>'
                else:
                    html += '<span style="display: inline-block; width: 40px; margin: 2px;"></span>'
            html += '</div>'
        html += '</div>'
        return mark_safe(html)
    
    seat_layout_display.short_description = 'Seat layout'


class TicketInline(admin.TabularInline):
    """
    Inline admin for tickets within schedule admin.
    """
    model = Ticket
    extra = 0
    readonly_fields = ['booking_reference', 'price', 'created_at']
    fields = ['seat_number', 'status', 'price', 'booking_reference']


@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    """
    Admin interface for managing bus schedules.
    """
    list_display = ['route', 'bus', 'departure_time', 'arrival_time', 'price_multiplier', 'current_price', 'available_seats', 'is_active', 'seat_management_actions']
    list_filter = ['is_active', 'route', 'bus', 'departure_time', 'arrival_time', 'created_at']
    search_fields = ['route__departure_city', 'route__arrival_city', 'bus__registration_number']
    list_editable = ['is_active']
    readonly_fields = ['created_at', 'current_price', 'available_seats', 'seat_status_display']
    inlines = [TicketInline]
    actions = ['release_all_booked_seats', 'mark_selected_as_paid', 'reset_all_seats']
    
    fieldsets = (
        ('Route Information', {
            'fields': ('route', 'bus')
        }),
        ('Time', {
            'fields': ('departure_time', 'arrival_time')
        }),
        ('Price', {
            'fields': ('price_multiplier', 'current_price')
        }),
        ('Seat Status', {
            'fields': ('available_seats', 'seat_status_display')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
        ('System Information', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )

    def current_price(self, obj):
        """Display current calculated price"""
        return f"{obj.current_price:.2f} PLN"
    current_price.short_description = 'Current price'

    def available_seats(self, obj):
        """Display available seats count"""
        available = obj.available_seats
        total = obj.bus.total_seats
        color = 'green' if available > 5 else 'orange' if available > 0 else 'red'
        return format_html(
            '<span style="color: {};">{}/{} seats</span>',
            color, available, total
        )
    available_seats.short_description = 'Available seats'

    def seat_status_display(self, obj):
        """Display seat status grid"""
        seat_status = obj.get_seat_status()
        html = '<div style="font-family: monospace;">'
        
        # Group seats by rows
        seats_per_row = obj.bus.seats_per_row
        seats = list(seat_status.keys())
        seats.sort()
        
        for i in range(0, len(seats), seats_per_row):
            html += '<div>'
            for j in range(seats_per_row):
                if i + j < len(seats):
                    seat_num = seats[i + j]
                    status = seat_status[seat_num]
                    
                    # Color coding for seat status
                    if status == 'available':
                        color = '#4CAF50'  # Green
                    elif status == 'booked':
                        color = '#FF9800'  # Orange
                    elif status == 'paid':
                        color = '#F44336'  # Red
                    else:
                        color = '#9E9E9E'  # Gray
                    
                    html += f'<span style="display: inline-block; width: 35px; height: 35px; text-align: center; line-height: 35px; background-color: {color}; color: white; margin: 2px; border-radius: 3px; font-size: 12px;">{seat_num}</span>'
            html += '</div>'
        html += '</div>'
        return mark_safe(html)
    
    seat_status_display.short_description = 'Seat status'
    
    def seat_management_actions(self, obj):
        """Display seat management action buttons"""
        actions_html = f'''
        <div style="display: flex; gap: 5px;">
            <a href="/seat-selection/{obj.id}/" 
               class="button" style="background: #264765; color: white; padding: 5px 10px; text-decoration: none; border-radius: 3px; font-size: 11px;" 
               target="_blank">
                <i class="fas fa-chair"></i> Manage Seats
            </a>
        </div>
        '''
        return mark_safe(actions_html)
    seat_management_actions.short_description = 'Actions'
    
    def release_all_booked_seats(self, request, queryset):
        """Release all booked seats for selected schedules"""
        updated_count = 0
        for schedule in queryset:
            booked_tickets = Ticket.objects.filter(schedule=schedule, status='booked')
            count = booked_tickets.count()
            booked_tickets.delete()
            updated_count += count
            
            # Broadcast update
            self.broadcast_seat_update(schedule.id, "all", "released")
        
        self.message_user(request, f'Released {updated_count} booked seats from {queryset.count()} schedules.', messages.SUCCESS)
    release_all_booked_seats.short_description = 'Release all booked seats'
    
    def mark_selected_as_paid(self, request, queryset):
        """Mark all booked seats as paid for selected schedules"""
        updated_count = 0
        for schedule in queryset:
            booked_tickets = Ticket.objects.filter(schedule=schedule, status='booked')
            count = booked_tickets.update(status='paid')
            updated_count += count
            
            # Broadcast update
            self.broadcast_seat_update(schedule.id, "all", "paid")
        
        self.message_user(request, f'Marked {updated_count} seats as paid for {queryset.count()} schedules.', messages.SUCCESS)
    mark_selected_as_paid.short_description = 'Mark all booked as paid'
    
    def reset_all_seats(self, request, queryset):
        """Reset all seats for selected schedules"""
        updated_count = 0
        for schedule in queryset:
            all_tickets = Ticket.objects.filter(schedule=schedule)
            count = all_tickets.count()
            all_tickets.delete()
            updated_count += count
            
            # Broadcast update
            self.broadcast_seat_update(schedule.id, "all", "reset")
        
        self.message_user(request, f'Reset {updated_count} seats for {queryset.count()} schedules.', messages.WARNING)
    reset_all_seats.short_description = 'Reset all seats (DANGER!)'
    
    def broadcast_seat_update(self, schedule_id, seat_number, action):
        """Broadcast seat update to connected clients"""
        print(f"Admin action broadcast: Schedule {schedule_id}, Seat {seat_number}, Action {action}")
        # TODO: Integrate with WebSocket/SSE for real-time updates


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    """
    Admin interface for managing individual tickets.
    """
    list_display = ['booking_reference', 'schedule', 'seat_number', 'status', 'booking_time_warning', 'price', 'updated_at', 'created_at']
    list_filter = ['status', 'schedule__route', 'schedule__departure_time', 'schedule__bus', 'created_at', 'updated_at']
    search_fields = ['booking_reference', 'schedule__route__departure_city', 'schedule__route__arrival_city']
    list_editable = ['status']
    readonly_fields = ['booking_reference', 'price', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Ticket Information', {
            'fields': ('schedule', 'seat_number', 'status')
        }),
        ('Price', {
            'fields': ('price',)
        }),
        ('Booking', {
            'fields': ('booking_reference',)
        }),
        ('System Information', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def booking_time_warning(self, obj):
        """Display warning for tickets with status 'booked' older than 10 minutes"""
        if obj.status != 'booked':
            return format_html(
                '<span style="color: green; font-weight: bold;">✓ {}</span>',
                obj.get_status_display()
            )
        else:
            # Check if ticket is booked for more than 10 minutes
            time_diff = timezone.now() - obj.created_at
            minutes_ago = time_diff.total_seconds() / 60
            
            if minutes_ago > 10:
                return format_html(
                    '<span style="color: red; font-weight: bold; background-color: #ffebee; padding: 2px 6px; border-radius: 3px;">'
                    '⚠️ Забронировано ({} мин назад)</span>',
                    int(minutes_ago)
                )
            else:
                return format_html(
                    '<span style="color: orange; font-weight: bold;">Забронировано ({} мин назад)</span>',
                    int(minutes_ago)
                )
    
    booking_time_warning.short_description = 'Время бронирования'

    def get_readonly_fields(self, request, obj=None):
        """Make booking_reference readonly when ticket is booked/paid"""
        if obj and obj.status in ['booked', 'paid']:
            return self.readonly_fields + ['booking_reference']
        return self.readonly_fields
    
    def save_model(self, request, obj, form, change):
        """
        Override save_model to broadcast seat updates when ticket status changes.
        The signal will automatically handle the broadcasting.
        """
        # Get old status if this is an update
        old_status = None
        if change:
            try:
                old_obj = Ticket.objects.get(pk=obj.pk)
                old_status = old_obj.status
            except Ticket.DoesNotExist:
                pass
        
        # Save the ticket - signal will automatically broadcast the update
        super().save_model(request, obj, form, change)
        
        # Show message if status changed
        if change and old_status != obj.status:
            messages.info(
                request, 
                f'Seat {obj.seat_number} status changed from {old_status} to {obj.status}. '
                f'Frontend users will see this update in real-time.'
            )
    
    def delete_model(self, request, obj):
        """
        Override delete_model to broadcast seat updates when ticket is deleted.
        The signal will automatically handle the broadcasting.
        """
        schedule_id = obj.schedule.id
        seat_number = obj.seat_number
        
        # Delete the ticket - signal will automatically broadcast the update
        super().delete_model(request, obj)
        
        messages.info(
            request, 
            f'Seat {seat_number} has been deleted. Frontend users will see this update in real-time.'
        )
    
    def broadcast_seat_update(self, schedule_id, seat_number, status):
        """
        Broadcast seat update to connected clients.
        """
        try:
            from .views import broadcast_seat_update
            broadcast_seat_update(schedule_id, seat_number, status)
        except Exception as e:
            # Log error but don't break admin functionality
            print(f"Error broadcasting seat update: {e}")


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    """
    Admin interface for managing customer bookings.
    """
    list_display = ['booking_reference', 'passenger_name_display', 'email', 'phone', 'route_info', 'created_at', 'is_paid', 'payment_status_with_warning', 'total_price']
    list_filter = ['is_paid', 'created_at', 'updated_at', OldUnpaidBookingFilter]
    search_fields = ['booking_reference', 'first_name', 'last_name', 'email']
    list_editable = ['is_paid']
    readonly_fields = ['booking_reference', 'total_price', 'created_at', 'ticket_info_display']
    actions = ['cancel_old_unpaid_bookings']
    
    def get_queryset(self, request):
        """Optimize queries to prevent duplication"""
        qs = super().get_queryset(request)
        qs = qs.select_related('user').prefetch_related('tickets__schedule__route')
        return qs
    
    fieldsets = (
        ('Customer Information', {
            'fields': ('user', 'first_name', 'last_name', 'email', 'phone')
        }),
        ('Booking Information', {
            'fields': ('booking_reference', 'total_price', 'is_paid')
        }),
        ('Ticket Details', {
            'fields': ('ticket_info_display',)
        }),
        ('System Information', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )

    def payment_status_with_warning(self, obj):
        """Display payment status with warning for unpaid bookings older than 10 minutes"""
        if obj.is_paid:
            return format_html(
                '<span style="color: green; font-weight: bold;">✓ Оплачено</span>'
            )
        else:
            # Check if booking is older than 10 minutes
            time_diff = timezone.now() - obj.created_at
            minutes_ago = time_diff.total_seconds() / 60
            
            if minutes_ago > 10:
                return format_html(
                    '<span style="color: red; font-weight: bold; background-color: #ffebee; padding: 2px 6px; border-radius: 3px;">'
                    '⚠️ Не оплачено ({} мин назад)</span>',
                    int(minutes_ago)
                )
            else:
                return format_html(
                    '<span style="color: orange; font-weight: bold;">Ожидание оплаты ({} мин назад)</span>',
                    int(minutes_ago)
                )
    
    payment_status_with_warning.short_description = 'Статус оплаты'

    def changelist_view(self, request, extra_context=None):
        """Override changelist_view to add warning about unpaid bookings older than 10 minutes"""
        # Count unpaid bookings older than 10 minutes
        ten_minutes_ago = timezone.now() - timedelta(minutes=10)
        unpaid_old_bookings = Booking.objects.filter(
            is_paid=False,
            created_at__lt=ten_minutes_ago
        ).count()
        
        if unpaid_old_bookings > 0:
            messages.warning(
                request,
                f'⚠️ Внимание: {unpaid_old_bookings} неоплаченных бронирований старше 10 минут! '
                f'Эти бронирования могут быть автоматически отменены.'
            )
        
        return super().changelist_view(request, extra_context)

    def cancel_old_unpaid_bookings(self, request, queryset):
        """Cancel unpaid bookings older than 10 minutes"""
        ten_minutes_ago = timezone.now() - timedelta(minutes=10)
        old_unpaid_bookings = queryset.filter(
            is_paid=False,
            created_at__lt=ten_minutes_ago
        )
        
        cancelled_count = 0
        for booking in old_unpaid_bookings:
            # Get tickets to release seats
            tickets = booking.tickets.all()
            for ticket in tickets:
                # Broadcast seat release
                try:
                    from .views import broadcast_seat_update
                    broadcast_seat_update(ticket.schedule.id, ticket.seat_number, "available")
                except Exception as e:
                    print(f"Error broadcasting seat update: {e}")
            
            # Delete tickets
            tickets.delete()
            cancelled_count += 1
        
        # Delete the bookings
        old_unpaid_bookings.delete()
        
        if cancelled_count > 0:
            self.message_user(
                request,
                f'✅ Отменено {cancelled_count} неоплаченных бронирований старше 10 минут. '
                f'Места освобождены для других пассажиров.',
                messages.SUCCESS
            )
        else:
            self.message_user(
                request,
                'ℹ️ Нет неоплаченных бронирований старше 10 минут для отмены.',
                messages.INFO
            )
    
    cancel_old_unpaid_bookings.short_description = '❌ Отменить неоплаченные бронирования (>10 мин)'

    def passenger_name_display(self, obj):
        """Display passenger name"""
        return obj.passenger_name or '-'
    passenger_name_display.short_description = 'Пассажир'

    def route_info(self, obj):
        """Display route information from first ticket"""
        first_ticket = obj.tickets.first()
        if first_ticket and first_ticket.schedule:
            return format_html(
                '{} → {}<br><small>Рейс: {}</small>',
                first_ticket.schedule.route.departure_city,
                first_ticket.schedule.route.arrival_city,
                first_ticket.schedule.departure_time.strftime('%H:%M') if first_ticket.schedule.departure_time else '-'
            )
        return '-'
    route_info.short_description = 'Маршрут'

    def ticket_info_display(self, obj):
        """Display detailed ticket information"""
        tickets_info = obj.get_ticket_info()
        html = '<div style="max-width: 600px;">'
        
        for i, ticket in enumerate(tickets_info, 1):
            html += f'''
            <div style="border: 1px solid #ddd; padding: 10px; margin-bottom: 10px; border-radius: 5px;">
                <h4 style="margin: 0 0 10px 0;">Билет {i}</h4>
                <p style="margin: 5px 0;"><strong>Маршрут:</strong> {ticket['route']}</p>
                <p style="margin: 5px 0;"><strong>Отправление:</strong> {ticket['departure_time'].strftime('%d.%m.%Y %H:%M')}</p>
                <p style="margin: 5px 0;"><strong>Прибытие:</strong> {ticket['arrival_time'].strftime('%d.%m.%Y %H:%M')}</p>
                <p style="margin: 5px 0;"><strong>Место:</strong> {ticket['seat_number']}</p>
                <p style="margin: 5px 0;"><strong>Цена:</strong> {ticket['price']:.2f} руб.</p>
                <p style="margin: 5px 0;"><strong>Статус:</strong> {ticket['status']}</p>
            </div>
            '''
        
        html += '</div>'
        return mark_safe(html)
    
    ticket_info_display.short_description = 'Детали билетов'


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    """
    Admin interface for managing payments.
    """
    list_display = ['booking', 'amount', 'payment_method', 'status', 'transaction_id', 'updated_at', 'created_at']
    list_filter = ['status', 'payment_method', 'created_at', 'updated_at']
    search_fields = ['booking__booking_reference', 'transaction_id']
    list_editable = ['status']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Payment Information', {
            'fields': ('booking', 'amount', 'payment_method', 'status')
        }),
        ('Transaction', {
            'fields': ('transaction_id',)
        }),
        ('System Information', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def get_queryset(self, request):
        """Optimize queries for better performance"""
        return super().get_queryset(request).select_related('booking')


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    """
    Admin interface for managing contact form messages.
    """
    list_display = ('name', 'email', 'subject', 'status', 'created_at', 'is_new_badge')
    list_filter = ('status', 'created_at')
    search_fields = ('name', 'email', 'subject', 'message')
    list_per_page = 20
    ordering = ('-created_at',)
    
    fieldsets = (
        ('Информация о сообщении', {
            'fields': ('name', 'email', 'subject', 'message')
        }),
        ('Управление статусом', {
            'fields': ('status', 'admin_notes')
        }),
        ('Системная информация', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ('created_at', 'updated_at')
    
    actions = ['mark_as_in_progress', 'mark_as_answered', 'mark_as_closed']
    
    # Use custom template to avoid Grappelli conflicts
    change_list_template = 'admin/tickets/contactmessage/change_list.html'
    
    def changelist_view(self, request, extra_context=None):
        """
        Override changelist_view to add custom context without Grappelli conflicts.
        """
        extra_context = extra_context or {}
        # Count new messages
        new_count = ContactMessage.objects.filter(status='new').count()
        extra_context['new_messages_count'] = new_count
        return super().changelist_view(request, extra_context)
    
    def is_new_badge(self, obj):
        """Display badge for new messages"""
        if obj.is_new:
            return format_html(
                '<span style="background-color: #ff4757; color: white; padding: 3px 8px; border-radius: 12px; font-size: 11px; font-weight: bold;">НОВОЕ</span>'
            )
        return ''
    is_new_badge.short_description = 'Статус'
    
    def mark_as_in_progress(self, request, queryset):
        """Mark selected messages as in progress"""
        updated = queryset.update(status='in_progress')
        self.message_user(request, f'{updated} сообщений отмечены как "В обработке".')
    mark_as_in_progress.short_description = 'Отметить как "В обработке"'
    
    def mark_as_answered(self, request, queryset):
        """Mark selected messages as answered"""
        updated = queryset.update(status='answered')
        self.message_user(request, f'{updated} сообщений отмечены как "Отвечено".')
    mark_as_answered.short_description = 'Отметить как "Отвечено"'
    
    def mark_as_closed(self, request, queryset):
        """Mark selected messages as closed"""
        updated = queryset.update(status='closed')
        self.message_user(request, f'{updated} сообщений отмечены как "Закрыто".')
    mark_as_closed.short_description = 'Отметить как "Закрыто"'
    
    def get_queryset(self, request):
        """Optimize queries and show new messages first"""
        qs = super().get_queryset(request)
        return qs.order_by('-created_at')


# Customize admin site
admin.site.site_header = "Система Билетов на Автобус"
admin.site.site_title = "Панель Администратора"
admin.site.index_title = "Управление Системой Билетов на Автобус" 
