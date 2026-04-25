-- Sample data for Bookings table
-- SQL script to populate bookings with test data
-- Note: This assumes Tickets table is already populated and some tickets have booking references

-- Sample bookings for paid tickets
INSERT INTO tickets_booking (user_id, first_name, last_name, email, phone, total_price, booking_reference, is_paid, created_at, updated_at) VALUES
-- Booking for Moscow - St. Petersburg (paid tickets)
(1, 'Ivan', 'Petrov', 'ivan.petrov@example.com', '+79001234567', 5000.00, 'BK20240423001', true, NOW(), NOW()),
(1, 'Maria', 'Ivanova', 'maria.ivanova@example.com', '+79002345678', 7500.00, 'BK20240423002', true, NOW(), NOW()),
(2, 'Alexey', 'Sidorov', 'alexey.sidorov@example.com', '+79003456789', 7500.00, 'BK20240423003', true, NOW(), NOW()),
(NULL, 'Elena', 'Kuznetsova', 'elena.kuznetsova@example.com', '+79004567890', 5000.00, 'BK20240423004', true, NOW(), NOW()),

-- Booking for Moscow - Kazan (paid tickets)
(1, 'Dmitry', 'Volkov', 'dmitry.volkov@example.com', '+79005678901', 3600.00, 'BK20240423005', true, NOW(), NOW()),
(NULL, 'Olga', 'Sokolova', 'olga.sokolova@example.com', '+79006789012', 1800.00, 'BK20240423006', true, NOW(), NOW()),

-- Booking for Moscow - Nizhny Novgorod (multiple paid tickets)
(2, 'Sergey', 'Mikhailov', 'sergey.mikhailov@example.com', '+79007890123', 24000.00, 'BK20240423007', true, NOW(), NOW()),
(1, 'Anna', 'Fedorova', 'anna.fedorova@example.com', '+79008901234', 1200.00, 'BK20240423008', true, NOW(), NOW()),

-- Booking for Moscow - Sochi (paid tickets)
(2, 'Pavel', 'Lebedev', 'pavel.lebedev@example.com', '+79009012345', 9600.00, 'BK20240423009', true, NOW(), NOW()),
(NULL, 'Natalia', 'Kovaleva', 'natalia.kovaleva@example.com', '+79000123456', 4800.00, 'BK20240423010', true, NOW(), NOW()),

-- Sample bookings for booked (unpaid) tickets
INSERT INTO tickets_booking (user_id, first_name, last_name, email, phone, total_price, booking_reference, is_paid, created_at, updated_at) VALUES
-- Booking for Moscow - St. Petersburg (unpaid tickets)
(1, 'Andrey', 'Novikov', 'andrey.novikov@example.com', '+79001234568', 5000.00, 'BK20240423011', false, NOW(), NOW()),
(2, 'Tatiana', 'Morozova', 'tatiana.morozova@example.com', '+79002345679', 2500.00, 'BK20240423012', false, NOW(), NOW()),
(NULL, 'Vladimir', 'Petrov', 'vladimir.petrov@example.com', '+79003456780', 2500.00, 'BK20240423013', false, NOW(), NOW()),

-- Booking for Moscow - St. Petersburg (comfort bus, unpaid)
(1, 'Ekaterina', 'Smirnova', 'ekaterina.smirnova@example.com', '+79004567891', 6000.00, 'BK20240423014', false, NOW(), NOW()),
(2, 'Mikhail', 'Popov', 'mikhail.popov@example.com', '+79005678902', 3000.00, 'BK20240423015', false, NOW(), NOW()),

-- Booking for Moscow - St. Petersburg (luxury bus, unpaid)
(NULL, 'Irina', 'Vasilieva', 'irina.vasilieva@example.com', '+79006789013', 7500.00, 'BK20240423016', false, NOW(), NOW()),
(1, 'Yuri', 'Kuzmin', 'yuri.kuzmin@example.com', '+79007890124', 3750.00, 'BK20240423017', false, NOW(), NOW()),

