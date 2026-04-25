-- Sample data for Payments table
-- SQL script to populate payments with test data
-- Note: This assumes Bookings table is already populated

-- Sample payments for paid bookings
INSERT INTO tickets_payment (booking_id, amount, payment_method, status, transaction_id, created_at, updated_at) VALUES
-- Payments for Moscow - St. Petersburg bookings
(1, 5000.00, 'card', 'completed', 'TXN202404230001', NOW(), NOW()),
(2, 7500.00, 'card', 'completed', 'TXN202404230002', NOW(), NOW()),
(3, 7500.00, 'bank_transfer', 'completed', 'TXN202404230003', NOW(), NOW()),
(4, 5000.00, 'card', 'completed', 'TXN202404230004', NOW(), NOW()),

-- Payments for Moscow - Kazan bookings
(5, 3600.00, 'card', 'completed', 'TXN202404230005', NOW(), NOW()),
(6, 1800.00, 'card', 'completed', 'TXN202404230006', NOW(), NOW()),

-- Payments for Moscow - Nizhny Novgorod bookings
(7, 24000.00, 'bank_transfer', 'completed', 'TXN202404230007', NOW(), NOW()),
(8, 1200.00, 'card', 'completed', 'TXN202404230008', NOW(), NOW()),

-- Payments for Moscow - Sochi bookings
(9, 9600.00, 'card', 'completed', 'TXN202404230009', NOW(), NOW()),
(10, 4800.00, 'card', 'completed', 'TXN202404230010', NOW(), NOW()),

-- Sample pending payments for unpaid bookings
INSERT INTO tickets_payment (booking_id, amount, payment_method, status, transaction_id, created_at, updated_at) VALUES
-- Pending payments for Moscow - St. Petersburg bookings
(11, 5000.00, 'card', 'pending', 'TXN202404230011', NOW(), NOW()),
(12, 2500.00, 'card', 'pending', 'TXN202404230012', NOW(), NOW()),
(13, 2500.00, 'bank_transfer', 'pending', 'TXN202404230013', NOW(), NOW()),

-- Pending payments for comfort bus bookings
(14, 6000.00, 'card', 'pending', 'TXN202404230014', NOW(), NOW()),
(15, 3000.00, 'card', 'pending', 'TXN202404230015', NOW(), NOW()),

-- Pending payments for luxury bus bookings
(16, 7500.00, 'card', 'pending', 'TXN202404230016', NOW(), NOW()),
(17, 3750.00, 'bank_transfer', 'pending', 'TXN202404230017', NOW(), NOW()),

-- More sample payments with various statuses and methods
INSERT INTO tickets_payment (booking_id, amount, payment_method, status, transaction_id, created_at, updated_at) VALUES
-- Recent payments (today)
(18, 2800.00, 'card', 'pending', 'TXN202404230018', NOW(), NOW()),
(19, 1400.00, 'card', 'pending', 'TXN202404230019', NOW(), NOW()),
(20, 1400.00, 'bank_transfer', 'pending', 'TXN202404230020', NOW(), NOW()),

-- Completed payments from yesterday
(21, 3600.00, 'card', 'completed', 'TXN202404220001', '2024-04-22 14:35:00', '2024-04-22 14:40:00'),
(22, 1800.00, 'card', 'completed', 'TXN202404220002', '2024-04-22 16:50:00', '2024-04-22 16:55:00'),
(23, 1800.00, 'bank_transfer', 'completed', 'TXN202404220003', '2024-04-22 18:25:00', '2024-04-22 18:30:00'),

-- Failed payments (for testing)
(24, 2600.00, 'card', 'failed', 'TXN202404150001', '2024-04-15 09:20:00', '2024-04-15 09:25:00'),
(25, 1300.00, 'card', 'failed', 'TXN202404150002', '2024-04-15 11:35:00', '2024-04-15 11:40:00'),
(26, 1300.00, 'bank_transfer', 'failed', 'TXN202404150003', '2024-04-15 13:50:00', '2024-04-15 13:55:00'),

-- Refunded payments
(27, 15000.00, 'card', 'refunded', 'TXN202404200001', '2024-04-20 08:05:00', '2024-04-20 15:30:00'),
(28, 11250.00, 'card', 'refunded', 'TXN202404200002', '2024-04-20 10:20:00', '2024-04-20 16:45:00'),
(29, 7500.00, 'bank_transfer', 'refunded', 'TXN202404200003', '2024-04-20 14:35:00', '2024-04-20 18:20:00'),

-- Business traveler payments (usually corporate cards)
(30, 9000.00, 'card', 'completed', 'TXN202404180001', '2024-04-18 16:25:00', '2024-04-18 16:30:00'),
(31, 6000.00, 'card', 'completed', 'TXN202404180002', '2024-04-18 17:50:00', '2024-04-18 17:55:00'),
(32, 4500.00, 'card', 'pending', 'TXN202404180003', '2024-04-18 19:15:00', NOW()),

