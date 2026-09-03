import os 
import mysql.connector
from dotenv import load_dotenv
from monitor import monitor_device
from discovery import discover_devices, get_local_network

load_dotenv()


def get_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
        port=int(os.getenv("DB_PORT", 3306))
    )


def insert_discovered_devices(network=None, device_type=None):
    """Discover devices and insert them into the database"""
    
    if network is None:
        network = get_local_network()
    
    devices = discover_devices(network)

    try:
        cnx = get_connection()
    except mysql.connector.Error as err:
        print(f"Database connection error: {err}")
        return
    except Exception as err:
        print(f"Error getting database connection: {err}")
        return
    
    sql = """
    INSERT INTO devices (ip_address, mac_address, vendor, network_address, source, device_type, status)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    ON DUPLICATE KEY UPDATE
        mac_address = VALUES(mac_address),
        vendor = VALUES(vendor),
        source = VALUES(source),
        updated_at = CURRENT_TIMESTAMP
    """
    
    try:
        cursor = cnx.cursor()
        
        for device in devices:
            values = (
                device["ip"],
                device["mac"],
                device["vendor"],
                network,
                "nmap-discovery",
                device_type,
                "up"
            )
            cursor.execute(sql, values)
        
        cnx.commit()
        print(f"Successfully inserted/updated {len(devices)} devices")
        
    except mysql.connector.Error as err:
        print(f"Error inserting devices: {err}")
        cnx.rollback()
    finally:
        cursor.close()
        cnx.close()


def get_all_devices():
    """Retrieve all devices from database"""
    
    cnx = get_connection()
    
    try:
        cursor = cnx.cursor(dictionary=True)
        cursor.execute("""
            SELECT id, hostname, ip_address, mac_address, vendor, 
                   network_address, source, device_type, status, created_at, updated_at
            FROM devices
        """)
        return cursor.fetchall()
    finally:
        cursor.close()
        cnx.close()


def insert_manual_device(ip_address, mac_address=None, vendor=None, device_type="host", hostname=None):
    """Manually insert a single device into the database"""
    
    cnx = get_connection()
    
    sql = """
    INSERT INTO devices (hostname, ip_address, mac_address, vendor, source, device_type, status)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    
    try:
        cursor = cnx.cursor()
        values = (
            hostname,
            ip_address,
            mac_address,
            vendor,
            "manual-entry",
            device_type,
            "unknown"
        )
        cursor.execute(sql, values)
        cnx.commit()
        print(f"Successfully inserted device: {ip_address}")
        
    except mysql.connector.Error as err:
        print(f"Error inserting device: {err}")
        cnx.rollback()
    finally:
        cursor.close()
        cnx.close()


def update_device_status(device_id, status, latency_ms=None):
    """Update device status and insert monitoring result"""
    
    cnx = get_connection()
    
    try:
        cursor = cnx.cursor()
        
        # Update device status
        cursor.execute(
            "UPDATE devices SET status = %s, updated_at = CURRENT_TIMESTAMP WHERE id = %s",
            (status, device_id)
        )
        
        # Insert monitoring result
        cursor.execute(
            "INSERT INTO monitoring_results (device_id, device_status, latency_ms) VALUES (%s, %s, %s)",
            (device_id, status, latency_ms)
        )
        
        cnx.commit()
        
    except mysql.connector.Error as err:
        print(f"Error updating device status: {err}")
        cnx.rollback()
    finally:
        cursor.close()
        cnx.close()


def monitor_all_and_update():
    """Monitor all devices and update their status in database"""
    
    devices = get_all_devices()
    
    for device in devices:
        result = monitor_device(device["id"], device["ip_address"])
        update_device_status(
            device["id"],
            result["status"],
            result["latency_ms"]
        )
        print(f"Updated {device['ip_address']}: {result['status']}")
