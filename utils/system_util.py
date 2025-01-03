from dash import html
import dash_bootstrap_components as dbc

# Common styles
CARD_STYLE = {
    "textAlign": "start",
    "borderRadius": "16px",
    "color": "#FFFFFF"
}

LABEL_STYLE = {
    "fontSize": "16px", "color": "#969696"
}

CARD_DATA = [
    {"title": "CPU", "id": "cpu-usage", "sub_id": "cpu-used", "icon_name": "bi bi-cpu",},
    {
        "title": "MEMORY",
        "id": "memory-usage",
        "sub_id": "memory-used",
        "icon_name": "bi bi-memory",
    },
    {
        "title": "DISK",
        "id": "disk-usage",
        "sub_id": "disk-used",
        "icon_name": "bi bi-hdd",
    },
]


# App Bar Component
def create_app_bar():
    return dbc.Row(
        [
            dbc.Col(
                html.Div(
                    [
                        html.Img(
                            src=r"assets/veya.jpg",
                            width="50px",
                            style={"marginRight": "10px"},
                        ),
                        html.H2("Desert Eagle", className="display-7", style={"color": "#ADD8E6"},),
                    ],
                    style={"display": "flex", "alignItems": "center"},
                ),
                width="auto",
            ),
            dbc.Col(
                html.H3("System Monitoring Dashboard", style={"marginLeft": "10rem", "color": "#ADD8E6",},),
            ),
        ],
        justify="between",
        style={"padding": "1rem 2rem"},
    )


# Card Component Utilities
def create_card_item(id, label):
    return html.Div(
        [
            html.H4(label, style={"fontSize": "16px", "color": "#969696"}),
            html.H4(id=id, style={"fontSize": "16px", "color": "#ADD8E6"}),
        ],
        style={
            "display": "flex",
            "justifyContent": "space-between",
            "width": "100%",
            "alignItems": "center",
        },
    )


def create_card(title, id, sub_id, icon_name):
    return dbc.Col(
        dbc.Card(
            dbc.CardBody(
                [
                    html.Div(
                        [
                            html.H4(
                                title, style={"fontSize": "18px", "color": "#969696"}
                            ),
                            html.I(className=icon_name, style={"fontSize": "1.5rem", "color": "#ADD8E6",},),
                        ],
                        style={
                            "display": "flex",
                            "justifyContent": "space-between",
                            "width": "100%",
                            "alignItems": "center",
                        },
                    ),
                    html.H3(
                        id=id,
                        style={
                            "fontSize": "40px",
                            "color": "#ADD8E6",
                            "fontWeight": "bold",
                        },
                    ),
                    create_card_item(sub_id, "Used"),
                ]
            ),
            className="border-0 shadow-lg",
            style=CARD_STYLE,
        ),
    )


# Information Card Utilities
def create_info_item(label, id):
    return html.Div(
        [
            html.H3(label, style={"fontSize": "16px", "color": "#ADD8E6"}),
            html.H3(id=id, style={"fontSize": "18px", "color": "#FFFFFF"}),
        ]
    )


def create_info_pair(label1, id1, label2, id2):
    return html.Div(
        [
            create_info_item(label1, id1),
            dbc.Col(
                create_info_item(label2, id2),
                style={"marginTop": "1rem"},
            ),
        ]
    )


def create_info_card():
    return dbc.Col(
        dbc.Card(
            dbc.CardBody(
                dbc.Row(
                    [
                        dbc.Col(
                            create_info_pair(
                                "MODEL:",
                                "model",
                                "DEVICE NAME:",
                                "device-name",
                            ),
                            width=5,
                        ),
                        dbc.Col(
                            create_info_pair(
                                "IP ADDRESS:",
                                "ip-address",
                                "BATTERY:",
                                "battery-percentage",
                            ),
                            width=4,
                        ),
                        dbc.Col(
                            create_info_pair(
                                "OS NAME:",
                                "os-name",
                                "OS ARCH:",
                                "os-arch",
                            ),
                            width=3,
                        ),
                    ],
                    className="g-4",
                )
            ),
            className="border-0 shadow-lg",
            style=CARD_STYLE,
        ),
        style={"flex": "2"},
    )


# Main Cards Component
def create_dashboard_cards():
    return dbc.Row(
        [
            create_info_card(),
            *[create_card(**card) for card in CARD_DATA],
        ],
        style={"paddingBottom": "2rem"},
    )