-- Student payments (various methods)
(33, 1800.00, 'card', 'completed', 'TXN202404170001', '2024-04-17 12:35:00', '2024-04-17 12:40:00'),
(34, 1200.00, 'bank_transfer', 'pending', 'TXN202404170002', '2024-04-17 14:50:00', NOW()),
(35, 1200.00, 'card', 'completed', 'TXN202404170003', '2024-04-17 16:05:00', '2024-04-17 16:10:00'),

-- Tourist payments (often international cards)
(36, 9600.00, 'card', 'completed', 'TXN202404160001', '2024-04-16 10:25:00', '2024-04-16 10:30:00'),
(37, 4800.00, 'card', 'completed', 'TXN202404160002', '2024-04-16 11:50:00', '2024-04-16 11:55:00'),
(38, 7200.00, 'card', 'pending', 'TXN202404160003', '2024-04-16 13:15:00', NOW()),

-- Cash payments (less common, usually for last-minute bookings)
(39, 2500.00, 'cash', 'completed', 'CASH202404220001', '2024-04-22 20:35:00', '2024-04-22 20:40:00'),
(40, 5000.00, 'cash', 'completed', 'CASH202404220002', '2024-04-22 21:50:00', '2024-04-22 21:55:00'),
(41, 3750.00, 'cash', 'pending', 'CASH202404220003', '2024-04-22 22:20:00', NOW()),

-- Corporate payments (bank transfers)
(42, 18000.00, 'bank_transfer', 'completed', 'CORP202404190001', '2024-04-19 09:05:00', '2024-04-19 14:30:00'),
(43, 13500.00, 'bank_transfer', 'completed', 'CORP202404190002', '2024-04-19 10:35:00', '2024-04-19 15:45:00'),
(44, 9000.00, 'bank_transfer', 'pending', 'CORP202404190003', '2024-04-19 12:20:00', NOW()),

-- International payments
(45, 4400.00, 'card', 'completed', 'INTL202404210001', '2024-04-21 15:35:00', '2024-04-21 15:40:00'),
(46, 2200.00, 'card', 'completed', 'INTL202404210002', '2024-04-21 16:50:00', '2024-04-21 16:55:00'),
(47, 3300.00, 'card', 'pending', 'INTL202404210003', '2024-04-21 18:25:00', NOW()),

-- Elderly passenger payments (often cash or bank transfer)
(48, 3000.00, 'cash', 'completed', 'CASH202404140001', '2024-04-14 11:25:00', '2024-04-14 11:30:00'),
(49, 1500.00, 'bank_transfer', 'completed', 'BANK202404140002', '2024-04-14 13:50:00', '2024-04-14 14:00:00'),
(50, 2250.00, 'cash', 'pending', 'CASH202404140003', '2024-04-14 15:15:00', NOW()),

-- Regular commuter payments (often saved cards)
(51, 2400.00, 'card', 'completed', 'TXN202404130001', '2024-04-13 08:35:00', '2024-04-13 08:40:00'),
(52, 2400.00, 'card', 'completed', 'TXN202404130002', '2024-04-13 08:50:00', '2024-04-13 08:55:00'),
(53, 1200.00, 'card', 'completed', 'TXN202404130003', '2024-04-13 09:20:00', '2024-04-13 09:25:00'),

-- Weekend traveler payments
(54, 3600.00, 'card', 'completed', 'TXN202404120001', '2024-04-12 17:25:00', '2024-04-12 17:30:00'),
(55, 1800.00, 'card', 'pending', 'TXN202404120002', '2024-04-12 18:50:00', NOW()),
(56, 2700.00, 'card', 'completed', 'TXN202404120003', '2024-04-12 19:35:00', '2024-04-12 19:40:00'),

-- Multiple payment attempts for same booking (failed then succeeded)
(57, 2600.00, 'card', 'failed', 'TXN202404110001', '2024-04-11 10:15:00', '2024-04-11 10:20:00'),
(57, 2600.00, 'card', 'completed', 'TXN202404110002', '2024-04-11 10:25:00', '2024-04-11 10:30:00'),

-- Split payments (for large bookings)
(58, 15000.00, 'card', 'completed', 'TXN202404100001', '2024-04-10 09:15:00', '2024-04-10 09:20:00'),
(58, 3000.00, 'card', 'completed', 'TXN202404100002', '2024-04-10 09:25:00', '2024-04-10 09:30:00'),

-- Payment method changes (initially bank transfer, then card)
(59, 1800.00, 'bank_transfer', 'failed', 'TXN202404090001', '2024-04-09 14:20:00', '2024-04-09 14:25:00'),
(59, 1800.00, 'card', 'completed', 'TXN202404090002', '2024-04-09 14:30:00', '2024-04-09 14:35:00'),

