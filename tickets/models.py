"""
Models for bus tickets application.

This module contains all the data models for the bus ticketing system:
- Route: Bus routes with departure and arrival cities
- Bus: Bus information with seating layout
- Schedule: Bus schedules for specific routes
- Ticket: Individual tickets with seat numbers
- Booking: Customer booking information
- Payment: Payment information and status
"""

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import uuid


class SeatLayout(models.Model):
    """
    Model representing bus seat layout configuration.
    """
    name = models.CharField(max_length=100, verbose_name="Layout name")
    description = models.TextField(blank=True, verbose_name="Description")
    total_seats = models.PositiveIntegerField(verbose_name="Total seats")
    seats_per_row = models.PositiveIntegerField(default=4, verbose_name="Seats per row")
    layout_data = models.JSONField(null=True, blank=True, verbose_name="Layout data", help_text="2D array representing seat layout")
    is_active = models.BooleanField(default=True, verbose_name="Active")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Seat Layout"
        verbose_name_plural = "Seat Layouts"
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.total_seats} seats)"

    def get_layout_display(self):
        """Get layout data for display"""
        if self.layout_data:
            return self.layout_data
        else:
            # Generate default layout if no data provided
            return self.generate_default_layout()

    def generate_default_layout(self):
        """Generate default layout based on total seats and seats per row"""
        # Handle None values for new objects
        total_seats = self.total_seats or 40  # Default to 40 seats
        seats_per_row = self.seats_per_row or 4  # Default to 4 seats per row
        
        layout = []
        rows = (total_seats + seats_per_row - 1) // seats_per_row
        seat_num = 1
        
        for row in range(1, rows + 1):
            row_seats = []
            for col in range(seats_per_row):
                if seat_num <= total_seats:
                    row_seats.append(seat_num)
                    seat_num += 1
                else:
                    row_seats.append(None)
            layout.append(row_seats)
        
        return layout


class Route(models.Model):
    """
    Model representing a bus route between two cities.
    """
    name = models.CharField(max_length=200, verbose_name="Route name")
    departure_city = models.CharField(max_length=100, verbose_name="Departure city")
    arrival_city = models.CharField(max_length=100, verbose_name="Arrival city")
    departure_address = models.CharField(max_length=200, default="Main Bus Station", verbose_name="Departure address")
    arrival_address = models.CharField(max_length=200, default="Main Bus Station", verbose_name="Arrival address")
    departure_date = models.DateField(verbose_name="Departure date", help_text="Date when this route operates", null=True, blank=True)
    distance = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="Distance (km)")
    estimated_time = models.DurationField(verbose_name="Estimated travel time")
    base_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Base price")
    is_active = models.BooleanField(default=True, verbose_name="Active")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Route"
        verbose_name_plural = "Routes"
        ordering = ['departure_city', 'arrival_city']

    def __str__(self):
        return f"{self.departure_city} - {self.arrival_city}"

    @property
    def full_name(self):
        """Return full route name with cities"""
        return f"{self.departure_city} - {self.arrival_city}"


