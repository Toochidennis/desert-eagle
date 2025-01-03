from dash import Dash, html, dcc, callback, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
from app import fetch_data_sync
import time


if __name__ == '__main__':
    start_time = time.perf_counter()  # Start the timer

    # Your code block
    (
        cpu_usage,
        memory_data,
        disk_data,
        network_speed,
        network_io,
        connections,
        processes,

    ) = fetch_data_sync()

    end_time = time.perf_counter()  # End the timer

    execution_time = end_time - start_time
    print(f"Execution time: {execution_time:.2f} seconds")
    print(f"cpu: {cpu_usage}")
    print(f"memory: {memory_data}")
    print(f"disk: {disk_data}")
