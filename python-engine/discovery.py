import subprocess
import re
import ipaddress
import psutil
import socket

def get_local_network():

    for interface, addrs in psutil.net_if_addrs().items():

        for addr in addrs:

            if addr.family == socket.AF_INET and not addr.address.startswith('127.'):

                ip = addr.address
                netmask = addr.netmask

                if ip and netmask:
                    network = ipaddress.IPv4Network(
                        f"{ip}/{netmask}",
                        strict=False
                    )

                    return str(network)

    raise RuntimeError("No Active IPv4 network interface found.")


def discover_devices(network=None):

    if network is None:
        network = get_local_network()

    command = ["nmap", "-sn", "-PR", network]

    result = subprocess.run(
        command,
        capture_output=True,
        text=True
    )

    devices = []
    current_device = None

    for line in result.stdout.splitlines():

        match = re.search(
            r"Nmap scan report for (?:.*\()?(\d+\.\d+\.\d+\.\d+)\)?",
            line
        )

        if match:

            if current_device:
                devices.append(current_device)

            current_device = {
                "ip": match.group(1),
                "mac": None,
                "vendor": None
            }

        mac_match = re.search(
            r"MAC Address:\s+([0-9A-Fa-f:]+)\s+\((.*?)\)",
            line
        )

        if mac_match and current_device:
            current_device["mac"] = mac_match.group(1)
            current_device["vendor"] = mac_match.group(2)

    if current_device:
        devices.append(current_device)

    return devices

