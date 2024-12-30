from dash import html, dcc
import dash_bootstrap_components as dbc

CARD_STYLE = {
    "textAlign": "start",
    "backgroundColor": "#FFFFFF",
    "borderRadius": "14px",
}


def get_row_component(id, title):
    return dbc.Col(
        dbc.Card(
            dbc.CardBody(
                [
                    html.H3(
                        title,
                        style={
                            "fontSize": "18px",
                            "color": "#26325D",
                        },
                    ),
                    dcc.Graph(
                        id=id,
                        style={"height": "300px"},
                    ),
                ]
            ),
            class_name="shadow-lg border-0",
            style=CARD_STYLE,
        ),
    )


def get_chart_component():
    return dbc.Row(
        [
            get_row_component(
                id="network-speed",
                title="Network Speed (Bytes/sec)",
            ),
            get_row_component(
                id="network-io",
                title="Network I/O",
            ),
            get_row_component(
                id="memory-graph",
                title="Memory Usage",
            ),
        ],
    )


def get_connection_table():
    return dbc.Table(
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
                id="connection-table"
            ),
        ],
        bordered=True,
        hover=True,
        striped=True,
        responsive=True,
        # style={"margin-top": "2rem"},
    )


def get_process_table():
    return dbc.Table(
        [
            html.Thead(
                html.Tr(
                    [
                        html.Th("PID"),
                        html.Th("Name"),
                        html.Th("User"),
                        html.Th("Status"),
                        html.Th("CPU %"),
                        html.Th("Memory %"),
                    ]
                )
            ),
            html.Tbody(
                id="process-table"
            ),
        ],
        bordered=True,
        hover=True,
        striped=True,
        responsive=True,
        # style={"margin-top": "2rem"},
    )


def get_table_item(title, content):
    return dbc.Card(
        dbc.CardBody(
            [
                html.H3(
                    title,
                    style={
                        "fontSize": "18px",
                        "color": "#26325D",
                    },
                ),
               html.Div(
                    content,
                    style={
                        "maxHeight": "400px",  # Set the height of the scrollable area
                        "overflowY": "auto",  # Enable vertical scrolling
                        "overflowX": "auto",  # Enable horizontal scrolling (if needed)
                    },
                ),
            ]
        ),
        class_name="shadow-lg border-0",
        style=CARD_STYLE,
    )


def get_table_component():
    return html.Div(
        [
            html.Div(
                get_table_item("Processes", get_process_table()),
                style={
                    "flex": "1.5",  # Allocate more space to the process table
                    "marginRight": "1rem",  # Add spacing between the tables
                },
            ),
            html.Div(
                get_table_item("Connections", get_connection_table()),
                style={
                    "flex": "1",  # Allocate less space to the connection table
                },
            ),
        ],
        style={
            "display": "flex",
            "justifyContent": "space-between",
            "marginTop": "2rem",
            "width": "100%"
        },
    )
