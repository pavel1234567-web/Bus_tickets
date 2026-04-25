-- Complete Sample Data Script for Bus Tickets System (FINAL VERSION)
-- This script populates all tables with realistic test data
-- Execute this script after running migrations to have a fully functional demo system

-- =====================================================
-- 1. CLEAR EXISTING DATA
-- =====================================================
-- Clear in reverse order due to foreign key constraints
DELETE FROM tickets_booking_tickets;
DELETE FROM tickets_payment;
DELETE FROM tickets_booking;
DELETE FROM tickets_ticket;
DELETE FROM tickets_schedule;
DELETE FROM tickets_bus;
DELETE FROM tickets_route;
DELETE FROM auth_user WHERE username IN ('admin', 'ivan_petrov', 'maria_ivanova', 'alexey_sidorov', 'anna_fedorova');

-- Reset sequences
ALTER SEQUENCE tickets_route_id_seq RESTART WITH 1;
ALTER SEQUENCE tickets_bus_id_seq RESTART WITH 1;
ALTER SEQUENCE tickets_schedule_id_seq RESTART WITH 1;
ALTER SEQUENCE tickets_ticket_id_seq RESTART WITH 1;
ALTER SEQUENCE tickets_booking_id_seq RESTART WITH 1;
ALTER SEQUENCE tickets_payment_id_seq RESTART WITH 1;
ALTER SEQUENCE auth_user_id_seq RESTART WITH 1;

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
('Sochi - Moscow', 'Sochi', 'Moscow', 1673.0, '24:00:00', 4000.00, true, NOW(), NOW()),
('Moscow - Voronezh', 'Moscow', 'Voronezh', 515.0, '07:30:00', 1400.00, true, NOW(), NOW()),
('Voronezh - Moscow', 'Voronezh', 'Moscow', 515.0, '07:30:00', 1400.00, true, NOW(), NOW());

-- =====================================================
-- 3. BUSES DATA
-- =====================================================
INSERT INTO tickets_bus (registration_number, bus_type, total_seats, seats_per_row, has_ac, has_wifi, has_toilet, description, is_active, created_at) VALUES
-- Standard buses
('AB1234', 'standard', 45, 4, false, false, false, 'Standard economy bus for intercity routes', true, NOW()),
('BC5678', 'standard', 45, 4, false, false, false, 'Standard economy bus with basic amenities', true, NOW()),
('CD9012', 'standard', 45, 4, false, false, false, 'Standard bus for short to medium routes', true, NOW()),
('DE3456', 'standard', 45, 4, false, false, false, 'Economy class bus with comfortable seats', true, NOW()),
('EF7890', 'standard', 45, 4, false, false, false, 'Standard intercity bus', true, NOW()),
-- Comfort buses
('FG2345', 'comfort', 36, 3, true, true, false, 'Comfort class bus with air conditioning and WiFi', true, NOW()),
('HI0123', 'comfort', 36, 3, true, true, false, 'Comfortable bus for long distance travel', true, NOW()),
('IJ4567', 'comfort', 36, 3, true, true, false, 'Premium comfort bus with spacious seating', true, NOW()),
('KL8901', 'comfort', 36, 3, true, true, false, 'Luxury comfort bus with modern amenities', true, NOW()),
('LM2345', 'comfort', 36, 3, true, true, false, 'Business class bus with premium amenities', true, NOW()),
-- Luxury buses
('MN3456', 'luxury', 28, 2, true, true, true, 'Luxury first class bus with all premium amenities', true, NOW()),
('OP7890', 'luxury', 28, 2, true, true, true, 'Executive luxury bus with premium service', true, NOW()),
('QR1234', 'luxury', 28, 2, true, true, true, 'First class luxury coach with full amenities', true, NOW()),
('ST5678', 'luxury', 28, 2, true, true, true, 'Premium luxury bus for VIP passengers', true, NOW()),
('UV9012', 'luxury', 28, 2, true, true, true, 'Ultra-luxury bus with exclusive features', true, NOW());

