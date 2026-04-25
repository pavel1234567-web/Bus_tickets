"""
Forms for bus tickets application.

This module contains forms for:
- Route search
- Booking information
- Payment processing
- Anonymous user bookings
"""

from django import forms
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta
from .models import Route, Schedule

# Get the User model
User = get_user_model()


class SearchForm(forms.Form):
    """
    Form for searching bus routes with dropdown menus.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Get unique cities from routes
        departure_cities = Route.objects.filter(is_active=True).values_list('departure_city', flat=True).distinct().order_by('departure_city')
        arrival_cities = Route.objects.filter(is_active=True).values_list('arrival_city', flat=True).distinct().order_by('arrival_city')
        
        # Create city choices with empty option
        departure_choices = [('', '-- Select departure city --')] + [(city, city) for city in departure_cities]
        arrival_choices = [('', '-- Select arrival city --')] + [(city, city) for city in arrival_cities]
        
        self.fields['departure_city'] = forms.ChoiceField(
            label='Departure city',
            choices=departure_choices,
            widget=forms.Select(attrs={
                'class': 'form-control',
                'id': 'departure_city_select'
            })
        )
        
        self.fields['arrival_city'] = forms.ChoiceField(
            label='Arrival city',
            choices=arrival_choices,
            widget=forms.Select(attrs={
                'class': 'form-control',
                'id': 'arrival_city_select'
            })
        )
        
        # Use calendar widget for date selection
        today = timezone.now().date()
        
        self.fields['departure_date'] = forms.DateField(
            label='Departure date (optional)',
            required=False,
            widget=forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control',
                'id': 'departure_date_select',
                'min': today.strftime('%Y-%m-%d'),
                'max': (today + timezone.timedelta(days=30)).strftime('%Y-%m-%d')
            })
        )
        
        # Set default date to today
        self.fields['departure_date'].initial = today.strftime('%Y-%m-%d')


class BookingForm(forms.Form):
    """
    Form for booking information.
    """
    first_name = forms.CharField(
        label='First name',
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
            'placeholder': 'Enter your first name'
        })
    )
    
    last_name = forms.CharField(
        label='Last name',
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
            'placeholder': 'Enter your last name'
        })
    )
    
    email = forms.EmailField(
        label='Email address',
        widget=forms.EmailInput(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
            'placeholder': 'Enter your email address'
        })
    )
    
    phone = forms.CharField(
        label='Phone number (optional)',
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
            'placeholder': 'Enter phone number (optional)'
        })
    )


class AnonymousBookingForm(forms.Form):
    """
    Form for anonymous users to complete booking with email.
    """
    first_name = forms.CharField(
        label='First name',
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your first name'
        })
    )
    
    last_name = forms.CharField(
        label='Last name',
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your last name'
        })
    )
    
    email = forms.EmailField(
        label='Email address',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email address'
        })
    )
    
    phone = forms.CharField(
        label='Phone number (optional)',
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your phone number'
        })
    )


class UserProfileForm(forms.ModelForm):
    """
    Custom form for user profile updates.
    """
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'placeholder': 'Enter username'
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'placeholder': 'Enter first name'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'placeholder': 'Enter last name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'placeholder': 'Enter email address'
            })
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add labels
        self.fields['username'].label = 'Username'
        self.fields['first_name'].label = 'First name'
        self.fields['last_name'].label = 'Last name'
        self.fields['email'].label = 'Email address'


class PaymentForm(forms.Form):
    """
    Form for processing payments.
    """
    payment_method = forms.ChoiceField(
        label='Payment method',
        choices=[
            ('credit_card', 'Credit Card'),
            ('bank_transfer', 'Bank Transfer'),
            ('cash', 'Cash')
        ],
        widget=forms.RadioSelect(attrs={
            'class': 'space-y-2'
        })
    )


class CustomUserCreationForm(forms.Form):
    """
    Custom user registration form without password validation.
    """
    username = forms.CharField(
        label='Username',
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
            'placeholder': 'Enter your username'
        })
    )
    
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
            'placeholder': 'Enter your password'
        })
    )
    
    def save(self):
        from django.contrib.auth.models import User
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            password=self.cleaned_data['password']
        )
        return user