-- More sample bookings with various statuses
INSERT INTO tickets_booking (user_id, first_name, last_name, email, phone, total_price, booking_reference, is_paid, created_at, updated_at) VALUES
-- Recent bookings (today)
(1, 'Anton', 'Romanov', 'anton.romanov@example.com', '+79008901235', 2800.00, 'BK20240423018', false, NOW(), NOW()),
(2, 'Svetlana', 'Belova', 'svetlana.belova@example.com', '+79009012346', 1400.00, 'BK20240423019', false, NOW(), NOW()),
(NULL, 'Nikolay', 'Orlov', 'nikolay.orlov@example.com', '+79000123457', 1400.00, 'BK20240423020', false, NOW(), NOW()),

-- Bookings from yesterday
(1, 'Victoria', 'Zakharova', 'victoria.zakharova@example.com', '+79001234569', 3600.00, 'BK20240422001', true, '2024-04-22 14:30:00', NOW()),
(2, 'Stanislav', 'Galkin', 'stanislav.galkin@example.com', '+79002345670', 1800.00, 'BK20240422002', false, '2024-04-22 16:45:00', NOW()),
(NULL, 'Lyudmila', 'Vinogradova', 'lyudmila.vinogradova@example.com', '+79003456781', 1800.00, 'BK20240422003', true, '2024-04-22 18:20:00', NOW()),

-- Bookings from last week
(1, 'Rostislav', 'Belyaev', 'rostislav.belyaev@example.com', '+79004567892', 5200.00, 'BK20240415001', true, '2024-04-15 09:15:00', NOW()),
(2, 'Ksenia', 'Makarova', 'ksenia.makarova@example.com', '+79005678903', 2600.00, 'BK20240415002', true, '2024-04-15 11:30:00', NOW()),
(NULL, 'Fyodor', 'Golubev', 'fyodor.golubev@example.com', '+79006789014', 2600.00, 'BK20240415003', false, '2024-04-15 13:45:00', NOW()),

-- Business travelers (multiple tickets)
(1, 'Konstantin', 'Tarasov', 'konstantin.tarasov@example.com', '+79007890125', 15000.00, 'BK20240420001', true, '2024-04-20 08:00:00', NOW()),
(2, 'Veronika', 'Sergeeva', 'veronika.sergeeva@example.com', '+79008901236', 11250.00, 'BK20240420002', true, '2024-04-20 10:15:00', NOW()),
(NULL, 'Boris', 'Karpov', 'boris.karpov@example.com', '+79009012347', 7500.00, 'BK20240420003', false, '2024-04-20 14:30:00', NOW()),

-- Family bookings
(1, 'Alexander', 'Frolov', 'alexander.frolov@example.com', '+79000123458', 9000.00, 'BK20240418001', true, '2024-04-18 16:20:00', NOW()),
(2, 'Marina', 'Tikhonova', 'marina.tikhonova@example.com', '+79001234560', 6000.00, 'BK20240418002', true, '2024-04-18 17:45:00', NOW()),
(NULL, 'Denis', 'Komarov', 'denis.komarov@example.com', '+79002345671', 4500.00, 'BK20240418003', false, '2024-04-18 19:10:00', NOW()),

-- Student bookings (usually economy class)
(1, 'Maxim', 'Zaitsev', 'maxim.zaitsev@example.com', '+79003456782', 1800.00, 'BK20240417001', true, '2024-04-17 12:30:00', NOW()),
(2, 'Daria', 'Nikolaeva', 'daria.nikolaeva@example.com', '+79004567893', 1200.00, 'BK20240417002', false, '2024-04-17 14:45:00', NOW()),
(NULL, 'Roman', 'Antonov', 'roman.antonov@example.com', '+79005678904', 1200.00, 'BK20240417003', true, '2024-04-17 16:00:00', NOW()),