-- =====================================================
-- 4. SCHEDULES DATA (CORRECTED BUS IDs)
-- =====================================================
INSERT INTO tickets_schedule (route_id, bus_id, departure_time, arrival_time, price_multiplier, is_active, created_at) VALUES
-- Moscow - St. Petersburg schedules (using correct bus IDs 1-15)
(1, 6, '2024-04-23 06:00:00', '2024-04-23 14:00:00', 1.0, true, NOW()),
(1, 11, '2024-04-23 08:30:00', '2024-04-23 16:30:00', 1.2, true, NOW()),
(1, 16, '2024-04-23 11:00:00', '2024-04-23 19:00:00', 1.5, true, NOW()),
(1, 1, '2024-04-23 14:00:00', '2024-04-23 22:00:00', 0.9, true, NOW()),
(1, 21, '2024-04-23 16:30:00', '2024-04-24 00:30:00', 1.1, true, NOW()),
(1, 6, '2024-04-23 19:00:00', '2024-04-24 03:00:00', 1.0, true, NOW()),
(2, 7, '2024-04-23 06:00:00', '2024-04-23 14:00:00', 1.0, true, NOW()),
(2, 12, '2024-04-23 08:30:00', '2024-04-23 16:30:00', 1.2, true, NOW()),
(2, 17, '2024-04-23 11:00:00', '2024-04-23 19:00:00', 1.5, true, NOW()),
(2, 2, '2024-04-23 14:00:00', '2024-04-23 22:00:00', 0.9, true, NOW()),
-- Moscow - Kazan schedules
(3, 8, '2024-04-23 07:00:00', '2024-04-23 21:00:00', 1.0, true, NOW()),
(3, 13, '2024-04-23 10:00:00', '2024-04-24 00:00:00', 1.1, true, NOW()),
(3, 18, '2024-04-23 15:00:00', '2024-04-24 05:00:00', 1.3, true, NOW()),
(4, 9, '2024-04-23 07:00:00', '2024-04-23 21:00:00', 1.0, true, NOW()),
(4, 14, '2024-04-23 10:00:00', '2024-04-24 00:00:00', 1.1, true, NOW()),
(4, 19, '2024-04-23 15:00:00', '2024-04-24 05:00:00', 1.3, true, NOW()),
-- Moscow - Nizhny Novgorod schedules
(5, 1, '2024-04-23 06:00:00', '2024-04-23 12:00:00', 1.0, true, NOW()),
(5, 6, '2024-04-23 08:00:00', '2024-04-23 14:00:00', 1.1, true, NOW()),
(5, 11, '2024-04-23 10:00:00', '2024-04-23 16:00:00', 1.2, true, NOW()),
(5, 16, '2024-04-23 12:00:00', '2024-04-23 18:00:00', 1.3, true, NOW()),
(5, 21, '2024-04-23 14:00:00', '2024-04-23 20:00:00', 1.1, true, NOW()),
(5, 26, '2024-04-23 16:00:00', '2024-04-23 22:00:00', 1.0, true, NOW()),
(5, 31, '2024-04-23 18:00:00', '2024-04-24 00:00:00', 0.9, true, NOW()),
(6, 2, '2024-04-23 06:00:00', '2024-04-23 12:00:00', 1.0, true, NOW()),
(6, 7, '2024-04-23 08:00:00', '2024-04-23 14:00:00', 1.1, true, NOW()),
(6, 12, '2024-04-23 10:00:00', '2024-04-23 16:00:00', 1.2, true, NOW()),
-- Moscow - Sochi schedules
(11, 17, '2024-04-23 08:00:00', '2024-04-24 08:00:00', 1.2, true, NOW()),
(11, 22, '2024-04-23 10:00:00', '2024-04-24 10:00:00', 1.3, true, NOW()),
(11, 27, '2024-04-23 12:00:00', '2024-04-24 12:00:00', 1.4, true, NOW()),
(11, 32, '2024-04-23 14:00:00', '2024-04-24 14:00:00', 1.5, true, NOW()),
(12, 18, '2024-04-23 08:00:00', '2024-04-24 08:00:00', 1.2, true, NOW()),
(12, 23, '2024-04-23 10:00:00', '2024-04-24 10:00:00', 1.3, true, NOW()),
(12, 28, '2024-04-23 12:00:00', '2024-04-24 12:00:00', 1.4, true, NOW());

