from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
from utils.network_util import generate_chart_section, generate_table_section
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
from utils.system_util import create_dashboard_cards, create_app_bar, create_footer


BYTES_IN_GB = 1024 * 1024 * 1024

# The line `app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.BOOTSTRAP])` is
# initializing a Dash application.
app = Dash(
    __name__,
    external_stylesheets=[dbc.themes.DARKLY, dbc.icons.BOOTSTRAP],
)

# Page contents
content = html.Div(
    children=[
        create_app_bar(),
        html.Hr(),
        create_dashboard_cards(),
        generate_chart_section(),
        generate_table_section(),
        create_footer(),
        dcc.Interval(
            id="interval-component",
            interval=15000,  # Refresh every 15000ms (15 seconds)
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
    style={
        "padding": "2rem",
    },
)


def create_chart(chart_type, title=None, labels=None, values=None, x=None, y=None):
    colors = ["#FFA500", "#0d6efd"]

    if chart_type == "pie":
        return px.pie(
            names=labels,
            values=values,
            title=title,
            color=labels,
            color_discrete_map={label: color for label, color in zip(labels, colors)},
        )
    elif chart_type == "bar":
        return px.bar(
            x=x,
            y=y,
            labels=labels,
            title=title,
            color=x,
            color_discrete_map={label: color for label, color in zip(x, colors)},
        )
    else:
        raise ValueError("Unsupported chart type")


# Update graph layout to ensure dark theme even when empty
def update_dark_theme_graph(fig, showlegend=False):
    """
    Update the graph's layout to match the dark theme, including empty state.
    :param fig: The plotly figure object.
    :return: The updated figure object with dark theme settings.
    """
    fig.update_layout(
        paper_bgcolor="#303030",  # Dark background for the paper
        plot_bgcolor="#222222",  # Dark plot background
        title_font_color="white",  # White title color
        font=dict(color="white"),  # White font color for labels and text
        xaxis=dict(
            title_font=dict(color="white"),  # X-axis title font color
            tickfont=dict(color="white"),  # X-axis tick color
        ),
        yaxis=dict(
            title_font=dict(color="white"),  # Y-axis title font color
            tickfont=dict(color="white"),  # Y-axis tick color
        ),
        # Handle empty state
        showlegend=showlegend,  # Optional: hide legend if not needed
        margin=dict(l=0, r=0, t=30, b=30),  # Tighten margins
        # In case of empty data, make sure background remains dark
        annotations=(
            [
                {
                    "text": "No Data Available",
                    "xref": "paper",
                    "yref": "paper",
                    "showarrow": False,
                    "font": {"size": 20, "color": "white"},
                    "align": "center",
                }
            ]
            if not fig.data
            else []
        ),
    )
    return fig


def fetch_all_data():
    try:
        return (
            device_info(),
            get_cpu_usage(),
            get_memory_usage(),
            get_disk_usage(),
            get_network_speed(),
            get_network_io(),
            get_active_connections(),
            get_all_processes(),
        )
    except Exception as e:
        print(f"Error fetching data: {e}")
        return [None] * 7


# Callback to update dashboard data every 15 seconds
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
    """
    Callback function to update the dashboard every `interval-component`.
    Retrieves system metrics, updates graphs, and tables dynamically.
    """
    # Collect data from system metrics functions
    (
        device_info_data,
        cpu_usage,
        memory_data,
        disk_data,
        network_speed,
        network_io,
        connections,
        processes,
    ) = fetch_all_data()

    model = device_info_data.get("model", "N/A")
    device_name = device_info_data.get("device_name", "Unknown")
    ip_address = device_info_data.get("ip_address", "0.0.0.0")
    battery = device_info_data.get("battery_percentage", 0)
    battery_percentage = f"{battery}%" if battery is not None else "N/A"
    os_name = device_info_data.get("os_name", "Unknown")
    os_arch = device_info_data.get("os_arch", "Unknown")
    cpu_used = device_info_data.get("cpu_used", 0)
    cpu_data = f"{cpu_usage or 0}%"

    # Memory data
    memory_used = memory_data.get("used", 0)
    memory_free = memory_data.get("free", 0)
    memory_total = memory_data.get("total", 0)
    memory_percent = memory_data.get("percent", 0)
    memory_used_gb = (
        f"{memory_used / BYTES_IN_GB:.2f}/{memory_total / BYTES_IN_GB:.2f} GB"
        if memory_total > 0
        else "N/A"
    )

    # Disk data
    disk_used = disk_data.get("used", 0)
    disk_free = disk_data.get("free", 0)
    disk_total = disk_data.get("total", 0)
    disk_percent = disk_data.get("percent", 0)
    disk_used_gb = (
        f"{disk_used / BYTES_IN_GB:.2f}/{disk_total / BYTES_IN_GB:.2f} GB"
        if disk_total > 0
        else "N/A"
    )

    # Network Speed Graph
    network_speed_fig = create_chart(
        chart_type="bar",
        title="Network Speed",
        labels={"x": "Network", "y": "Speed (Mbps)"},
        x=["Upload", "Download"],
        y=[
            network_speed.get("upload_speed", 0),
            network_speed.get("download_speed", 0),
        ],
    )

    network_speed_fig = update_dark_theme_graph(network_speed_fig)

    # Network I/O Graph
    network_io_fig = create_chart(
        chart_type="bar",
        title="Network I/O",
        labels={"x": "Network I/O", "y": "Bytes"},
        x=["Bytes Sent", "Bytes Received"],
        y=[
            network_io.get("bytes_sent", 0),
            network_io.get("bytes_received", 0),
        ],
    )

    # Update layout for dark theme
    network_io_fig = update_dark_theme_graph(network_io_fig)

    # Memory Usage
    memory_usage_fig = create_chart(
        chart_type="pie",
        title="Memory Usage",
        labels=["Used", "Free"],
        values=[memory_used, memory_free],
    )

    # Update layout for dark theme
    memory_usage_fig = update_dark_theme_graph(memory_usage_fig, showlegend=True)

    # Disk Usage
    disk_usage_fig = create_chart(
        chart_type="pie",
        title="Disk Usage",
        labels=["Used", "Free"],
        values=[disk_used, disk_free],
    )

    # Update layout for dark theme
    disk_usage_fig = update_dark_theme_graph(disk_usage_fig, showlegend=True)

    # Sort by CPU usage (descending) and limit to top 15
    process_rows = [
        html.Tr(
            [
                html.Td(proc.get("pid", "N/A")),
                html.Td(proc.get("name", "Unknown")),
                html.Td(proc.get("username", "Unknown")),
                html.Td(proc.get("status", "N/A")),
                html.Td(f"{proc.get('cpu_percent', 0):.1f}%"),
                html.Td(f"{proc.get('memory_percent', 0):.1f}%"),
            ]
        )
        for proc in sorted(
            processes, key=lambda x: x.get("cpu_percent", 0), reverse=True
        )[:15]
    ]

    # Limit to the first 15 connections
    connections_rows = [
        html.Tr(
            [
                html.Td(conn.get("local_address", "N/A")),
                html.Td(conn.get("remote_address", "N/A")),
                html.Td(conn.get("status", "Unknown")),
                html.Td(conn.get("type", "Unknown")),
            ]
        )
        for conn in connections[:15]
    ]

    return [
        model,
        device_name,
        ip_address,
        battery_percentage,
        os_name,
        os_arch,
        cpu_data,
        f"{memory_percent}%",
        f"{disk_percent}%",
        cpu_used,
        memory_used_gb,
        disk_used_gb,
        network_speed_fig,
        network_io_fig,
        memory_usage_fig,
        disk_usage_fig,
        process_rows,
        connections_rows,
    ]


# server = app.server
# main
if __name__ == "__main__":
    app.run_server(debug=True)
