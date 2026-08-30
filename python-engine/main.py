from my_database import get_ips, insert_monitoring_result


if __name__ == "__main__":
    try:
        insert_monitoring_result()
        print("Monitoring results inserted successfully.")
    except Exception as e:
        print(f"An error occurred while inserting monitoring results: {e}")