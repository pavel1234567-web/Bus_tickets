-- Simple Working Sample Data Script for Bus Tickets System
-- This script populates all tables with realistic test data
-- Execute this script after running migrations

-- =====================================================
-- 1. CLEAR EXISTING DATA AND RESET SEQUENCES
-- =====================================================
DELETE FROM tickets_booking_tickets;
DELETE FROM tickets_payment;
DELETE FROM tickets_booking;
DELETE FROM tickets_ticket;
DELETE FROM tickets_schedule;
DELETE FROM tickets_bus;
DELETE FROM tickets_route;
DELETE FROM auth_user WHERE username IN ('admin', 'ivan_petrov', 'maria_ivanova', 'alexey_sidorov', 'anna_fedorova');

-- Reset sequences to start from 1
ALTER SEQUENCE tickets_route_id_seq RESTART WITH 1;
ALTER SEQUENCE tickets_bus_id_seq RESTART WITH 1;
ALTER SEQUENCE tickets_schedule_id_seq RESTART WITH 1;
ALTER SEQUENCE tickets_ticket_id_seq RESTART WITH 1;
ALTER SEQUENCE tickets_booking_id_seq RESTART WITH 1;
ALTER SEQUENCE tickets_payment_id_seq RESTART WITH 1;

-- =====================================================
-- 2. ROUTES DATA (IDs 1-8)
-- =====================================================
INSERT INTO tickets_route (id, name, departure_city, arrival_city, distance, estimated_time, base_price, is_active, created_at, updated_at) VALUES
(1, 'Moscow - St. Petersburg', 'Moscow', 'St. Petersburg', 704.5, '08:00:00', 2500.00, true, NOW(), NOW()),
(2, 'St. Petersburg - Moscow', 'St. Petersburg', 'Moscow', 704.5, '08:00:00', 2500.00, true, NOW(), NOW()),
(3, 'Moscow - Kazan', 'Moscow', 'Kazan', 819.0, '14:00:00', 1800.00, true, NOW(), NOW()),
(4, 'Kazan - Moscow', 'Kazan', 'Moscow', 819.0, '14:00:00', 1800.00, true, NOW(), NOW()),
(5, 'Moscow - Nizhny Novgorod', 'Moscow', 'Nizhny Novgorod', 439.0, '06:00:00', 1200.00, true, NOW(), NOW()),
(6, 'Nizhny Novgorod - Moscow', 'Nizhny Novgorod', 'Moscow', 439.0, '06:00:00', 1200.00, true, NOW(), NOW()),
(7, 'Moscow - Sochi', 'Moscow', 'Sochi', 1673.0, '24:00:00', 4000.00, true, NOW(), NOW()),
(8, 'Sochi - Moscow', 'Sochi', 'Moscow', 1673.0, '24:00:00', 4000.00, true, NOW(), NOW());

-- =====================================================
-- 3. BUSES DATA (IDs 1-10)
-- =====================================================
INSERT INTO tickets_bus (id, registration_number, bus_type, total_seats, seats_per_row, has_ac, has_wifi, has_toilet, description, is_active, created_at) VALUES
(1, 'AB1234', 'standard', 45, 4, false, false, false, 'Standard economy bus for intercity routes', true, NOW()),
(2, 'BC5678', 'standard', 45, 4, false, false, false, 'Standard economy bus with basic amenities', true, NOW()),
(3, 'CD9012', 'standard', 45, 4, false, false, false, 'Standard bus for short to medium routes', true, NOW()),
(4, 'DE3456', 'standard', 45, 4, false, false, false, 'Economy class bus with comfortable seats', true, NOW()),
(5, 'EF7890', 'standard', 45, 4, false, false, false, 'Standard intercity bus', true, NOW()),
(6, 'FG2345', 'comfort', 36, 3, true, true, false, 'Comfort class bus with air conditioning and WiFi', true, NOW()),
(7, 'HI0123', 'comfort', 36, 3, true, true, false, 'Comfortable bus for long distance travel', true, NOW()),
(8, 'IJ4567', 'comfort', 36, 3, true, true, false, 'Premium comfort bus with spacious seating', true, NOW()),
(9, 'KL8901', 'comfort', 36, 3, true, true, false, 'Luxury comfort bus with modern amenities', true, NOW()),
(10, 'LM2345', 'luxury', 28, 2, true, true, true, 'Luxury first class bus with all premium amenities', true, NOW());

