from dash import Dash, html, dcc, callback, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objs as go

# from modules.network_stats import get_network_speed, get_network_io, get_active_connections
# from modules.process_stats import get_all_processes
# from modules.system_stats import get_cpu_usage, get_disk_usage, get_disk_io_stats, get_memory_usage, get_per_cpu_usage, get_swap_usage

# Initialize app
app = Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.BOOTSTRAP],
)

color_discrete_sequence = [
    "#0a9396",
    "#94d2bd",
    "#e9d8a6",
    "#ee9b00",
    "#ca6702",
    "#bb3e03",
    "#ae2012",
]

SIDEBAR_STYLE = {
    "position": "fixed",
    "top": "0",
    "left": "0",
    "bottom": "0",
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem, 1rem",
}

sidebar = html.Div(
    [
        html.Div(
            [
                html.Img(
                    src="https://www.flaticon.com/free-icons/eagle.svg",
                    style={"margin-right": "10px", "font-size": "24px"},
                ),
                html.H2("Desert Eagle", className="display-7"),
            ],
            style={"display": "flex", "align-items": "center"},
        ),
        html.Hr(),
        dbc.Nav(
            [
                dbc.NavLink("Home", href="/", active="exact"),
                dbc.NavLink("Network", href="/network-page", active="exact"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)

content = html.Div(
    id="page-content",
    children=[],
    style=CONTENT_STYLE,
)


def get_card_component(title, data):
    return dbc.Col(
        dbc.Card(
            dbc.CardBody(
                [
                    html.H4(title),
                    html.H4(data),
                ]
            ),
            color="white",
            class_name='shadow-lg bg-dark border-0',
            style={"textAlign": "center", "margin-bottom": "24px"},
        ),
    )


network_page = html.Div(
    id="network-page",
    children=[
        # html.H2(
        #     "Networking Statistics",
        #     style={"textAlign": "center", "padding-bottom": "1rem"},
        # ),
        dbc.Card(
            dbc.CardBody( 
                children=[
                    dbc.Row(
                        [
                            get_card_component(title="Total ports", data="30"),
                            get_card_component(title="Total ports", data="30"),
                            get_card_component(title="Total ports", data="30"),
                            get_card_component(title="Total ports", data="30"),
                            get_card_component(title="Total ports", data="30"),
                        ]
                    ),
                    dbc.Row(
                        children=[
                            get_card_component(title="Total ports", data="30"),
                            get_card_component(title="Total ports", data="30"),
                            get_card_component(title="Total ports", data="30"),
                            get_card_component(title="Total ports", data="30"),
                            get_card_component(title="Total ports", data="30"),
                        ]
                    ),
                ]
            ),
            class_name='shadow-lg bg-light border-0'
        ),
        dbc.Row(dbc.Col([
            html.H4('Connections'),
            html.Div([
                dbc.RadioItems(
                    id='connections-radios',
                    
                )
            ])
        ]))
    ],
    style={"margin-top": "2em"},
)


# App layout
app.layout = html.Div(
    [
        dcc.Location(id="url"),
        sidebar,
        content,
    ]
)


@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname == "/":
        pass
    else:
        return network_page


# main
if __name__ == "__main__":
    app.run_server(debug=True)
