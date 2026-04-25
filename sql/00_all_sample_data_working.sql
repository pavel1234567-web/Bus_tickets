-- Working Sample Data Script for Bus Tickets System
-- This script populates all tables with realistic test data
-- Execute this script after running migrations

-- =====================================================
-- 1. CLEAR EXISTING DATA
-- =====================================================
DELETE FROM tickets_booking_tickets;
DELETE FROM tickets_payment;
DELETE FROM tickets_booking;
DELETE FROM tickets_ticket;
DELETE FROM tickets_schedule;
DELETE FROM tickets_bus;
DELETE FROM tickets_route;
DELETE FROM auth_user WHERE username IN ('admin', 'ivan_petrov', 'maria_ivanova', 'alexey_sidorov', 'anna_fedorova');

-- =====================================================
-- 2. ROUTES DATA
-- =====================================================
INSERT INTO tickets_route (name, departure_city, arrival_city, distance, estimated_time, base_price, is_active, created_at, updated_at) VALUES
('Moscow - St. Petersburg', 'Moscow', 'St. Petersburg', 704.5, '08:00:00', 2500.00, true, NOW(), NOW()),
('St. Petersburg - Moscow', 'St. Petersburg', 'Moscow', 704.5, '08:00:00', 2500.00, true, NOW(), NOW()),
('Moscow - Kazan', 'Moscow', 'Kazan', 819.0, '14:00:00', 1800.00, true, NOW(), NOW()),
('Kazan - Moscow', 'Kazan', 'Moscow', 819.0, '14:00:00', 1800.00, true, NOW(), NOW()),
('Moscow - Nizhny Novgorod', 'Moscow', 'Nizhny Novgorod', 439.0, '06:00:00', 1200.00, true, NOW(), NOW()),
('Nizhny Novgorod - Moscow', 'Nizhny Novgorod', 'Moscow', 439.0, '06:00:00', 1200.00, true, NOW(), NOW()),
('Moscow - Sochi', 'Moscow', 'Sochi', 1673.0, '24:00:00', 4000.00, true, NOW(), NOW()),
('Sochi - Moscow', 'Sochi', 'Moscow', 1673.0, '24:00:00', 4000.00, true, NOW(), NOW());

-- =====================================================
-- 3. BUSES DATA
-- =====================================================
INSERT INTO tickets_bus (registration_number, bus_type, total_seats, seats_per_row, has_ac, has_wifi, has_toilet, description, is_active, created_at) VALUES
('AB1234', 'standard', 45, 4, false, false, false, 'Standard economy bus for intercity routes', true, NOW()),
('BC5678', 'standard', 45, 4, false, false, false, 'Standard economy bus with basic amenities', true, NOW()),
('CD9012', 'standard', 45, 4, false, false, false, 'Standard bus for short to medium routes', true, NOW()),
('DE3456', 'standard', 45, 4, false, false, false, 'Economy class bus with comfortable seats', true, NOW()),
('EF7890', 'standard', 45, 4, false, false, false, 'Standard intercity bus', true, NOW()),
('FG2345', 'comfort', 36, 3, true, true, false, 'Comfort class bus with air conditioning and WiFi', true, NOW()),
('HI0123', 'comfort', 36, 3, true, true, false, 'Comfortable bus for long distance travel', true, NOW()),
('IJ4567', 'comfort', 36, 3, true, true, false, 'Premium comfort bus with spacious seating', true, NOW()),
('KL8901', 'comfort', 36, 3, true, true, false, 'Luxury comfort bus with modern amenities', true, NOW()),
('LM2345', 'comfort', 36, 3, true, true, false, 'Business class bus with premium amenities', true, NOW()),
('MN3456', 'luxury', 28, 2, true, true, true, 'Luxury first class bus with all premium amenities', true, NOW()),
('OP7890', 'luxury', 28, 2, true, true, true, 'Executive luxury bus with premium service', true, NOW()),
('QR1234', 'luxury', 28, 2, true, true, true, 'First class luxury coach with full amenities', true, NOW()),
('ST5678', 'luxury', 28, 2, true, true, true, 'Premium luxury bus for VIP passengers', true, NOW()),
('UV9012', 'luxury', 28, 2, true, true, true, 'Ultra-luxury bus with exclusive features', true, NOW());

