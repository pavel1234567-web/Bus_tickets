# SQL Sample Data Scripts

This directory contains SQL scripts to populate the Bus Tickets System database with realistic test data.

## Available Scripts

### Individual Table Scripts
- `01_routes_sample_data.sql` - Sample routes between Russian cities
- `02_buses_sample_data.sql` - Sample buses (standard, comfort, luxury classes)
- `03_schedules_sample_data.sql` - Sample schedules with departure times
- `04_tickets_sample_data.sql` - Sample tickets with various statuses
- `05_bookings_sample_data.sql` - Sample bookings with customer information
- `06_payments_sample_data.sql` - Sample payments with different methods and statuses

### Complete Script
- `00_all_sample_data.sql` - Complete script that populates all tables at once

## Data Overview

### Routes
- **30 realistic routes** between major Russian cities
- Includes Moscow, St. Petersburg, Kazan, Nizhny Novgorod, Sochi, etc.
- Realistic distances and travel times
- Base prices in Russian Rubles (RUB)

### Buses
- **25 buses** with different classes:
  - **Standard**: 45 seats, basic amenities
  - **Comfort**: 36 seats, AC + WiFi
  - **Luxury**: 28 seats, AC + WiFi + Toilet
- Registration numbers and descriptions

### Schedules
- **37 schedules** with various departure times
- Price multipliers for different time slots
- Active schedules for current and future dates

### Tickets
- **60+ tickets** with different statuses:
  - `available` - Ready for booking
  - `booked` - Reserved but not paid
  - `paid` - Fully paid and confirmed
- Realistic seat numbers and prices

### Bookings
- **20+ bookings** with various customer types:
  - Individual travelers
  - Business travelers
  - Students
  - Tourists
  - Corporate bookings
- Realistic customer information and contact details

### Payments
- **20+ payments** with various methods and statuses:
  - **Methods**: card, bank_transfer, cash
  - **Statuses**: completed, pending, failed, refunded
- Transaction IDs and timestamps

## Usage Instructions

### Prerequisites
1. Make sure Django project is set up
2. Run database migrations: `python manage.py migrate`
3. Database should be created and accessible

### Option 1: Complete Setup (Recommended)
```bash
# Execute the complete script
psql -d bus_tickets_db -f sql/00_all_sample_data.sql

# Or if using SQLite
sqlite3 db.sqlite3 < sql/00_all_sample_data.sql
```

### Option 2: Individual Tables
Execute scripts in order:
```bash
# 1. Routes (must be first)
psql -d bus_tickets_db -f sql/01_routes_sample_data.sql

# 2. Buses
psql -d bus_tickets_db -f sql/02_buses_sample_data.sql

# 3. Schedules
psql -d bus_tickets_db -f sql/03_schedules_sample_data.sql

# 4. Tickets
psql -d bus_tickets_db -f sql/04_tickets_sample_data.sql

# 5. Bookings
psql -d bus_tickets_db -f sql/05_bookings_sample_data.sql

# 6. Payments
psql -d bus_tickets_db -f sql/06_payments_sample_data.sql
```

### Option 3: Django Management Command
If you prefer using Django:
```bash
# Create a custom management command to load the data
python manage.py load_sample_data
```

## Sample User Accounts

The script creates sample users for testing:

| Username | Email | Password | Role |
|----------|-------|----------|------|
| admin | admin@bustickets.com | admin123 | Administrator |
| ivan_petrov | ivan.petrov@example.com | password123 | Regular user |
| maria_ivanova | maria.ivanova@example.com | password123 | Regular user |
| alexey_sidorov | alexey.sidorov@example.com | password123 | Regular user |
| anna_fedorova | anna.fedorova@example.com | password123 | Regular user |

## Testing Scenarios

The sample data supports various testing scenarios:

### 1. Search Functionality
- Multiple routes between cities
- Different departure times
- Various price ranges

### 2. Seat Selection
- Mixed availability (available, booked, paid)
- Different bus types (standard, comfort, luxury)
- Realistic seat layouts

### 3. Booking Process
- New bookings with available seats
- Payment processing
- Booking confirmations

### 4. User Management
- Login with sample accounts
- Profile management
- Booking history

### 5. Payment Testing
- Different payment methods
- Various payment statuses
- Transaction tracking

### 6. Admin Panel Testing
- Manage routes and buses
- View bookings and payments
- Generate reports

## Data Relationships

```
Routes (30) 
  -> Schedules (37) 
    -> Tickets (60+) 
      -> Bookings (20+) 
        -> Payments (20+)
```

## Important Notes

1. **Dependencies**: Scripts must be executed in order due to foreign key constraints
2. **IDs**: The scripts use specific IDs that reference each other
3. **Dates**: All timestamps use current date for realistic testing
4. **Currency**: All prices are in Russian Rubles (RUB)
5. **Phone Numbers**: Russian phone number format (+7XXXXXXXXXX)

## Customization

You can modify the scripts to:
- Add more routes and cities
- Change prices and schedules
- Add more sample users
- Modify booking scenarios
- Test edge cases

## Troubleshooting

### Common Issues

1. **Foreign Key Violations**: Make sure scripts are executed in correct order
2. **Duplicate Entries**: Clear existing data before loading new data
3. **Permission Errors**: Ensure database user has INSERT permissions

### Reset Data
To clear all sample data and start fresh:
```sql
-- Clear in reverse order due to foreign keys
DELETE FROM tickets_payment;
DELETE FROM tickets_booking_tickets;
DELETE FROM tickets_booking;
DELETE FROM tickets_ticket;
DELETE FROM tickets_schedule;
DELETE FROM tickets_bus;
DELETE FROM tickets_route;
DELETE FROM auth_user WHERE username IN ('admin', 'ivan_petrov', 'maria_ivanova', 'alexey_sidorov', 'anna_fedorova');
```

## Production Considerations

- These scripts are for **development/testing only**
- Remove sample data before production deployment
- Use proper data migration strategies for production
- Consider data privacy regulations for real customer data

## Support

For issues with the sample data:
1. Check Django logs for errors
2. Verify database connections
3. Ensure all migrations are applied
4. Check foreign key constraints

---

**Note**: This sample data is designed to provide a realistic testing environment for the Bus Tickets System. Feel free to modify it according to your specific testing needs.
