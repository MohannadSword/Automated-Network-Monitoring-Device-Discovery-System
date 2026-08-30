import platform
import subprocess
import re




def parse_ping(device_id,output, ip):
    result = {
        "device_id": device_id,
        "ip": ip,
        "status": "DOWN",
        "latency_ms": None
    }

    packet_match = re.search(
        r'(\d+) packets transmitted, (\d+) received',
        output
    )

    if packet_match and int(packet_match.group(2)) > 0:
        result["status"] = "UP"

    latency_match = re.search(
        r'rtt min/avg/max/mdev = [\d.]+/([\d.]+)/[\d.]+/[\d.]+ ms',
        output
    )

    if latency_match:
        result["latency_ms"] = float(latency_match.group(1))

    return result


def ping_host(host):
    param = '-n' if platform.system().lower() == 'windows' else '-c'
    command = ['ping', param, '5', host]
    return subprocess.run(
        command,
        capture_output=True,
        text=True
    )



def monitor_device(device_id, ip):
    ping_output = ping_host(ip).stdout
    result = parse_ping(device_id, ping_output, ip)
    return result


def monitor_all_devices(devices):
    monitor_results = {}

    for device in devices:
        if isinstance(device, dict):
            device_id = device.get("device_id")
            ip = device.get("ip")
        else:
            device_id, hostname, ip = device

        result = monitor_device(device_id, ip)
        monitor_results[hostname] = result

    return monitor_results