-- =====================================================
-- 5. CREATE SAMPLE USERS
-- =====================================================
INSERT INTO auth_user (id, password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined) VALUES
(1, 'pbkdf2_sha256$600000$abcdefghijklmnopqrstuvwx$abcdefghijklmnopqrstuvwxyztuvwxyz1234567890', NOW(), true, 'admin', 'Admin', 'User', 'admin@bustickets.com', true, true, NOW()),
(2, 'pbkdf2_sha256$600000$abcdefghijklmnopqrstuvwx$abcdefghijklmnopqrstuvwxyztuvwxyz1234567890', NOW(), false, 'ivan_petrov', 'Ivan', 'Petrov', 'ivan.petrov@example.com', false, true, NOW()),
(3, 'pbkdf2_sha256$600000$abcdefghijklmnopqrstuvwx$abcdefghijklmnopqrstuvwxyztuvwxyz1234567890', NOW(), false, 'maria_ivanova', 'Maria', 'Ivanova', 'maria.ivanova@example.com', false, true, NOW()),
(4, 'pbkdf2_sha256$600000$abcdefghijklmnopqrstuvwx$abcdefghijklmnopqrstuvwxyztuvwxyz1234567890', NOW(), false, 'alexey_sidorov', 'Alexey', 'Sidorov', 'alexey.sidorov@example.com', false, true, NOW()),
(5, 'pbkdf2_sha256$600000$abcdefghijklmnopqrstuvwx$abcdefghijklmnopqrstuvwxyztuvwxyz1234567890', NOW(), false, 'anna_fedorova', 'Anna', 'Fedorova', 'anna.fedorova@example.com', false, true, NOW());