-- Tourist bookings (often to popular destinations)
(1, 'Oleg', 'Ermakov', 'oleg.ermakov@example.com', '+79006789015', 9600.00, 'BK20240416001', true, '2024-04-16 10:20:00', NOW()),
(2, 'Alina', 'Grigorieva', 'alina.grigorieva@example.com', '+79007890126', 4800.00, 'BK20240416002', true, '2024-04-16 11:45:00', NOW()),
(NULL, 'Vadim', 'Kovalchuk', 'vadim.kovalchuk@example.com', '+79008901237', 7200.00, 'BK20240416003', false, '2024-04-16 13:10:00', NOW()),

-- Last minute bookings
(1, 'Kirill', 'Pavlov', 'kirill.pavlov@example.com', '+79009012348', 2500.00, 'BK20240422004', false, '2024-04-22 20:30:00', NOW()),
(2, 'Polina', 'Samoilova', 'polina.samoilova@example.com', '+79000123459', 5000.00, 'BK20240422005', false, '2024-04-22 21:45:00', NOW()),
(NULL, 'Timofey', 'Gusev', 'timofey.gusev@example.com', '+79001234561', 3750.00, 'BK20240422006', false, '2024-04-22 22:15:00', NOW()),

-- Corporate bookings
(1, 'Vladislav', 'Sobolev', 'vladislav.sobolev@company.com', '+79002345672', 18000.00, 'BK20240419001', true, '2024-04-19 09:00:00', NOW()),
(2, 'Kristina', 'Vlasova', 'kristina.vlasova@company.com', '+79003456783', 13500.00, 'BK20240419002', true, '2024-04-19 10:30:00', NOW()),
(NULL, 'Artem', 'Medvedev', 'artem.medvedev@company.com', '+79004567894', 9000.00, 'BK20240419003', false, '2024-04-19 12:15:00', NOW()),

-- International travelers
(1, 'George', 'Smith', 'george.smith@example.com', '+79101234567', 4400.00, 'BK20240421001', true, '2024-04-21 15:30:00', NOW()),
(2, 'Sophie', 'Martin', 'sophie.martin@example.com', '+79102345678', 2200.00, 'BK20240421002', true, '2024-04-21 16:45:00', NOW()),
(NULL, 'Hans', 'Müller', 'hans.muller@example.com', '+79103456789', 3300.00, 'BK20240421003', false, '2024-04-21 18:20:00', NOW()),

-- Elderly passengers
(1, 'Petr', 'Vasiliev', 'petr.vasiliev@example.com', '+79005678905', 3000.00, 'BK20240414001', true, '2024-04-14 11:20:00', NOW()),
(2, 'Valentina', 'Sidorova', 'valentina.sidorova@example.com', '+79006789016', 1500.00, 'BK20240414002', true, '2024-04-14 13:45:00', NOW()),
(NULL, 'Viktor', 'Nikolaev', 'viktor.nikolaev@example.com', '+79007890127', 2250.00, 'BK20240414003', false, '2024-04-14 15:10:00', NOW()),

-- Regular commuters
(1, 'Sergey', 'Kuznetsov', 'sergey.kuznetsov@example.com', '+79008901238', 2400.00, 'BK20240413001', true, '2024-04-13 08:30:00', NOW()),
(2, 'Olga', 'Petrova', 'olga.petrova@example.com', '+79009012349', 2400.00, 'BK20240413002', true, '2024-04-13 08:45:00', NOW()),
(NULL, 'Andrey', 'Sokolov', 'andrey.sokolov@example.com', '+79000123460', 1200.00, 'BK20240413003', true, '2024-04-13 09:15:00', NOW()),

-- Weekend travelers
(1, 'Dmitry', 'Kozlov', 'dmitry.kozlov@example.com', '+79001234562', 3600.00, 'BK20240412001', true, '2024-04-12 17:20:00', NOW()),
(2, 'Anastasia', 'Novikova', 'anastasia.novikova@example.com', '+79002345673', 1800.00, 'BK20240412002', false, '2024-04-12 18:45:00', NOW()),
(NULL, 'Mikhail', 'Orlov', 'mikhail.orlov@example.com', '+79003456784', 2700.00, 'BK20240412003', true, '2024-04-12 19:30:00', NOW());