-- =====================================================
-- 4. SCHEDULES DATA (IDs 1-15) - USING CORRECT BUS IDs 1-10
-- =====================================================
INSERT INTO tickets_schedule (id, route_id, bus_id, departure_time, arrival_time, price_multiplier, is_active, created_at) VALUES
-- Moscow - St. Petersburg schedules
(1, 1, 1, '2024-04-23 06:00:00', '2024-04-23 14:00:00', 1.0, true, NOW()),
(2, 1, 6, '2024-04-23 08:30:00', '2024-04-23 16:30:00', 1.2, true, NOW()),
(3, 1, 10, '2024-04-23 11:00:00', '2024-04-23 19:00:00', 1.5, true, NOW()),
(4, 1, 2, '2024-04-23 14:00:00', '2024-04-23 22:00:00', 0.9, true, NOW()),
(5, 1, 7, '2024-04-23 16:30:00', '2024-04-24 00:30:00', 1.1, true, NOW()),
-- St. Petersburg - Moscow schedules
(6, 2, 3, '2024-04-23 06:00:00', '2024-04-23 14:00:00', 1.0, true, NOW()),
(7, 2, 8, '2024-04-23 08:30:00', '2024-04-23 16:30:00', 1.2, true, NOW()),
(8, 2, 9, '2024-04-23 11:00:00', '2024-04-23 19:00:00', 1.5, true, NOW()),
(9, 2, 4, '2024-04-23 14:00:00', '2024-04-23 22:00:00', 0.9, true, NOW()),
-- Moscow - Kazan schedules
(10, 3, 5, '2024-04-23 07:00:00', '2024-04-23 21:00:00', 1.0, true, NOW()),
(11, 3, 6, '2024-04-23 10:00:00', '2024-04-24 00:00:00', 1.1, true, NOW()),
(12, 3, 10, '2024-04-23 15:00:00', '2024-04-24 05:00:00', 1.3, true, NOW()),
-- Moscow - Nizhny Novgorod schedules
(13, 5, 1, '2024-04-23 06:00:00', '2024-04-23 12:00:00', 1.0, true, NOW()),
(14, 5, 7, '2024-04-23 08:00:00', '2024-04-23 14:00:00', 1.1, true, NOW()),
(15, 5, 8, '2024-04-23 10:00:00', '2024-04-23 16:00:00', 1.2, true, NOW());

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
-- 6. BOOKINGS DATA (IDs 1-10)
-- =====================================================
INSERT INTO tickets_booking (id, user_id, first_name, last_name, email, phone, total_price, booking_reference, is_paid, created_at, updated_at) VALUES
(1, 1, 'Ivan', 'Petrov', 'ivan.petrov@example.com', '+79001234567', 5000.00, 'BK20240423001', true, NOW(), NOW()),
(2, 2, 'Maria', 'Ivanova', 'maria.ivanova@example.com', '+79002345678', 7500.00, 'BK20240423002', true, NOW(), NOW()),
(3, 3, 'Alexey', 'Sidorov', 'alexey.sidorov@example.com', '+79003456789', 7500.00, 'BK20240423003', true, NOW(), NOW()),
(4, NULL, 'Elena', 'Kuznetsova', 'elena.kuznetsova@example.com', '+79004567890', 5000.00, 'BK20240423004', true, NOW(), NOW()),
(5, 1, 'Dmitry', 'Volkov', 'dmitry.volkov@example.com', '+79005678901', 3600.00, 'BK20240423005', true, NOW(), NOW()),
(6, NULL, 'Olga', 'Sokolova', 'olga.sokolova@example.com', '+79006789012', 1800.00, 'BK20240423006', true, NOW(), NOW()),
(7, 2, 'Sergey', 'Mikhailov', 'sergey.mikhailov@example.com', '+79007890123', 24000.00, 'BK20240423007', true, NOW(), NOW()),
(8, 4, 'Anna', 'Fedorova', 'anna.fedorova@example.com', '+79008901234', 1200.00, 'BK20240423008', true, NOW(), NOW()),
(9, 3, 'Pavel', 'Lebedev', 'pavel.lebedev@example.com', '+79009012345', 9600.00, 'BK20240423009', true, NOW(), NOW()),
(10, NULL, 'Natalia', 'Kovaleva', 'natalia.kovaleva@example.com', '+79000123456', 4800.00, 'BK20240423010', true, NOW(), NOW());

-- =====================================================
-- 7. PAYMENTS DATA (IDs 1-10) - USING CORRECT BOOKING IDs 1-10
-- =====================================================
INSERT INTO tickets_payment (id, booking_id, amount, payment_method, status, transaction_id, created_at, updated_at) VALUES
(1, 1, 5000.00, 'card', 'completed', 'TXN202404230001', NOW(), NOW()),
(2, 2, 7500.00, 'card', 'completed', 'TXN202404230002', NOW(), NOW()),
(3, 3, 7500.00, 'bank_transfer', 'completed', 'TXN202404230003', NOW(), NOW()),
(4, 4, 5000.00, 'card', 'completed', 'TXN202404230004', NOW(), NOW()),
(5, 5, 3600.00, 'card', 'completed', 'TXN202404230005', NOW(), NOW()),
(6, 6, 1800.00, 'card', 'completed', 'TXN202404230006', NOW(), NOW()),
(7, 7, 24000.00, 'bank_transfer', 'completed', 'TXN202404230007', NOW(), NOW()),
(8, 8, 1200.00, 'card', 'completed', 'TXN202404230008', NOW(), NOW()),
(9, 9, 9600.00, 'card', 'completed', 'TXN202404230009', NOW(), NOW()),
(10, 10, 4800.00, 'card', 'completed', 'TXN202404230010', NOW(), NOW());

-- =====================================================
-- SUMMARY
-- =====================================================
-- Routes: 8 realistic routes between major Russian cities (IDs 1-8)
-- Buses: 10 buses (standard, comfort, luxury classes) (IDs 1-10)
-- Schedules: 15 schedules with various departure times (IDs 1-15)
-- Bookings: 10 bookings with various customer types (IDs 1-10)
-- Payments: 10 payments with different methods and statuses (IDs 1-10)
-- Users: 5 sample users including admin

-- =====================================================
-- USAGE INSTRUCTIONS
-- =====================================================
-- 1. Run migrations first: python manage.py migrate
-- 2. Execute this script: psql -U postgres -d bus_tickets_db -f sql/00_all_sample_data_simple.sql
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