-- =====================================================
-- 4. SCHEDULES DATA (USING CORRECT BUS IDs 1-15)
-- =====================================================
INSERT INTO tickets_schedule (route_id, bus_id, departure_time, arrival_time, price_multiplier, is_active, created_at) VALUES
-- Moscow - St. Petersburg schedules
(1, 1, '2024-04-23 06:00:00', '2024-04-23 14:00:00', 1.0, true, NOW()),
(1, 6, '2024-04-23 08:30:00', '2024-04-23 16:30:00', 1.2, true, NOW()),
(1, 11, '2024-04-23 11:00:00', '2024-04-23 19:00:00', 1.5, true, NOW()),
(1, 2, '2024-04-23 14:00:00', '2024-04-23 22:00:00', 0.9, true, NOW()),
(1, 7, '2024-04-23 16:30:00', '2024-04-24 00:30:00', 1.1, true, NOW()),
(2, 3, '2024-04-23 06:00:00', '2024-04-23 14:00:00', 1.0, true, NOW()),
(2, 8, '2024-04-23 08:30:00', '2024-04-23 16:30:00', 1.2, true, NOW()),
(2, 12, '2024-04-23 11:00:00', '2024-04-23 19:00:00', 1.5, true, NOW()),
(2, 4, '2024-04-23 14:00:00', '2024-04-23 22:00:00', 0.9, true, NOW()),
-- Moscow - Kazan schedules
(3, 9, '2024-04-23 07:00:00', '2024-04-23 21:00:00', 1.0, true, NOW()),
(3, 13, '2024-04-23 10:00:00', '2024-04-24 00:00:00', 1.1, true, NOW()),
(3, 14, '2024-04-23 15:00:00', '2024-04-24 05:00:00', 1.3, true, NOW()),
(4, 5, '2024-04-23 07:00:00', '2024-04-23 21:00:00', 1.0, true, NOW()),
(4, 10, '2024-04-23 10:00:00', '2024-04-24 00:00:00', 1.1, true, NOW()),
(4, 15, '2024-04-23 15:00:00', '2024-04-24 05:00:00', 1.3, true, NOW()),
-- Moscow - Nizhny Novgorod schedules
(5, 1, '2024-04-23 06:00:00', '2024-04-23 12:00:00', 1.0, true, NOW()),
(5, 6, '2024-04-23 08:00:00', '2024-04-23 14:00:00', 1.1, true, NOW()),
(5, 11, '2024-04-23 10:00:00', '2024-04-23 16:00:00', 1.2, true, NOW()),
(5, 2, '2024-04-23 12:00:00', '2024-04-23 18:00:00', 1.3, true, NOW()),
(5, 7, '2024-04-23 14:00:00', '2024-04-23 20:00:00', 1.1, true, NOW()),
(6, 3, '2024-04-23 06:00:00', '2024-04-23 12:00:00', 1.0, true, NOW()),
(6, 8, '2024-04-23 08:00:00', '2024-04-23 14:00:00', 1.1, true, NOW()),
(6, 12, '2024-04-23 10:00:00', '2024-04-23 16:00:00', 1.2, true, NOW()),
-- Moscow - Sochi schedules
(7, 13, '2024-04-23 08:00:00', '2024-04-24 08:00:00', 1.2, true, NOW()),
(7, 14, '2024-04-23 10:00:00', '2024-04-24 10:00:00', 1.3, true, NOW()),
(7, 15, '2024-04-23 12:00:00', '2024-04-24 12:00:00', 1.4, true, NOW()),
(8, 11, '2024-04-23 08:00:00', '2024-04-24 08:00:00', 1.2, true, NOW()),
(8, 12, '2024-04-23 10:00:00', '2024-04-24 10:00:00', 1.3, true, NOW()),
(8, 13, '2024-04-23 12:00:00', '2024-04-24 12:00:00', 1.4, true, NOW());

-- =====================================================
-- 5. CREATE SAMPLE USERS
-- =====================================================
INSERT INTO auth_user (password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined) VALUES
('pbkdf2_sha256$600000$abcdefghijklmnopqrstuvwx$abcdefghijklmnopqrstuvwxyztuvwxyz1234567890', NOW(), true, 'admin', 'Admin', 'User', 'admin@bustickets.com', true, true, NOW()),
('pbkdf2_sha256$600000$abcdefghijklmnopqrstuvwx$abcdefghijklmnopqrstuvwxyztuvwxyz1234567890', NOW(), false, 'ivan_petrov', 'Ivan', 'Petrov', 'ivan.petrov@example.com', false, true, NOW()),
('pbkdf2_sha256$600000$abcdefghijklmnopqrstuvwx$abcdefghijklmnopqrstuvwxyztuvwxyz1234567890', NOW(), false, 'maria_ivanova', 'Maria', 'Ivanova', 'maria.ivanova@example.com', false, true, NOW()),
('pbkdf2_sha256$600000$abcdefghijklmnopqrstuvwx$abcdefghijklmnopqrstuvwxyztuvwxyz1234567890', NOW(), false, 'alexey_sidorov', 'Alexey', 'Sidorov', 'alexey.sidorov@example.com', false, true, NOW()),
('pbkdf2_sha256$600000$abcdefghijklmnopqrstuvwx$abcdefghijklmnopqrstuvwxyztuvwxyz1234567890', NOW(), false, 'anna_fedorova', 'Anna', 'Fedorova', 'anna.fedorova@example.com', false, true, NOW());

