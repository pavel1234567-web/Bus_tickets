# Bus Tickets - Django Application

Modern system for booking bus tickets built in Django with PostgreSQL, with an admin interface for managing all aspects of the system.

## Features

### For passengers:
- **Route search** by departure and arrival cities
- **Seat selection** with interactive bus layout
- **Online booking** with instant confirmation
- **Online payments** (credit card, bank transfer)
- **PDF tickets** for download and printing
- **Email with ticket** after completed payment
- **Booking history** for logged-in users

### For administrators:
- **Route management** (cities, prices, travel time)
- **Bus configuration** (seat count, layout, amenities)
- **Bus schedules** with flexible management
- **Ticket statuses** (available, booked, sold)
- **Booking management** with cancellation options
- **Payment reports** and statistics
- **Seat visualization** in buses

## Technologies

- **Backend**: Django 5.0.6
- **Database**: PostgreSQL
- **Frontend**: Tailwind CSS
- **API**: Django REST Framework
- **PDF**: ReportLab
- **Email**: Django Email Backend

## Installation

### 1. Clone repository
```bash
git clone <repository-url>
cd bus_tickets
```

### 2. Virtual environment
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure PostgreSQL database
```sql
CREATE DATABASE bus_tickets_db;
CREATE USER bus_tickets_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE bus_tickets_db TO bus_tickets_user;
```

### 5. Configure environment variables
```bash
cp .env.example .env
```
Edit the `.env` file and set appropriate values:
- `SECRET_KEY` - Django key
- `DB_*` - PostgreSQL access data
- `EMAIL_*` - email configuration (optional)

### 6. Database migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 7. Create superuser
```bash
python manage.py createsuperuser
```

### 8. Run development server
```bash
python manage.py runserver
```

The application will be available at `http://localhost:8000`

## Admin Panel

The admin panel is available at `http://localhost:8000/admin/`

Log in with superuser credentials to manage:
- Bus routes
- Buses and their configuration
- Bus schedules
- Bookings and payments

## Project Structure

```
bus_tickets/
 manage.py
 bus_tickets/
   __init__.py
   settings.py
   urls.py
   wsgi.py
   asgi.py
 tickets/
   __init__.py
   admin.py          # Admin panel configuration
   apps.py           # Application configuration
   forms.py          # Forms
   models.py         # Data models
   urls.py           # URL configuration
   views.py          # Views and business logic
 templates/
   base.html         # Main template
   tickets/
     home.html       # Home page
     search_results.html  # Search results
     schedule_detail.html  # Seat selection
     booking_detail.html   # Booking details
     booking_confirmation.html  # Confirmation
 static/
   # Static files (CSS, JS, images)
 media/
   # Media files (bus photos, etc.)
```

## Data Models

### Route
- Departure and arrival cities
- Distance and estimated time
- Base price

### Bus
- Registration number and type
- Seat count and seat layout
- Amenities (air conditioning, WiFi, toilet)

### Schedule
- Route and bus
- Departure/arrival times
- Price multiplier

### Ticket
- Schedule and seat number
- Status (available/booked/sold)
- Price and booking reference

### Booking
- Customer data
- Associated tickets
- Payment status

### Payment
- Payment method and status
- Amount and transaction ID

## API

The system provides REST API for:
- Route search (`/api/routes/`)
- Schedules (`/api/schedules/`)
- Checking seat availability (`/api/schedule/{id}/seats/`)

## Email and PDF

- **Email**: Automatic sending of booking confirmations
- **PDF**: Ticket generation in PDF format for download
- **Templates**: Fully configurable email and PDF templates

## Deployment

### Production
1. Set `DEBUG=False`
2. Configure `ALLOWED_HOSTS`
3. Set correct `SECRET_KEY`
4. Configure production server (Gunicorn + Nginx)
5. Set up PostgreSQL database
6. Configure static files and media

### Docker (optional)
```dockerfile
# Example Dockerfile
FROM python:3.11
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
```

## Technical Support

- **Django Documentation**: https://docs.djangoproject.com/
- **Tailwind CSS**: https://tailwindcss.com/
- **PostgreSQL**: https://www.postgresql.org/docs/

## License

MIT License

## Author

System created using Django 5.0.6 with modern web technologies.
