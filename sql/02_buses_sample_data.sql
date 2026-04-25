-- Sample data for Buses table
-- SQL script to populate buses with test data

INSERT INTO tickets_bus (registration_number, bus_type, total_seats, seats_per_row, has_ac, has_wifi, has_toilet, description, is_active, created_at) VALUES
-- Standard buses (economy class)
('AB1234', 'standard', 45, 4, false, false, false, 'Standard economy bus for intercity routes', true, NOW()),
('BC5678', 'standard', 45, 4, false, false, false, 'Standard economy bus with basic amenities', true, NOW()),
('CD9012', 'standard', 45, 4, false, false, false, 'Standard bus for short to medium routes', true, NOW()),
('DE3456', 'standard', 45, 4, false, false, false, 'Economy class bus with comfortable seats', true, NOW()),
('EF7890', 'standard', 45, 4, false, false, false, 'Standard intercity bus', true, NOW()),

-- Comfort buses (business class)
('FG2345', 'comfort', 36, 3, true, true, false, 'Comfort class bus with air conditioning and WiFi', true, NOW()),
('GH6789', 'comfort', 36, 3, true, true, false, 'Business class bus with premium amenities', true, NOW()),
('HI0123', 'comfort', 36, 3, true, true, false, 'Comfortable bus for long distance travel', true, NOW()),
('IJ4567', 'comfort', 36, 3, true, true, false, 'Premium comfort bus with spacious seating', true, NOW()),
('KL8901', 'comfort', 36, 3, true, true, false, 'Luxury comfort bus with modern amenities', true, NOW()),

-- Luxury buses (first class)
('MN3456', 'luxury', 28, 2, true, true, true, 'Luxury first class bus with all premium amenities', true, NOW()),
('OP7890', 'luxury', 28, 2, true, true, true, 'Executive luxury bus with premium service', true, NOW()),
('QR1234', 'luxury', 28, 2, true, true, true, 'First class luxury coach with full amenities', true, NOW()),
('ST5678', 'luxury', 28, 2, true, true, true, 'Premium luxury bus for VIP passengers', true, NOW()),
('UV9012', 'luxury', 28, 2, true, true, true, 'Ultra-luxury bus with exclusive features', true, NOW()),

-- Additional standard buses for high-demand routes
('WX2345', 'standard', 45, 4, false, false, false, 'Additional standard bus for peak hours', true, NOW()),
('YZ6789', 'standard', 45, 4, false, false, false, 'Standard bus for regional routes', true, NOW()),
('ZA0123', 'standard', 45, 4, false, false, false, 'Economy bus with reliable service', true, NOW()),

-- Additional comfort buses
('AB4567', 'comfort', 36, 3, true, true, false, 'Comfort bus for business travelers', true, NOW()),
('CD8901', 'comfort', 36, 3, true, true, false, 'Premium comfort bus with enhanced features', true, NOW()),

-- Additional luxury buses for premium routes
('EF2345', 'luxury', 28, 2, true, true, true, 'Luxury coach for international routes', true, NOW()),
('GH6789', 'luxury', 28, 2, true, true, true, 'First class bus with concierge service', true, NOW()),

-- Mini buses for shorter routes
('IJ0123', 'standard', 25, 4, false, false, false, 'Mini bus for regional connections', true, NOW()),
('KL3456', 'standard', 25, 4, false, false, false, 'Compact bus for local routes', true, NOW()),
('MN7890', 'comfort', 20, 3, true, false, false, 'Mini comfort bus for premium local service', true, NOW()),

-- Special purpose buses
('OP1234', 'luxury', 18, 2, true, true, true, 'VIP luxury bus for special events', true, NOW()),
('QR5678', 'comfort', 32, 3, true, true, true, 'Tourist bus with full amenities', true, NOW()),
('ST9012', 'standard', 40, 4, true, false, true, 'Standard bus with AC and toilet for long routes', true, NOW()),

-- Express buses
('UV2345', 'comfort', 30, 3, true, true, false, 'Express comfort bus for fast connections', true, NOW()),
('WX6789', 'luxury', 24, 2, true, true, true, 'Express luxury bus with premium service', true, NOW()),
('YZ0123', 'standard', 42, 4, true, false, false, 'Express standard bus with basic amenities', true, NOW());
