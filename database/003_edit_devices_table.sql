ALTER TABLE devices
    ADD COLUMN mac_address VARCHAR(17) NULL AFTER ip_address,
    ADD COLUMN vendor VARCHAR(100) NULL AFTER mac_address,
    ADD COLUMN network_address VARCHAR(43) NULL AFTER vendor,
    ADD COLUMN source VARCHAR(30) NULL AFTER network_address,
    ADD COLUMN updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP AFTER created_at;