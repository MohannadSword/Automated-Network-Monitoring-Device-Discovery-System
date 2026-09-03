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
    proc = ping_host(ip)
    output = proc.stdout or ""
    # include stderr when ping fails to aid debugging
    if proc.returncode != 0:
        output = (output + "\n" + (proc.stderr or "")).strip()

    result = parse_ping(device_id, output, ip)
    return result


def monitor_all_devices(devices):
    monitor_results = {}

    for device in devices:
        # normalize device representation (support dicts returned by DB)
        if isinstance(device, dict):
            device_id = device.get("id") or device.get("device_id")
            ip = device.get("ip_address") or device.get("ip")
            hostname = device.get("hostname") or ip
        else:
            # accept tuple forms: (id, hostname, ip) or (id, ip)
            if len(device) == 3:
                device_id, hostname, ip = device
            elif len(device) == 2:
                device_id, ip = device
                hostname = ip
            else:
                # unexpected shape; skip
                continue

        result = monitor_device(device_id, ip)
        monitor_results[hostname] = result

    return monitor_results





