CREATE TABLE monitoring_results(
	id BIGINT AUTO_INCREMENT PRIMARY KEY ,
    device_id INT NOT NULL,
	device_status VARCHAR(20) NOT NULL,
	latency_ms DECIMAL(10,2),
    checked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY(device_id)
		REFERENCES devices(id)
);
