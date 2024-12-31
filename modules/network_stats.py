import psutil as ps
import socket
import time
import platform
import subprocess


def get_network_io():
    """
    Get total network I/O (bytes sent and received).
    :return: Dictionary with total bytes sent and received.
    """

    net_io = ps.net_io_counters()
    return {
        "bytes_sent": net_io.bytes_sent,  # Total bytes sent
        "bytes_received": net_io.bytes_recv,  # Total bytes received
        "packets_sent": net_io.packets_sent,  # Total packets sent
        "packets_received": net_io.packets_recv,  # Total packets received
    }


def get_network_speed(interval=1):
    """
    Calculate network upload and download speeds.
    :param interval: Time interval in seconds to measure speed.
    :return: Dictionary with upload and download speeds in bytes/sec.
    """

    net_io_1 = ps.net_io_counters()
    time.sleep(interval)
    net_io_2 = ps.net_io_counters()

    upload_speed = (net_io_2.bytes_sent - net_io_1.bytes_sent) / interval
    download_speed = (net_io_2.bytes_recv - net_io_1.bytes_recv) / interval

    return {
        "upload_speed": upload_speed,  # Bytes uploaded per second
        "download_speed": download_speed,  # Bytes downloaded per second
    }


def get_active_connections():
    """
    Get details of active network connections.
    :return: List of dictionaries containing connection details.
    """

    connections = ps.net_connections()
    active_connections = []

    for conn in connections:
        active_connections.append(
            {
                "local_address": f"{conn.laddr.ip}:{conn.laddr.port}" if conn.laddr else None,
                "remote_address": f"{conn.raddr.ip}:{conn.raddr.port}" if conn.raddr else None,
                "status": conn.status,
                "type": "TCP" if conn.type == socket.SOCK_STREAM else "UDP",
            }
        )

    return active_connections


def get_private_ip():
    try:
        # Create a temporary socket and connect to an external address
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))
            private_ip = s.getsockname()[0]
        return private_ip
    except Exception as e:
        return socket.gethostbyname(socket.gethostname())


def get_system_model():
    try:
        if platform.system() == "Windows":
            # Windows: Use WMIC to get model
            model = subprocess.run(
                ["wmic", "computersystem", "get", "model"],
                capture_output=True,
                text=True,
            )
            return model.stdout.split("\n")[2].strip()
        elif platform.system() == "Linux":
            # Linux: Read from the DMI data
            # manufacturer = subprocess.run("cat /sys/class/dmi/id/sys_vendor", shell=True, capture_output=True, text=True)
            model = subprocess.run(
                "cat /sys/class/dmi/id/product_name",
                shell=True,
                capture_output=True,
                text=True,
            )
            return model.stdout.split("\n")[2].strip()
        elif platform.system() == "Darwin":
            # macOS: Use system_profiler for details
            model = subprocess.check_output(
                "sysctl -n hw.model", shell=True, universal_newlines=True
            ).strip()
            return f"Apple {model}"
        else:
            return "Unsupported OS"
    except Exception as e:
        print(str(e))
        return "Unknown"


def get_device_info():
    # Device Name
    device_name = socket.gethostname()

    # Battery Percentage
    battery = ps.sensors_battery()
    battery_percent = battery.percent if battery else "No"

    # IP Address
    private_ip = get_private_ip()
    
    # cpu frequency
    freq = ps.cpu_freq()
    max = f"{freq.max / 1000:.2f}"
    current = f"{freq.current / 1000:.2f}"
    cpu_used = f"{current}/{max} GHz"

    # Get system model and OS information
    system_arch = platform.uname().machine  # For general architecture (e.g., x86_64)
    system_name = platform.uname().system  # OS name
    os_release = platform.release()
    system_model = get_system_model()

    return {
        "model": system_model,
        "device_name": device_name,
        "ip_address": private_ip,
        "battery_percentage": battery_percent,
        "os_name": f"{system_name} {os_release}",
        "os_arch": system_arch,
        "cpu_used": cpu_used,
    }


# if __name__ == "__main__":
#     # Test the functions
#     print("Network I/O:", get_network_io())
#     print("Network Speed (1s interval):", get_network_speed(interval=1))
#     print("Active Connections:")
#     for conn in get_active_connections():
#         print(conn)