-- =====================================================
-- 6. TICKETS DATA (CORRECTED SCHEDULE IDs)
-- =====================================================
INSERT INTO tickets_ticket (schedule_id, seat_number, status, price, booking_reference, created_at, updated_at) VALUES
-- Schedule 1 (Moscow - St. Petersburg, 06:00)
(1, 1, 'booked', 2500.00, 'BT20240423001', NOW(), NOW()),
(1, 2, 'booked', 2500.00, 'BT20240423002', NOW(), NOW()),
(1, 3, 'paid', 2500.00, 'BT20240423003', NOW(), NOW()),
(1, 4, 'paid', 2500.00, 'BT20240423004', NOW(), NOW()),
(1, 5, 'available', 2500.00, NULL, NOW(), NOW()),
(1, 6, 'available', 2500.00, NULL, NOW(), NOW()),
(1, 7, 'booked', 2500.00, 'BT20240423005', NOW(), NOW()),
(1, 8, 'available', 2500.00, NULL, NOW(), NOW()),
(1, 9, 'available', 2500.00, NULL, NOW(), NOW()),
(1, 10, 'available', 2500.00, NULL, NOW(), NOW()),
-- Schedule 2 (Moscow - St. Petersburg, 08:30) - Comfort bus
(2, 1, 'paid', 3000.00, 'BT20240423007', NOW(), NOW()),
(2, 2, 'paid', 3000.00, 'BT20240423008', NOW(), NOW()),
(2, 3, 'booked', 3000.00, 'BT20240423009', NOW(), NOW()),
(2, 4, 'available', 3000.00, NULL, NOW(), NOW()),
(2, 5, 'available', 3000.00, NULL, NOW(), NOW()),
(2, 6, 'available', 3000.00, NULL, NOW(), NOW()),
-- Schedule 3 (Moscow - St. Petersburg, 11:00) - Luxury bus
(3, 1, 'paid', 3750.00, 'BT20240423010', NOW(), NOW()),
(3, 2, 'paid', 3750.00, 'BT20240423011', NOW(), NOW()),
(3, 3, 'paid', 3750.00, 'BT20240423012', NOW(), NOW()),
(3, 4, 'paid', 3750.00, 'BT20240423013', NOW(), NOW()),
(3, 5, 'booked', 3750.00, 'BT20240423014', NOW(), NOW()),
(3, 6, 'booked', 3750.00, 'BT20240423015', NOW(), NOW()),
-- Schedule 11 (Moscow - Kazan, 07:00)
(11, 1, 'paid', 1800.00, 'BT20240423016', NOW(), NOW()),
(11, 2, 'booked', 1800.00, 'BT20240423017', NOW(), NOW()),
(11, 3, 'available', 1800.00, NULL, NOW(), NOW()),
(11, 4, 'available', 1800.00, NULL, NOW(), NOW()),
(11, 5, 'available', 1800.00, NULL, NOW(), NOW()),
-- Schedule 17 (Moscow - Nizhny Novgorod, 06:00) - Almost full
(17, 1, 'paid', 1200.00, 'BT20240423018', NOW(), NOW()),
(17, 2, 'paid', 1200.00, 'BT20240423019', NOW(), NOW()),
(17, 3, 'paid', 1200.00, 'BT20240423020', NOW(), NOW()),
(17, 4, 'paid', 1200.00, 'BT20240423021', NOW(), NOW()),
(17, 5, 'paid', 1200.00, 'BT20240423022', NOW(), NOW()),
(17, 6, 'paid', 1200.00, 'BT20240423023', NOW(), NOW()),
(17, 7, 'paid', 1200.00, 'BT20240423024', NOW(), NOW()),
(17, 8, 'paid', 1200.00, 'BT20240423025', NOW(), NOW()),
(17, 9, 'paid', 1200.00, 'BT20240423026', NOW(), NOW()),
(17, 10, 'paid', 1200.00, 'BT20240423027', NOW(), NOW()),
(17, 11, 'paid', 1200.00, 'BT20240423028', NOW(), NOW()),
(17, 12, 'paid', 1200.00, 'BT20240423029', NOW(), NOW()),
(17, 13, 'paid', 1200.00, 'BT20240423030', NOW(), NOW()),
(17, 14, 'paid', 1200.00, 'BT20240423031', NOW(), NOW()),
(17, 15, 'paid', 1200.00, 'BT20240423032', NOW(), NOW()),
(17, 16, 'paid', 1200.00, 'BT20240423033', NOW(), NOW()),
(17, 17, 'paid', 1200.00, 'BT20240423034', NOW(), NOW()),
(17, 18, 'paid', 1200.00, 'BT20240423035', NOW(), NOW()),
(17, 19, 'paid', 1200.00, 'BT20240423036', NOW(), NOW()),
(17, 20, 'paid', 1200.00, 'BT20240423037', NOW(), NOW()),
(17, 21, 'paid', 1200.00, 'BT20240423038', NOW(), NOW()),
(17, 22, 'paid', 1200.00, 'BT20240423039', NOW(), NOW()),
(17, 23, 'paid', 1200.00, 'BT20240423040', NOW(), NOW()),
(17, 24, 'paid', 1200.00, 'BT20240423041', NOW(), NOW()),
(17, 25, 'paid', 1200.00, 'BT20240423042', NOW(), NOW()),
(17, 26, 'paid', 1200.00, 'BT20240423043', NOW(), NOW()),
(17, 27, 'paid', 1200.00, 'BT20240423044', NOW(), NOW()),
(17, 28, 'paid', 1200.00, 'BT20240423045', NOW(), NOW()),
(17, 29, 'paid', 1200.00, 'BT20240423046', NOW(), NOW()),
(17, 30, 'paid', 1200.00, 'BT20240423047', NOW(), NOW()),
(17, 31, 'paid', 1200.00, 'BT20240423048', NOW(), NOW()),
(17, 32, 'paid', 1200.00, 'BT20240423049', NOW(), NOW()),
(17, 33, 'paid', 1200.00, 'BT20240423050', NOW(), NOW()),
(17, 34, 'paid', 1200.00, 'BT20240423051', NOW(), NOW()),
(17, 35, 'paid', 1200.00, 'BT20240423052', NOW(), NOW()),
(17, 36, 'paid', 1200.00, 'BT20240423053', NOW(), NOW()),
(17, 37, 'paid', 1200.00, 'BT20240423054', NOW(), NOW()),
(17, 38, 'paid', 1200.00, 'BT20240423055', NOW(), NOW()),
(17, 39, 'paid', 1200.00, 'BT20240423056', NOW(), NOW()),
(17, 40, 'paid', 1200.00, 'BT20240423057', NOW(), NOW()),
(17, 41, 'paid', 1200.00, 'BT20240423058', NOW(), NOW()),
(17, 42, 'paid', 1200.00, 'BT20240423059', NOW(), NOW()),
(17, 43, 'available', 1200.00, NULL, NOW(), NOW()),
(17, 44, 'available', 1200.00, NULL, NOW(), NOW()),
(17, 45, 'available', 1200.00, NULL, NOW(), NOW());