class Bus(models.Model):
    """
    Model representing a bus with seating configuration.
    """
    BUS_TYPES = [
        ('standard', 'Standard'),
        ('comfort', 'Comfort'),
        ('luxury', 'Luxury'),
    ]

    registration_number = models.CharField(max_length=20, unique=True, verbose_name="Registration number")
    bus_type = models.CharField(max_length=20, choices=BUS_TYPES, verbose_name="Bus type")
    seat_layout_config = models.ForeignKey(SeatLayout, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Seat layout")
    total_seats = models.PositiveIntegerField(verbose_name="Total seats")
    seats_per_row = models.PositiveIntegerField(default=4, verbose_name="Seats per row")
    has_ac = models.BooleanField(default=True, verbose_name="Air conditioning")
    has_wifi = models.BooleanField(default=False, verbose_name="WiFi")
    has_toilet = models.BooleanField(default=False, verbose_name="Toilet")
    description = models.TextField(blank=True, verbose_name="Description")
    is_active = models.BooleanField(default=True, verbose_name="Active")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Bus"
        verbose_name_plural = "Buses"
        ordering = ['registration_number']

    def __str__(self):
        return f"{self.registration_number} ({self.get_bus_type_display()})"

    @property
    def seat_layout(self):
        """Get seat layout for the bus"""
        if self.seat_layout_config:
            return self.seat_layout_config.get_layout_display()
        else:
            # Generate default layout if no custom layout is assigned
            # Handle None values for new objects
            total_seats = self.total_seats or 40  # Default to 40 seats
            seats_per_row = self.seats_per_row or 4  # Default to 4 seats per row
            
            layout = []
            rows = (total_seats + seats_per_row - 1) // seats_per_row
            seat_num = 1
            
            for row in range(1, rows + 1):
                row_seats = []
                for col in range(seats_per_row):
                    if seat_num <= total_seats:
                        row_seats.append(seat_num)
                        seat_num += 1
                    else:
                        row_seats.append(None)
                layout.append(row_seats)
            
            return layout


class Schedule(models.Model):
    """
    Model representing bus schedules for specific routes.
    """
    route = models.ForeignKey(Route, on_delete=models.CASCADE, verbose_name="Route")
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE, verbose_name="Bus")
    departure_time = models.DateTimeField(verbose_name="Departure time")
    arrival_time = models.DateTimeField(verbose_name="Arrival time")
    price_multiplier = models.DecimalField(max_digits=3, decimal_places=2, default=1.0, 
                                         verbose_name="Price multiplier")
    is_active = models.BooleanField(default=True, verbose_name="Active")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Schedule"
        verbose_name_plural = "Schedules"
        ordering = ['departure_time']

    def __str__(self):
        return f"{self.route} - {self.departure_time.strftime('%d.%m.%Y %H:%M')}"

    @property
    def current_price(self):
        """Calculate current price based on base price and multiplier"""
        return self.route.base_price * self.price_multiplier

    @property
    def available_seats(self):
        """Get number of available seats"""
        total_seats = self.bus.total_seats
        booked_seats = Ticket.objects.filter(
            schedule=self, 
            status__in=['booked', 'paid']
        ).count()
        return total_seats - booked_seats

    def get_seat_status(self):
        """Get status of all seats in the bus"""
        seats = {}
        for seat_num in range(1, self.bus.total_seats + 1):
            try:
                ticket = Ticket.objects.get(schedule=self, seat_number=seat_num)
                seats[seat_num] = ticket.status
            except Ticket.DoesNotExist:
                seats[seat_num] = 'available'
        return seats


class Ticket(models.Model):
    """
    Model representing individual tickets.
    """
    TICKET_STATUS = [
        ('available', 'Available'),
        ('booked', 'Booked'),
        ('paid', 'Paid'),
        ('cancelled', 'Cancelled'),
    ]

    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE, verbose_name="Schedule")
    seat_number = models.PositiveIntegerField(verbose_name="Seat number")
    status = models.CharField(max_length=20, choices=TICKET_STATUS, default='available', 
                            verbose_name="Status")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Price")
    booking_reference = models.CharField(max_length=50, unique=True, null=True, blank=True,
                                      verbose_name="Booking reference")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Ticket"
        verbose_name_plural = "Tickets"
        unique_together = ['schedule', 'seat_number']
        ordering = ['schedule', 'seat_number']

    def __str__(self):
        return f"Bilet {self.booking_reference or f'Miejsce {self.seat_number}'}"

    def save(self, *args, **kwargs):
        """Override save to generate booking reference and set price"""
        if not self.booking_reference and self.status in ['booked', 'paid']:
            self.booking_reference = self.generate_booking_reference()
        
        if not self.price:
            self.price = self.schedule.current_price
        
        super().save(*args, **kwargs)

    @staticmethod
    def generate_booking_reference():
        """Generate unique booking reference"""
        while True:
            ref = f"BT{uuid.uuid4().hex[:8].upper()}"
            if not Ticket.objects.filter(booking_reference=ref).exists():
                return ref


