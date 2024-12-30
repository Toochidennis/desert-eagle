from modules.process_stats import get_all_processes
import psutil
from dash import Dash, html, dcc, callback, Input, Output


class ProcessPage:
    def __init__(self, html, dcc, dbc):
        self.html = html
        self.dcc = dcc
        self.dbc = dbc

    def get_page_content(self):
        table_header = self.html.Thead(
            self.html.Tr(
                [
                    self.html.Th("PID"),
                    self.html.Th("Name"),
                    self.html.Th("User"),
                    self.html.Th("Status"),
                    self.html.Th("CPU %"),
                    self.html.Th("Memory %"),
                ]
            )
        )

        return self.html.Div(
            [
                self.html.H3("Process Monitor", style={"margin-bottom": "20px"}),
                self.dbc.Row(
                    [
                        self.dbc.Col(
                            self.dbc.Card(
                                self.dbc.CardBody(
                                    [
                                        self.html.H4("Total CPU Usage"),
                                        self.html.H4(id="total-cpu"),
                                    ]
                                ),
                                class_name="shadow bg-dark text-white",
                            ),
                            width=3,
                        ),
                        self.dbc.Col(
                            self.dbc.Card(
                                self.dbc.CardBody(
                                    [
                                        self.html.H4("Total Memory Usage"),
                                        self.html.H4(id="total-memory"),
                                    ]
                                ),
                                class_name="shadow bg-dark text-white",
                            ),
                            width=3,
                        ),
                    ],
                    style={"margin-bottom": "20px"},
                ),
                self.dbc.Table(
                    children=[
                        table_header,
                        self.html.Tbody(id="process-table-body"),
                    ],
                    bordered=True,
                    hover=True,
                    striped=True,
                    responsive=True,
                ),
                self.dcc.Interval(
                    id="process-interval",
                    interval=2000,  # Update every 2 seconds
                    n_intervals=0,
                ),
            ],
            style={"margin-top": "20px"},
        )

   # Callbacks for ProcessPage
    @staticmethod
    def register_callbacks(app):
        @app.callback(
            [
                Output("process-table-body", "children"),
                Output("total-cpu", "children"),
                Output("total-memory", "children"),
            ],
            Input("process-interval", "n_intervals"),
        )
        def update_process_page(n_intervals):
            processes = get_all_processes()
            total_cpu = psutil.cpu_percent()
            total_memory = psutil.virtual_memory().percent

            table_rows = [
                html.Tr([html.Td(proc["pid"]), html.Td(proc["name"]), html.Td(f"{proc['cpu_percent']:.1f}")])
                for proc in processes
            ]
            return table_rows, f"CPU: {total_cpu}%", f"Memory: {total_memory}%"