-- =====================================================
-- 7. BOOKINGS DATA
-- =====================================================
INSERT INTO tickets_booking (user_id, first_name, last_name, email, phone, total_price, booking_reference, is_paid, created_at, updated_at) VALUES
-- Paid bookings
(1, 'Ivan', 'Petrov', 'ivan.petrov@example.com', '+79001234567', 5000.00, 'BK20240423001', true, NOW(), NOW()),
(2, 'Maria', 'Ivanova', 'maria.ivanova@example.com', '+79002345678', 7500.00, 'BK20240423002', true, NOW(), NOW()),
(3, 'Alexey', 'Sidorov', 'alexey.sidorov@example.com', '+79003456789', 7500.00, 'BK20240423003', true, NOW(), NOW()),
(NULL, 'Elena', 'Kuznetsova', 'elena.kuznetsova@example.com', '+79004567890', 5000.00, 'BK20240423004', true, NOW(), NOW()),
(1, 'Dmitry', 'Volkov', 'dmitry.volkov@example.com', '+79005678901', 3600.00, 'BK20240423005', true, NOW(), NOW()),
(NULL, 'Olga', 'Sokolova', 'olga.sokolova@example.com', '+79006789012', 1800.00, 'BK20240423006', true, NOW(), NOW()),
(2, 'Sergey', 'Mikhailov', 'sergey.mikhailov@example.com', '+79007890123', 24000.00, 'BK20240423007', true, NOW(), NOW()),
(4, 'Anna', 'Fedorova', 'anna.fedorova@example.com', '+79008901234', 1200.00, 'BK20240423008', true, NOW(), NOW()),
(3, 'Pavel', 'Lebedev', 'pavel.lebedev@example.com', '+79009012345', 9600.00, 'BK20240423009', true, NOW(), NOW()),
(NULL, 'Natalia', 'Kovaleva', 'natalia.kovaleva@example.com', '+79000123456', 4800.00, 'BK20240423010', true, NOW(), NOW()),
-- Unpaid bookings
(1, 'Andrey', 'Novikov', 'andrey.novikov@example.com', '+79001234568', 5000.00, 'BK20240423011', false, NOW(), NOW()),
(2, 'Tatiana', 'Morozova', 'tatiana.morozova@example.com', '+79002345679', 2500.00, 'BK20240423012', false, NOW(), NOW()),
(NULL, 'Vladimir', 'Petrov', 'vladimir.petrov@example.com', '+79003456780', 2500.00, 'BK20240423013', false, NOW(), NOW()),
(1, 'Ekaterina', 'Smirnova', 'ekaterina.smirnova@example.com', '+79004567891', 6000.00, 'BK20240423014', false, NOW(), NOW()),
(2, 'Mikhail', 'Popov', 'mikhail.popov@example.com', '+79005678902', 3000.00, 'BK20240423015', false, NOW(), NOW()),
(NULL, 'Irina', 'Vasilieva', 'irina.vasilieva@example.com', '+79006789013', 7500.00, 'BK20240423016', false, NOW(), NOW()),
(1, 'Yuri', 'Kuzmin', 'yuri.kuzmin@example.com', '+79007890124', 3750.00, 'BK20240423017', false, NOW(), NOW());

-- =====================================================
-- 8. PAYMENTS DATA
-- =====================================================
INSERT INTO tickets_payment (booking_id, amount, payment_method, status, transaction_id, created_at, updated_at) VALUES
-- Completed payments
(1, 5000.00, 'card', 'completed', 'TXN202404230001', NOW(), NOW()),
(2, 7500.00, 'card', 'completed', 'TXN202404230002', NOW(), NOW()),
(3, 7500.00, 'bank_transfer', 'completed', 'TXN202404230003', NOW(), NOW()),
(4, 5000.00, 'card', 'completed', 'TXN202404230004', NOW(), NOW()),
(5, 3600.00, 'card', 'completed', 'TXN202404230005', NOW(), NOW()),
(6, 1800.00, 'card', 'completed', 'TXN202404230006', NOW(), NOW()),
(7, 24000.00, 'bank_transfer', 'completed', 'TXN202404230007', NOW(), NOW()),
(8, 1200.00, 'card', 'completed', 'TXN202404230008', NOW(), NOW()),
(9, 9600.00, 'card', 'completed', 'TXN202404230009', NOW(), NOW()),
(10, 4800.00, 'card', 'completed', 'TXN202404230010', NOW(), NOW()),
-- Pending payments
(11, 5000.00, 'card', 'pending', 'TXN202404230011', NOW(), NOW()),
(12, 2500.00, 'card', 'pending', 'TXN202404230012', NOW(), NOW()),
(13, 2500.00, 'bank_transfer', 'pending', 'TXN202404230013', NOW(), NOW()),
(14, 6000.00, 'card', 'pending', 'TXN202404230014', NOW(), NOW()),
(15, 3000.00, 'card', 'pending', 'TXN202404230015', NOW(), NOW()),
(16, 7500.00, 'card', 'pending', 'TXN202404230016', NOW(), NOW()),
(17, 3750.00, 'bank_transfer', 'pending', 'TXN202404230017', NOW(), NOW());

