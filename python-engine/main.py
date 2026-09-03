from my_database import get_all_devices, insert_discovered_devices, monitor_all_and_update
from discovery import get_local_network    

if __name__ == "__main__":
    network = get_local_network()

    try:
        insert_discovered_devices(network)
        print("Discovered devices inserted successfully.")
    except Exception as e:
        print(f"An error occurred while inserting discovered devices: {e}")

#you can try to use other functions as well, for example, to retrieve all devices from the database:
    try:
        devices = get_all_devices()
        for device in devices:
            print(device)
    except Exception as e:
        print(f"An error occurred while retrieving devices: {e}")

#or simply you can monitor all the devices in the database and update their status in the database:
    try:
        monitor_all_and_update()
        print("All devices monitored and status updated.")
    except Exception as e:
        print(f"An error occurred while monitoring devices: {e}")   