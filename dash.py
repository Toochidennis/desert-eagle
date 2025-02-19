import pandas as pd
import plotly.express as px
from dash import Dash, html, dash_table, dcc, callback, input, output

df = pd.read_csv('housing.csv')

app = Dash()

app.layout = [
    html.Div(children = 'dashboard')
]

if __name__=='__main__':
    app.run(debug=True)