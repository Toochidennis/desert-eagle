from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objs as go
import psutil
from utils.network_util import (
    get_chart_component as charts,
    get_table_component as tables,
)
from modules.system_stats import (
    get_cpu_usage,
    get_disk_usage,
    get_memory_usage,
)
from modules.network_stats import (
    get_active_connections,
    get_network_io,
    get_network_speed,
    get_device_info as device_info,
)
from modules.process_stats import get_all_processes
from utils.system_util import cards, app_bar

# Initialize app
app = Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.BOOTSTRAP],
)

# Page contents
content = html.Div(
    children=[
        app_bar,
        html.Hr(),
        cards,
        charts(),
        tables(),
        dcc.Interval(
            id="interval-component",
            interval=5000,  # Refresh every 5000ms (5 seconds)
            n_intervals=0,
        ),
    ],
)

# App layout
app.layout = dbc.Container(
    [
        content,
    ],
    fluid=True,
    style={"backgroundColor": "#FBFBFB"},
)


@app.callback(
    [
        Output("model", "children"),
        Output("device-name", "children"),
        Output("ip-address", "children"),
        Output("battery-percentage", "children"),
        Output("os-name", "children"),
        Output("os-arch", "children"),
        Output("cpu-usage", "children"),
        Output("memory-usage", "children"),
        Output("disk-usage", "children"),
        Output("cpu-used", "children"),
        Output("memory-used", "children"),
        Output("disk-used", "children"),
        Output("network-speed", "figure"),
        Output("network-io", "figure"),
        Output("memory-pie", "figure"),
        Output("disk-pie", "figure"),
        Output("process-table", "children"),
        Output("connection-table", "children"),
    ],
    [Input("interval-component", "n_intervals")],
)
def render_page_content(n_intervals):
    # Fetch data
    device_info_data = device_info()
    cpu_usage = get_cpu_usage()
    memory_usage = get_memory_usage()
    disk_usage = get_disk_usage()
    network_speed = get_network_speed(interval=1)
    network_io = get_network_io()
    processes = get_all_processes()
    connections = get_active_connections()

    # Network Speed Graph
    network_speed_fig = go.Figure(
        data=[
            go.Bar(
                x=["Upload", "Download"],
                y=[network_speed["upload_speed"], network_speed["download_speed"]],
            )
        ]
    )

    # Network I/O Graph
    network_io_fig = go.Figure(
        data=[
            go.Bar(
                x=["Bytes Sent", "Bytes Received"],
                y=[network_io["bytes_sent"], network_io["bytes_received"]],
            )
        ]
    )

    # Memory Usage
    memory_usage_fig = go.Figure(
        data=[
            go.Pie(
                labels=["Used", "Free"],
                values=[
                    memory_usage["used"],
                    memory_usage["free"],
                ],
                hole=0.5,
                marker=dict(
                    colors=["#0d6efd", "#6c757d"],  # Bootstrap colors
                ),
            )
        ]
    )

    # Disk Usage
    disk_usage_fig = go.Figure(
        data=[
            go.Pie(
                labels=["Used", "Free"],
                values=[
                    disk_usage["used"],
                    disk_usage["free"],
                ],
                hole=0.5,
                marker=dict(
                    colors=["#0d6efd", "#6c757d"],
                ),
            )
        ]
    )

    # Active Processes Table
    process_rows = []
    for proc in processes:  # Display first 10 processes for brevity
        row = html.Tr(
            [
                html.Td(proc["pid"].strip()),
                html.Td(proc["name"].strip()),
                html.Td(proc["username"].strip()),
                html.Td(proc["status"].strip()),
                html.Td(f"{proc['cpu_percent']:.1f}%"),
                html.Td(f"{proc['memory_percent']:.1f}%"),
            ],
        )
        process_rows.append(row)

    # Active Connections Table
    connections_rows = []
    for conn in connections:  # Display first 10 processes for brevity
        row = html.Tr(
            [
                html.Td(conn["local_address"]),
                html.Td(conn["remote_address"]),
                html.Td(conn["status"]),
                html.Td(conn["type"]),
            ]
        )
        connections_rows.append(row)

    return [
        device_info_data["model"],
        device_info_data["device_name"],
        device_info_data["ip_address"],
        f"{device_info_data['battery_percentage']}%",
        device_info_data["os_name"],
        device_info_data["os_arch"],
        f"{cpu_usage}%",
        f"{memory_usage['percent']}%",
        f"{disk_usage['percent']}%",
        device_info_data["cpu_used"],
        f"{memory_usage['used'] / (1024*1024*1024):.2f}/{memory_usage['total'] / (1024*1024*1024):.2f} GB",
        f"{disk_usage['used'] / (1024*1024*1024):.2f}/{disk_usage['total'] / (1024*1024*1024):.2f} GB",
        network_speed_fig,
        network_io_fig,
        memory_usage_fig,
        disk_usage_fig,
        process_rows,
        connections_rows,
    ]


# main
if __name__ == "__main__":
    app.run_server(debug=True)
