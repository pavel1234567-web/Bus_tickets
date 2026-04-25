"""
Forms for bus tickets application.

This module contains all the forms for the bus ticketing system:
- Route search form
- Booking form
- Payment form
"""

from django import forms
from django.utils import timezone
from .models import Route, Schedule


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
        
        self.fields['departure_date'] = forms.DateField(
            label='Departure date (optional)',
            required=False,
            widget=forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'min': timezone.now().date()
            })
        )
        
        # Set default date to today
        self.fields['departure_date'].initial = timezone.now().date()


class BookingForm(forms.Form):
    """
    Form for booking information.
    """
    first_name = forms.CharField(
        label='First name',
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
            'placeholder': 'Enter first name'
        })
    )
    
    last_name = forms.CharField(
        label='Last name',
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
            'placeholder': 'Enter last name'
        })
    )
    
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
            'placeholder': 'Enter email address'
        })
    )
    
    phone = forms.CharField(
        label='Phone',
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
            'placeholder': 'Enter phone number (optional)'
        })
    )


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
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
            'placeholder': '123',
            'pattern': '[0-9]{3}'
        })
    )
    
    cardholder_name = forms.CharField(
        label='Cardholder name',
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
            'placeholder': 'Ivan Ivanov'
        })
    )

    def clean(self):
        cleaned_data = super().clean()
        payment_method = cleaned_data.get('payment_method')
        
        if payment_method == 'card':
            card_number = cleaned_data.get('card_number')
            card_expiry = cleaned_data.get('card_expiry')
            card_cvv = cleaned_data.get('card_cvv')
            cardholder_name = cleaned_data.get('cardholder_name')
            
            if not all([card_number, card_expiry, card_cvv, cardholder_name]):
                raise forms.ValidationError(
                    'All credit card fields are required when selecting card payment.'
                )
        
        return cleaned_data


class GuestBookingForm(BookingForm):
    """
    Extended booking form for guest users.
    """
    agree_terms = forms.BooleanField(
        label='I agree to the booking terms',
        widget=forms.CheckboxInput(attrs={
            'class': 'w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 rounded focus:ring-blue-500'
        })
    )
    
    def clean_agree_terms(self):
        agree_terms = self.cleaned_data.get('agree_terms')
        if not agree_terms:
            raise forms.ValidationError('You must agree to the booking terms.')
        return agree_terms
