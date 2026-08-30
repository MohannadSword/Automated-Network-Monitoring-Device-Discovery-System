import os 
import mysql.connector
from dotenv import load_dotenv
from monitor import monitor_all_devices

load_dotenv()


def get_connection():

    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
        port=os.getenv("DB_PORT", 3306)
    )


def get_ips():
    cnx = get_connection()

    

    try :
        cursor = cnx.cursor()

        cursor.execute('SELECT id, hostname, ip_address FROM devices')

        return [row[0:3] for row in cursor.fetchall()]
    finally : 
        cursor.close()
        cnx.close()

def get_monitoring_data():

    devices = get_ips()
    monitoring_data = []

    for hostname, data in monitor_all_devices(devices).items():

        device_id = data["device_id"]
        status = data["status"]
        latency = data["latency_ms"]

        monitoring_data.append(
            (device_id, status, latency)
        )

    return monitoring_data


def insert_monitoring_result():

    cnx = get_connection()

    sql = """
INSERT INTO monitoring_results (device_id, device_status , latency_ms) VALUES (%s, %s, %s)
    """
    values = get_monitoring_data()

    try :
        cursor = cnx.cursor()

        cursor.executemany(sql, values)

        cnx.commit()
    finally : 
        cursor.close()
        cnx.close()
