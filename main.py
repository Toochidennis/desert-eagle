import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import psutil as ps
from modules.network_stats import get_network_speed, get_network_io, get_active_connections
from modules.process_stats import get_all_processes
from modules.system_stats import get_cpu_usage, get_disk_usage, get_disk_io_stats, get_memory_usage, get_per_cpu_usage, get_swap_usage


# Initialize app
app = dash.Dash(__name__)

# App layout
app.layout = html.Div([
    html.H1('System Monitoring Dashboard', style={'text-align: center'}),
    
    # CPU and meory usage graph
    html.Div([
        dcc.Graph(id='cpu-usage'),
        dcc.Graph(id='memory-usage')
    ], style={'display': 'flex', 'justify-content': 'space-between'}),
    
    # Network Stats (Speed and I/O)
    html.Div([
         html.H3("Network Speed (1s Interval)"),
        dcc.Graph(id='network-speed'),
        html.H3("Network I/O (Total Sent/Received)"),
        dcc.Graph(id='network-io')
    ]),
    
     # Active Processes
    html.Div([
        html.H3("Active Processes"),
        html.Table(id='process-table')
    ])
])

# Define callbacks for updating the graphs and tables
@app.callback(
    [
        Output('cpu-usage', 'figure'),
        Output('memory-usage', 'figure'),
        Output('network-speed', 'figure'),
        Output('network-io', 'figure'),
        Output('process-table', 'children'),
    ],
    Input('update-interval', 'n_intervals')
)

def update_dashboard(_):
    # Get system stats
    cpu_usage = get_cpu_usage()
    memory_usage = get_memory_usage()
    
    network_speed = get_network_speed(interval=1)
    network_io = get_network_io()

    processes = get_all_processes()

    # CPU Usage Graph
    cpu_fig = {
        'data': [go.Bar(x=["CPU"], y=[cpu_usage])],
        'layout': go.Layout(title="CPU Usage (%)", showlegend=False)
    }

    # Memory Usage Graph
    memory_fig = {
        'data': [go.Bar(x=["Memory"], y=[memory_usage])],
        'layout': go.Layout(title="Memory Usage (%)", showlegend=False)
    }

    # Network Speed Graph
    network_speed_fig = {
        'data': [
            go.Bar(x=["Upload", "Download"], y=[network_speed['upload_speed'], network_speed['download_speed']])
        ],
        'layout': go.Layout(title="Network Speed (Bytes/sec)", showlegend=False)
    }

    # Network I/O Graph
    network_io_fig = {
        'data': [
            go.Bar(x=["Bytes Sent", "Bytes Received"], y=[network_io['bytes_sent'], network_io['bytes_received']])
        ],
        'layout': go.Layout(title="Network I/O", showlegend=False)
    }

    # Active Processes Table
    process_rows = []
    for proc in processes[:10]:  # Display first 10 processes for brevity
        row = html.Tr([html.Td(proc["pid"]), html.Td(proc["name"]), html.Td(proc["username"]), html.Td(proc["status"]),
                       html.Td(f"{proc['cpu_percent']}%"), html.Td(f"{proc['memory_percent']}%")])
        process_rows.append(row)

    process_table = html.Table([
        html.Thead(html.Tr([html.Th("PID"), html.Th("Name"), html.Th("User"), html.Th("Status"),
                            html.Th("CPU %"), html.Th("Memory %")])),
        html.Tbody(process_rows)
    ])

    return cpu_fig, memory_fig, network_speed_fig, network_io_fig, process_table

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)