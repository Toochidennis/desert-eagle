from dash import html, dcc
import dash_bootstrap_components as dbc

CARD_STYLE = {
    "textAlign": "start",
    "borderRadius": "16px",
}
CHART_TITLE_STYLE = {
    "fontSize": "20px",
    "color": "#ADD8E6",
}
TABLE_HEADER_STYLE = {
    "color": "#ADD8E6",  # Light blue header text
}

def create_chart_card(chart_id):
    """
    Create a reusable card component for displaying charts.
    :param chart_id: ID for the chart's dcc.Graph component.
    :param title: Title of the chart.
    :return: dbc.Col containing the chart card.
    """
    return dbc.Col(
        dbc.Card(
            dbc.CardBody(
                [
                    dcc.Graph(
                        id=chart_id,
                        style={"height": "300px"},
                    ),
                ]
            ),
            class_name="shadow-lg border-0",
            style=CARD_STYLE,
        ),
    )


def generate_chart_section():
    """
    Create a row of chart components.
    :return: dbc.Row containing chart cards.
    """
    return dbc.Row(
        [
            create_chart_card("network-speed"),
            create_chart_card("network-io"),
            create_chart_card("memory-pie"),
            create_chart_card("disk-pie"),
        ],
    )


def create_connection_table():
    """
    Create a table for displaying network connections.
    :return: dbc.Table component for connections.
    """
    return dbc.Table(
        [
            html.Thead(
                html.Tr(
                    [
                        html.Th("Local Address"),
                        html.Th("Foreign Address"),
                        html.Th("Status"),
                        html.Th("Type"),
                    ]
                )
            ),
            html.Tbody(id="connection-table"),
        ],
        bordered=True,
        hover=True,
        striped=True,
        responsive=True,
    )


def create_process_table():
    """
    Create a table for displaying process details.
    :return: dbc.Table component for processes.
    """
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
            html.Tbody(id="process-table"),
        ],
        bordered=True,
        hover=True,
        striped=True,
        responsive=True,
    )


def create_table_card(title, content):
    """
    Create a reusable card component for tables.
    :param title: Title of the card.
    :param content: Content to display inside the card.
    :return: dbc.Card containing the table.
    """
    return dbc.Card(
        dbc.CardBody(
            [
                html.H3(
                    title,
                    style=CHART_TITLE_STYLE
                ),
                html.Div(
                    content,
                    style={
                        "marginTop": "1rem",
                        "maxHeight": "400px",
                        "overflowY": "auto",
                    },
                ),
            ]
        ),
        class_name="shadow-lg border-0",
        style=CARD_STYLE,
    )


def generate_table_section():
    """
    Create a section containing the process and connection tables.
    :return: html.Div containing table cards.
    """
    return html.Div(
        [
            html.Div(
                create_table_card("Processes", create_process_table()),
                style={
                    "flex": "1.5",
                    "marginRight": "1rem",
                },
            ),
            html.Div(
                create_table_card("Connections", create_connection_table()),
                style={
                    "flex": "1",
                },
            ),
        ],
        style={
            "display": "flex",
            "justifyContent": "space-between",
            "marginTop": "2rem",
            "width": "100%",
        },
    )
