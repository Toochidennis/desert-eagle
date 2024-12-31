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
    get_disk_io_stats,
    get_memory_usage,
    get_per_cpu_usage,
    get_swap_usage,
)
from modules.network_stats import (
    get_active_connections as connections,
    get_network_io as network_io,
    get_network_speed as network_speed,
    get_device_info as device_info,
)
from modules.process_stats import get_all_processes as processes
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
        # Output('disk-usage', 'title'),
        # Output('network-io', 'figure'),
        # Output('process-table', 'children'),
    ],
    [Input("interval-component", "n_intervals")],
)
def render_page_content(n_intervals):
    # Fetch data
    device_info_data = device_info()
    cpu_usage = get_cpu_usage()
    memory_usage = get_memory_usage()
    disk_usage = get_disk_usage()

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
    ]


# main
if __name__ == "__main__":
    app.run_server(debug=True)
