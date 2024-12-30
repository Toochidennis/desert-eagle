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
        "icon_name": "bi bi-cpu",
    },
    {
      "title": "MEMORY",
       "id": "memory-usage",
        "icon_name": "bi bi-memory",
    },
    {
        "title": "DISK",
         "id": "disk-usage",
        "icon_name": "bi bi-hdd",
    },
    {
        "title": "CPU",
        "id": "cpu-usage1",
        "icon_name": "bi bi-cpu",
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
                title=title,
                style={
                    "fontSize": "16px",
                    "color": "#969696",
                },
            ),
            html.H4(
                
                style={
                    "fontSize": "16px",
                    "color": "#969696",
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


def get_card_component(title, id, icon_name):
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
                    get_card_item("used", "Used",),
                    get_card_item("free", "Free",),
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
            html.H3(id=id, style={"fontSize": "20px"}),
        ],
    )


def get_info_card():
    return dbc.Col(
        dbc.Card(
            dbc.CardBody(
                [
                    html.Div(
                        [
                            info_item("USERNAME:", "username"),
                            info_item("DEVICE NAME:", "device-name"),
                        ],
                        style={
                            "display": "flex",
                            "justifyContent": "space-between",
                            "alignItems": "center", 
                        },
                    ),
                    html.Div(
                        [
                            info_item("IP ADDRESS:", "ip-address"),
                            info_item("BATTERY:", "battery-percentage"),
                        ],
                        style={
                            "marginTop": "1rem",
                            "display": "flex",
                            "justifyContent": "space-between",
                            "alignItems": "center",
                        },
                    ),
                ]
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
