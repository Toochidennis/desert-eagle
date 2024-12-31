from dash import html
import dash_bootstrap_components as dbc

# from modules.network_stats import get_network_speed, get_network_io, get_active_connections
CARD_STYLE = {
    "textAlign": "start",
    "backgroundColor": "#FFFFFF",
    "borderRadius": "16px",
}

CARD_DATA = [
    {
        "title": "CPU",
        "id": "cpu-usage",
        "sub_id": "cpu-used",
        "icon_name": "bi bi-cpu",
    },
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

app_bar = dbc.Row(
    [
        dbc.Col(
            html.Div(
                [
                    html.Img(
                        src=r"assets/veya.jpg",
                        width="50px",
                        style={
                            "marginRight": "10px",
                        },
                    ),
                    html.H2("Desert Eagle", className="display-7"),
                ],
                style={"display": "flex", "alignItems": "center"},
            ),
            width="auto",
        ),
        dbc.Col(
            html.H3(
                "System Monitoring Dashboard",
                style={"marginLeft": "10rem"},
            ),
        ),
    ],
    justify="between",
    style={"padding": "1rem 2rem"},
)


def get_card_item(id, title):
    return html.Div(
        [
            html.H4(
                title,
                style={
                    "fontSize": "16px",
                    "color": "#969696",
                },
            ),
            html.H4(
                id=id,
                style={
                    "fontSize": "16px",
                    "color": "#4469F9",
                },
            ),
        ],
        style={
            "display": "flex",
            "justifyContent": "space-between",
            "width": "100%",
            "alignItems": "center",
        },
    )


def get_card_component(title, id, sub_id, icon_name):
    return dbc.Col(
        dbc.Card(
            dbc.CardBody(
                [
                    html.Div(
                        [
                            html.H4(
                                title,
                                style={
                                    "fontSize": "18px",
                                    "color": "#969696",
                                },
                            ),
                            html.I(
                                className=icon_name,
                                style={
                                    "fontSize": "1.5rem",
                                },
                            ),
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
                            "fontSize": "30px",
                            "color": "#26325D",
                            "fontWeight": "bold",
                        },
                    ),
                    get_card_item(sub_id, "Used"),
                ]
            ),
            class_name="border-0 shadow-lg",
            style=CARD_STYLE,
        ),
    )


def info_item(title, id):
    return html.Div(
        [
            html.H3(title, style={"fontSize": "16px"}),
            html.H3(id=id, style={"fontSize": "18px"}),
        ],
    )


def card_item(title1, id1, title2, id2):
    return html.Div(
        [
            info_item(title1, id1),
            dbc.Col(
                info_item(title2, id2),
                style={"marginTop": "1rem"},
            ),
        ],
    )


def get_info_card():
    return dbc.Col(
        dbc.Card(
            dbc.CardBody(
                dbc.Row(
                    [
                        dbc.Col(
                            card_item(
                                title1="MODEL:",
                                id1="model",
                                title2="DEVICE NAME:",
                                id2="device-name",
                            ),
                            width=5,
                        ),
                        dbc.Col(
                            card_item(
                                title1="IP ADDRESS:",
                                id1="ip-address",
                                title2="BATTERY:",
                                id2="battery-percentage",
                            ),
                            width=4,
                        ),
                        dbc.Col(
                            card_item(
                                title1="OS NAME:",
                                id1="os-name",
                                title2="OS ARCH:",
                                id2="os-arch",
                            ),
                            width=3,
                        ),
                    ],
                    className="g-4",
                )
            ),
            class_name="border-0 shadow-lg",
            style=CARD_STYLE,
        ),
        style={
            "flex": "2",
        },
    )


cards = dbc.Row(
    [
        get_info_card(),
        *[get_card_component(**card) for card in CARD_DATA],
    ],
    style={"paddingBottom": "2rem"},
)