-- High-value payments (luxury routes)
(60, 12000.00, 'card', 'completed', 'TXN202404080001', '2024-04-08 11:40:00', '2024-04-08 11:45:00'),
(61, 15000.00, 'bank_transfer', 'completed', 'TXN202404080002', '2024-04-08 13:55:00', '2024-04-08 20:15:00'),
(62, 9000.00, 'card', 'pending', 'TXN202404080003', '2024-04-08 15:20:00', NOW()),

-- Mobile wallet payments
(63, 2800.00, 'card', 'completed', 'MOBILE202404070001', '2024-04-07 12:30:00', '2024-04-07 12:35:00'),
(64, 1400.00, 'card', 'completed', 'MOBILE202404070002', '2024-04-07 14:45:00', '2024-04-07 14:50:00'),
(65, 2100.00, 'card', 'pending', 'MOBILE202404070003', '2024-04-07 16:10:00', NOW()),

-- Gift card payments
(66, 2000.00, 'card', 'completed', 'GIFT202404060001', '2024-04-06 10:25:00', '2024-04-06 10:30:00'),
(67, 1500.00, 'card', 'completed', 'GIFT202404060002', '2024-04-06 11:40:00', '2024-04-06 11:45:00'),
(68, 1000.00, 'card', 'pending', 'GIFT202404060003', '2024-04-06 13:15:00', NOW()),

-- Installment payments
(69, 8000.00, 'card', 'completed', 'INST202404050001', '2024-04-05 09:20:00', '2024-04-05 09:25:00'),
(69, 4000.00, 'card', 'completed', 'INST202404050002', '2024-04-12 09:20:00', '2024-04-12 09:25:00'),
(69, 4000.00, 'card', 'pending', 'INST202404050003', '2024-04-19 09:20:00', NOW()),

-- Express payments (quick processing)
(70, 3500.00, 'card', 'completed', 'EXPRESS202404040001', '2024-04-04 08:15:00', '2024-04-04 08:16:00'),
(71, 1750.00, 'card', 'completed', 'EXPRESS202404040002', '2024-04-04 10:30:00', '2024-04-04 10:31:00'),
(72, 5250.00, 'card', 'pending', 'EXPRESS202404040003', '2024-04-04 14:45:00', NOW()),

-- Subscription payments (regular commuters)
(73, 48000.00, 'bank_transfer', 'completed', 'SUB202404010001', '2024-04-01 08:00:00', '2024-04-01 17:00:00'),
(74, 24000.00, 'card', 'completed', 'SUB202404010002', '2024-04-01 09:15:00', '2024-04-01 09:20:00'),
(75, 36000.00, 'card', 'pending', 'SUB202404010003', '2024-04-01 10:30:00', NOW()),

-- Discount payments (with promotional codes)
(76, 2250.00, 'card', 'completed', 'DISCOUNT202404030001', '2024-04-03 15:25:00', '2024-04-03 15:30:00'),
(77, 1800.00, 'card', 'completed', 'DISCOUNT202404030002', '2024-04-03 16:40:00', '2024-04-03 16:45:00'),
(78, 3150.00, 'card', 'pending', 'DISCOUNT202404030003', '2024-04-03 18:10:00', NOW()),

-- Group booking payments
(79, 45000.00, 'bank_transfer', 'completed', 'GROUP202404020001', '2024-04-02 11:20:00', '2024-04-02 16:45:00'),
(80, 22500.00, 'card', 'completed', 'GROUP202404020002', '2024-04-02 13:35:00', '2024-04-02 13:40:00'),
(81, 67500.00, 'bank_transfer', 'pending', 'GROUP202404020003', '2024-04-02 15:50:00', NOW()),

-- Emergency payments (last minute changes)
(82, 5500.00, 'card', 'completed', 'EMERGENCY202404010001', '2024-04-01 22:15:00', '2024-04-01 22:20:00'),
(83, 2750.00, 'card', 'completed', 'EMERGENCY202404010002', '2024-04-01 23:30:00', '2024-04-01 23:35:00'),
(84, 8250.00, 'cash', 'pending', 'EMERGENCY202404010003', '2024-04-02 00:45:00', NOW()),

-- VIP payments (premium services)
(85, 25000.00, 'card', 'completed', 'VIP202404010001', '2024-04-01 07:00:00', '2024-04-01 07:05:00'),
(86, 12500.00, 'card', 'completed', 'VIP202404010002', '2024-04-01 08:15:00', '2024-04-01 08:20:00'),
(87, 37500.00, 'bank_transfer', 'pending', 'VIP202404010003', '2024-04-01 09:30:00', NOW());