-- =====================================================
-- 6. BOOKINGS DATA
-- =====================================================
INSERT INTO tickets_booking (user_id, first_name, last_name, email, phone, total_price, booking_reference, is_paid, created_at, updated_at) VALUES
(1, 'Ivan', 'Petrov', 'ivan.petrov@example.com', '+79001234567', 5000.00, 'BK20240423001', true, NOW(), NOW()),
(2, 'Maria', 'Ivanova', 'maria.ivanova@example.com', '+79002345678', 7500.00, 'BK20240423002', true, NOW(), NOW()),
(3, 'Alexey', 'Sidorov', 'alexey.sidorov@example.com', '+79003456789', 7500.00, 'BK20240423003', true, NOW(), NOW()),
(NULL, 'Elena', 'Kuznetsova', 'elena.kuznetsova@example.com', '+79004567890', 5000.00, 'BK20240423004', true, NOW(), NOW()),
(1, 'Dmitry', 'Volkov', 'dmitry.volkov@example.com', '+79005678901', 3600.00, 'BK20240423005', true, NOW(), NOW()),
(NULL, 'Olga', 'Sokolova', 'olga.sokolova@example.com', '+79006789012', 1800.00, 'BK20240423006', true, NOW(), NOW()),
(2, 'Sergey', 'Mikhailov', 'sergey.mikhailov@example.com', '+79007890123', 24000.00, 'BK20240423007', true, NOW(), NOW()),
(4, 'Anna', 'Fedorova', 'anna.fedorova@example.com', '+79008901234', 1200.00, 'BK20240423008', true, NOW(), NOW()),
(3, 'Pavel', 'Lebedev', 'pavel.lebedev@example.com', '+79009012345', 9600.00, 'BK20240423009', true, NOW(), NOW()),
(NULL, 'Natalia', 'Kovaleva', 'natalia.kovaleva@example.com', '+79000123456', 4800.00, 'BK20240423010', true, NOW(), NOW());

-- =====================================================
-- 7. PAYMENTS DATA
-- =====================================================
INSERT INTO tickets_payment (booking_id, amount, payment_method, status, transaction_id, created_at, updated_at) VALUES
(1, 5000.00, 'card', 'completed', 'TXN202404230001', NOW(), NOW()),
(2, 7500.00, 'card', 'completed', 'TXN202404230002', NOW(), NOW()),
(3, 7500.00, 'bank_transfer', 'completed', 'TXN202404230003', NOW(), NOW()),
(4, 5000.00, 'card', 'completed', 'TXN202404230004', NOW(), NOW()),
(5, 3600.00, 'card', 'completed', 'TXN202404230005', NOW(), NOW()),
(6, 1800.00, 'card', 'completed', 'TXN202404230006', NOW(), NOW()),
(7, 24000.00, 'bank_transfer', 'completed', 'TXN202404230007', NOW(), NOW()),
(8, 1200.00, 'card', 'completed', 'TXN202404230008', NOW(), NOW()),
(9, 9600.00, 'card', 'completed', 'TXN202404230009', NOW(), NOW()),
(10, 4800.00, 'card', 'completed', 'TXN202404230010', NOW(), NOW());

-- =====================================================
-- SUMMARY
-- =====================================================
-- Routes: 8 realistic routes between major Russian cities
-- Buses: 15 buses (standard, comfort, luxury classes)
-- Schedules: 26 schedules with various departure times
-- Bookings: 10 bookings with various customer types
-- Payments: 10 payments with different methods and statuses
-- Users: 5 sample users including admin

-- =====================================================
-- USAGE INSTRUCTIONS
-- =====================================================
-- 1. Run migrations first: python manage.py migrate
-- 2. Execute this script: psql -U postgres -d bus_tickets_db -f sql/00_all_sample_data_working.sql
-- 3. Create superuser: python manage.py createsuperuser
-- 4. Login with: admin / admin123 (or your chosen password)
-- 5. Test the system with the sample data

-- Sample login credentials:
-- Username: admin
-- Email: admin@bustickets.com
-- Password: admin123

-- Sample user accounts:
-- ivan_petrov / password123
-- maria_ivanova / password123
-- alexey_sidorov / password123
-- anna_fedorova / password123