class Booking(models.Model):
    """
    Model representing customer booking information.
    """
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, 
                           verbose_name="User")
    first_name = models.CharField(max_length=50, verbose_name="First name")
    last_name = models.CharField(max_length=50, verbose_name="Last name")
    email = models.EmailField(verbose_name="Email")
    phone = models.CharField(max_length=20, verbose_name="Phone")
    tickets = models.ManyToManyField(Ticket, verbose_name="Tickets")
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Total price")
    booking_reference = models.CharField(max_length=50, unique=True, verbose_name="Booking reference")
    is_paid = models.BooleanField(default=False, verbose_name="Paid")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Booking"
        verbose_name_plural = "Bookings"
        ordering = ['-created_at']

    def __str__(self):
        return f"Rezerwacja {self.booking_reference}"

    def save(self, *args, **kwargs):
        """Override save to generate booking reference"""
        if not self.booking_reference:
            self.booking_reference = self.generate_booking_reference()
        
        super().save(*args, **kwargs)
    
    def clean(self):
        """Custom validation for booking"""
        from django.core.exceptions import ValidationError
        # Проверяем наличие билетов только при обновлении, не при создании
        if self.pk and not self.tickets.exists():
            raise ValidationError("Booking must have at least one ticket")

    @staticmethod
    def generate_booking_reference():
        """Generate unique booking reference"""
        while True:
            ref = f"BR{uuid.uuid4().hex[:8].upper()}"
            if not Booking.objects.filter(booking_reference=ref).exists():
                return ref

    @property
    def passenger_name(self):
        """Get full passenger name"""
        return f"{self.first_name} {self.last_name}"

    def get_ticket_info(self):
        """Get detailed ticket information"""
        tickets_info = []
        for ticket in self.tickets.all():
            tickets_info.append({
                'route': ticket.schedule.route.full_name,
                'departure_time': ticket.schedule.departure_time,
                'arrival_time': ticket.schedule.arrival_time,
                'seat_number': ticket.seat_number,
                'price': ticket.price,
                'status': ticket.get_status_display()
            })
        return tickets_info


class Payment(models.Model):
    """
    Model representing payment information.
    """
    PAYMENT_STATUS = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    ]

    PAYMENT_METHOD = [
        ('card', 'Credit card'),
        ('bank_transfer', 'Bank transfer'),
        ('cash', 'Cash'),
        ('lipay', 'LiPay'),
        ('paypal', 'PayPal'),
    ]

    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, verbose_name="Booking")
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Amount")
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD, verbose_name="Payment method")
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default='pending', 
                           verbose_name="Payment status")
    transaction_id = models.CharField(max_length=100, blank=True, verbose_name="Transaction ID")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Payment"
        verbose_name_plural = "Payments"
        ordering = ['-created_at']

    def __str__(self):
        return f"Payment {self.id} - {self.amount} RUB"


class PassengerInfo(models.Model):
    """
    Model representing detailed passenger information.
    """
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, verbose_name="Booking")
    first_name = models.CharField(max_length=50, verbose_name="First name")
    last_name = models.CharField(max_length=50, verbose_name="Last name")
    email = models.EmailField(verbose_name="Email")
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name="Phone")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Passenger Information"
        verbose_name_plural = "Passenger Information"

    def __str__(self):
        return f"Passenger: {self.first_name} {self.last_name}"


class ContactMessage(models.Model):
    """
    Model representing contact form messages from users.
    """
    STATUS_CHOICES = [
        ('new', 'Новое'),
        ('in_progress', 'В обработке'),
        ('answered', 'Отвечено'),
        ('closed', 'Закрыто'),
    ]
    
    name = models.CharField(max_length=100, verbose_name="Имя")
    email = models.EmailField(verbose_name="Email")
    subject = models.CharField(max_length=200, verbose_name="Тема")
    message = models.TextField(verbose_name="Сообщение")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new', verbose_name="Статус")
    admin_notes = models.TextField(blank=True, null=True, verbose_name="Заметки администратора")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    
    class Meta:
        verbose_name = "Сообщение обратной связи"
        verbose_name_plural = "Сообщения обратной связи"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Сообщение от {self.name} - {self.subject[:50]}"
    
    @property
    def is_new(self):
        """Check if message is new"""
        return self.status == 'new'
    
    @property
    def short_message(self):
        """Return shortened version of message"""
        return self.message[:100] + "..." if len(self.message) > 100 else self.message
