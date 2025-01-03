import psutil as ps


async def get_cpu_usage():
    """
    Get the percentage of CPU usage.
    :return: CPU usage as a percentage.
    """
    return ps.cpu_percent(interval=1)


async def get_per_cpu_usage():
    """
    Get CPU usage per core.
    :return: List of CPU usage percentages for each core.
    """
    return ps.cpu_percent(interval=1, percpu=True)


async def get_memory_usage():
    """
    Get memory usage details.
    :return: Dictionary with total, used, and percentage of memory usage.
    """

    memory = ps.virtual_memory()
    return {
        "used": memory.used,
        "free": memory.free,
        "total": memory.total,
        "percent": memory.percent,
    }


async def get_swap_usage():
    """
    Get swap memory usage details.
    :return: Dictionary with total, used, and percentage of swap usage.
    """

    swap = ps.swap_memory()
    return {
        "used": swap.used,
        "free": swap.free,
        "total": swap.total,
        "percent": swap.percent,
    }


async def get_disk_usage(partition="/"):
    """
    Get disk usage details for a specific partition.
    :param partition: Partition to check (default: '/').
    :return: Dictionary with total, used, and percentage of disk usage.
    """

    disk = ps.disk_usage(partition)
    return {
        "used": disk.used,
        "free": disk.free,
        "total": disk.total,
        "percent": disk.percent,
    }


async def get_disk_io_stats():
    """
    Get disk I/O statistics (read and write operations).
    :return: Dictionary with read and write stats in bytes.
    """

    disk_io = ps.disk_io_counters()
    return {"read_bytes": disk_io.read_bytes, "write_bytes": disk_io.write_bytes}


# if __name__ == "__main__":
#     # Test the functions
#     print("CPU Usage:", get_cpu_usage(), "%")
#     print("Per CPU Usage:", get_per_cpu_usage())
#     print("Memory Usage:", get_memory_usage())
#     print("Swap Usage:", get_swap_usage())
#     print("Disk Usage:", get_disk_usage())
#     print("Disk I/O Stats:", get_disk_io_stats())