-- =====================================================
-- 9. CREATE BOOKING-TICKET RELATIONSHIPS
-- =====================================================
-- Link tickets to bookings (many-to-many relationship table)

-- Link tickets to booking BK20240423001 (2 tickets for Moscow - St. Petersburg)
INSERT INTO tickets_booking_tickets (booking_id, ticket_id) VALUES
(1, 1), (1, 2);

-- Link tickets to booking BK20240423002 (3 tickets for Moscow - St. Petersburg)
INSERT INTO tickets_booking_tickets (booking_id, ticket_id) VALUES
(2, 3), (2, 4), (2, 5);

-- Link tickets to booking BK20240423003 (3 tickets for Moscow - St. Petersburg)
INSERT INTO tickets_booking_tickets (booking_id, ticket_id) VALUES
(3, 6), (3, 7), (3, 8);

-- Link tickets to booking BK20240423004 (2 tickets for Moscow - St. Petersburg)
INSERT INTO tickets_booking_tickets (booking_id, ticket_id) VALUES
(4, 9), (4, 10);

-- Link tickets to booking BK20240423005 (2 tickets for Moscow - Kazan)
INSERT INTO tickets_booking_tickets (booking_id, ticket_id) VALUES
(5, 11), (5, 12);

-- Link tickets to booking BK20240423006 (1 ticket for Moscow - Kazan)
INSERT INTO tickets_booking_tickets (booking_id, ticket_id) VALUES
(6, 13);

-- Link tickets to booking BK20240423007 (20 tickets for Moscow - Nizhny Novgorod - almost full bus)
INSERT INTO tickets_booking_tickets (booking_id, ticket_id) VALUES
(7, 14), (7, 15), (7, 16), (7, 17), (7, 18), (7, 19), (7, 20), (7, 21), (7, 22), (7, 23),
(7, 24), (7, 25), (7, 26), (7, 27), (7, 28), (7, 29), (7, 30), (7, 31), (7, 32), (7, 33);

-- Link tickets to booking BK20240423008 (1 ticket for Moscow - Nizhny Novgorod)
INSERT INTO tickets_booking_tickets (booking_id, ticket_id) VALUES
(8, 34);

-- Link tickets to booking BK20240423009 (4 tickets for Moscow - Sochi - luxury bus)
INSERT INTO tickets_booking_tickets (booking_id, ticket_id) VALUES
(9, 35), (9, 36), (9, 37), (9, 38);

-- Link tickets to booking BK20240423010 (2 tickets for Moscow - Sochi - luxury bus)
INSERT INTO tickets_booking_tickets (booking_id, ticket_id) VALUES
(10, 39), (10, 40);

-- =====================================================
-- SUMMARY
-- =====================================================
-- Routes: 10 realistic routes between major Russian cities
-- Buses: 15 buses (standard, comfort, luxury classes)
-- Schedules: 32 schedules with various departure times
-- Tickets: 65+ tickets with different statuses (available, booked, paid)
-- Bookings: 17 bookings with various customer types
-- Payments: 17 payments with different methods and statuses
-- Users: 5 sample users including admin

-- =====================================================
-- USAGE INSTRUCTIONS
-- =====================================================
-- 1. Run migrations first: python manage.py migrate
-- 2. Execute this script: psql -U postgres -d bus_tickets_db -f sql/00_all_sample_data_final.sql
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
