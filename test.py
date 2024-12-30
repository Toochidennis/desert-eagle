from dash import Dash, html, dcc, callback, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px


app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

color_discrete_sequence = ['#0a9396','#94d2bd','#e9d8a6','#ee9b00', '#ca6702', '#bb3e03', '#ae2012']


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
        html.Thead(html.Tr([
            html.Th("PID"),
            html.Th("Name"),
            html.Th("User"),
            html.Th("Status"),
            html.Th("CPU %"),
            html.Th("Memory %")])),
        html.Tbody(process_rows)
    ])

    return cpu_fig, memory_fig, network_speed_fig, network_io_fig, process_table



if __name__ == '__main__':
    app.run_server(debug=True)
    


def get_page_content(self):
    card_data = [{"title": "Total ports", "data": "80% "}] * 5

    return html.Div(
        id="network-page",
        children=[
            dbc.Card(
                dbc.CardBody(
                    children=[
                        dbc.Row(
                            children=[get_card_component(**card) for card in card_data]
                        ),
                        dbc.Row(
                            children=[get_card_component(**card) for card in card_data]
                        ),
                    ]
                ),
                class_name="shadow-lg bg-light border-0",
            ),
            dbc.Row(
                dbc.Col(
                    [
                        html.H4(
                            "Connections",
                            style={"margin-top": "2rem"},
                        ),
                        html.Div(
                            dbc.RadioItems(
                                id="connections-radios",
                                class_name="btn-group",
                                input_class_name="btn-check",
                                label_class_name="btn btn-outline-dark",
                                label_checked_class_name="active",
                                options=[
                                    {"label": "All", "value": "all"},
                                    {
                                        "label": "Established",
                                        "value": "established",
                                    },
                                    {"label": "Listening", "value": "listening"},
                                ],
                                value="all",
                            ),
                            className="radio-group",
                            style={"margin-top": "2rem"},
                        ),
                        dbc.Table(
                            [
                                html.Thead(
                                    html.Tr(
                                        [
                                            html.Th("Local address"),
                                            html.Th("Foreign address"),
                                            html.Th("Status"),
                                            html.Th("Type"),
                                        ]
                                    )
                                ),
                                html.Tbody(
                                    [
                                        html.Tr(
                                            [
                                                html.Td("Arthur"),
                                                html.Td("Dent"),
                                                html.Td("Dent"),
                                                html.Td("Dent"),
                                            ]
                                        ),
                                        html.Tr(
                                            [
                                                html.Td("Arthur"),
                                                html.Td("Dent"),
                                                html.Td("Dent"),
                                                html.Td("Dent"),
                                            ]
                                        ),
                                    ]
                                ),
                            ],
                            bordered=True,
                            hover=True,
                            striped=True,
                            responsive=True,
                            style={"margin-top": "2rem"},
                        ),
                    ]
                )
            ),
        ],
        style={"margin-top": "2em"},
    )
