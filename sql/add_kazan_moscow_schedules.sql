-- Add schedules for Kazan -> Moscow route
-- This will fix the issue where Kazan -> Moscow route exists but has no schedules

INSERT INTO tickets_schedule (
    route_id, 
    bus_id, 
    departure_time, 
    arrival_time, 
    price_multiplier, 
    is_active, 
    created_at, 
    updated_at
) VALUES 
-- Schedule for today
(4, 1, NOW() + INTERVAL '10 hours', NOW() + INTERVAL '10 hours' + INTERVAL '14 hours 30 minutes', 1.0, true, NOW(), NOW()),

-- Schedule for tomorrow
(4, 1, NOW() + INTERVAL '1 day' + INTERVAL '10 hours', NOW() + INTERVAL '1 day' + INTERVAL '10 hours' + INTERVAL '14 hours 30 minutes', 1.0, true, NOW(), NOW()),

-- Schedule for day after tomorrow
(4, 1, NOW() + INTERVAL '2 days' + INTERVAL '10 hours', NOW() + INTERVAL '2 days' + INTERVAL '10 hours' + INTERVAL '14 hours 30 minutes', 1.0, true, NOW(), NOW()),

-- Schedule for next week
(4, 1, NOW() + INTERVAL '7 days' + INTERVAL '10 hours', NOW() + INTERVAL '7 days' + INTERVAL '10 hours' + INTERVAL '14 hours 30 minutes', 1.0, true, NOW(), NOW()),

-- Additional evening schedules
(4, 1, NOW() + INTERVAL '1 day' + INTERVAL '18 hours', NOW() + INTERVAL '1 day' + INTERVAL '18 hours' + INTERVAL '14 hours 30 minutes', 1.0, true, NOW(), NOW()),

(4, 1, NOW() + INTERVAL '2 days' + INTERVAL '18 hours', NOW() + INTERVAL '2 days' + INTERVAL '18 hours' + INTERVAL '14 hours 30 minutes', 1.0, true, NOW(), NOW());
