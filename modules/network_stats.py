import psutil as ps
import socket
import time

def get_network_io():
    """
    Get total network I/O (bytes sent and received).
    :return: Dictionary with total bytes sent and received.
    """
    
    net_io = ps.net_io_counters()
    return {
        "bytes_sent": net_io.bytes_sent,      # Total bytes sent
        "bytes_received": net_io.bytes_recv, # Total bytes received
        "packets_sent": net_io.packets_sent, # Total packets sent
        "packets_received": net_io.packets_recv # Total packets received
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
        "upload_speed": upload_speed,       # Bytes uploaded per second
        "download_speed": download_speed   # Bytes downloaded per second
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
            "type": "TCP" if conn.type == socket.SOCK_STREAM else "UDP"
            }
        )

    return active_connections

if __name__ == "__main__":
    # Test the functions
    print("Network I/O:", get_network_io())
    print("Network Speed (1s interval):", get_network_speed(interval=1))
    print("Active Connections:")
    for conn in get_active_connections():
        print(conn)