import psutil as ps

def get_all_processes():
    """
    Get a list of all running processes with details.
    :return: List of dictionaries containing process details.
    """
    processes = []
    for proc in ps.process_iter(attrs=['pid', 'name', 'username', 'status']):
        try:
            process_info = proc.info
            process_info["cpu_percent"] = proc.cpu_percent(interval=0.1)  # CPU usage percentage
            process_info["memory_percent"] = proc.memory_percent()  # Memory usage percentage
            processes.append(process_info)
        except (ps.NoSuchProcess, ps.AccessDenied):
            # Skip processes that can't be accessed
            continue

    return processes

def kill_process(pid):
    """
    Kill a process by its PID.
    :param pid: Process ID.
    :return: True if successfully terminated, False otherwise.
    """
    try:
        proc = ps.Process(pid)
        proc.terminate()  # Request termination
        proc.wait(timeout=3)  # Wait for process to terminate
        return True
    except (ps.NoSuchProcess, ps.AccessDenied, ps.TimeoutExpired):
        return False
    
    
# if __name__ == "__main__":
#     # Test the functions
#     print("All Processes:")
#     for process in get_all_processes()[:20]:  # Display first 5 processes for brevity
#         print(process)

#     # test_pid = 1  # Replace with a valid PID to test
#     # print(f"\nDetails of process {test_pid}:")
#     # print(get_process_by_pid(test_pid))

#     # print(f"\nAttempting to kill process {test_pid}:")
#     # print("Success" if kill_process(test_pid) else "Failed")