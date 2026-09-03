# Network Monitoring Tool

A Python-based network monitoring tool that checks the availability and latency of network devices and stores monitoring results in a MySQL database.

The project is being developed incrementally, starting with basic device monitoring and database integration, with automated network discovery planned for a future version.

## Current Features

* Retrieve network devices and IP addresses from a MySQL database
* Ping devices automatically
* Determine whether a device is **UP** or **DOWN**
* Measure network latency
* Parse ping output and extract monitoring metrics
* Store monitoring results in MySQL
* Separate device information from monitoring history
* Use environment variables for database credentials

## Current Architecture

The current version follows a simple separation of responsibilities:

```text
                MySQL
                  │
                  │
             Device IPs
                  │
                  ▼
             monitor.py
                  │
                  │ Ping
                  ▼
              Network
                  │
                  ▼
          Monitoring Results
                  │
                  ▼
                MySQL
```


## Modules

### `my_database.py`

Handles communication with the MySQL database.

Responsibilities include:

* Establishing the database connection
* Retrieving devices/IP addresses
* Inserting monitoring results
* Performing basic database operations

Database credentials are loaded through environment variables rather than being hard-coded in the source code.

### `monitor.py`

Contains the network monitoring logic.

Responsibilities include:

* Executing ping commands
* Parsing ping output
* Determining device availability
* Calculating/extracting latency information
* Producing structured monitoring results

A monitoring result follows a structure similar to:

```python
{
    "device_id": 1,
    "ip": "192.168.1.1",
    "status": "UP",
    "latency_ms": 5.28
}
```

### `main.py`

Acts as the entry point of the application and coordinates the monitoring workflow.

## Database Design

The project uses MySQL to maintain two main concepts:

### Devices

Contains the devices that should be monitored.

Example:

```text
device_id | hostname  | ip_address
----------|-----------|------------
1         | router-01 | 192.168.1.1
2         | pc-01     | 192.168.1.10
```

### Monitoring Results

Stores the results of individual monitoring checks.

Example:

```text
result_id | device_id | status | latency_ms
----------|-----------|--------|-----------
1         | 1         | UP     | 5.28
2         | 2         | UP     | 1.42
3         | 1         | DOWN   | NULL
```

This separation allows the device inventory to remain independent from its monitoring history.

## Requirements

* Python 3
* MySQL Server
* `mysql-connector-python`
* Linux environment with the `ping` command available

Python dependencies are listed in:

```text
requirements.txt
```

## Installation

Clone the repository:

```bash
git clone https://github.com/<your-username>/<repository-name>.git
cd <repository-name>
```

Create a virtual environment:

```bash
python3 -m venv .venv
```

Activate it:

```bash
source .venv/bin/activate
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

## Configuration

Create a `.env` file in the project root:

```text
DB_HOST=localhost
DB_USER=your_database_user
DB_PASSWORD=your_database_password
DB_NAME=your_database_name
DB_PORT=3306
```

The `.env` file contains local credentials and should **not** be committed to Git.

A `.env.example` file is provided as a template.

## Running the Tool

Activate the virtual environment:

```bash
source .venv/bin/activate
```

Then run:

```bash
python3 main.py
```

The application retrieves the configured devices, performs monitoring checks, and stores the results in the database.

## Current Limitations

The current version depends on devices already being present in the database.

It does **not yet automatically discover devices on the network**.

It also does not currently provide:

* Automatic network scanning
* Device classification
* Network topology discovery
* SNMP monitoring
* Bandwidth/interface monitoring
* Web dashboard
* Alerting system

These are potential future improvements.

## Roadmap

### Phase 1 — Basic Monitoring

* [x] MySQL database integration
* [x] Retrieve devices from database
* [x] Ping devices
* [x] Determine UP/DOWN status
* [x] Measure latency
* [x] Store monitoring results

### Phase 2 — Network Discovery

* [x] Automatically scan the local network
* [x] Detect connected devices
* [x] Retrieve IP and MAC addresses
* [x] Identify device vendors
* [x] Automatically add discovered devices to the database

### Phase 3 — Device Classification

* [ ] Identify hosts
* [ ] Identify routers
* [ ] Identify switches
* [ ] Add confidence-based classification
* [ ] Handle unknown devices

### Phase 4 — Advanced Monitoring

* [ ] SNMP monitoring
* [ ] Interface statistics
* [ ] Packet loss tracking
* [ ] Historical performance analysis
* [ ] Alerting
* [ ] Monitoring dashboard

## Project Goal

The long-term goal is to develop a lightweight network monitoring system capable of automatically discovering network devices, maintaining a device inventory, monitoring device availability and performance, and storing historical monitoring data.

The project is being developed as a practical Python networking project, with an emphasis on automation, network monitoring, database integration, and modular software design.

## License

This project is currently intended as a learning and portfolio project.
