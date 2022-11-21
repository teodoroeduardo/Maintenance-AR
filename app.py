import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import random as rnd
import plotly.graph_objects as go

app = dash.Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.BOOTSTRAP],
title="Utilização de AR nas práticas de Engenharia de Manutenção",suppress_callback_exceptions=True)

dropdown_menu = dbc.DropdownMenu([
    dbc.DropdownMenuItem("TEXTO A", header=True),
    dbc.DropdownMenuItem(divider=True),
    dbc.DropdownMenuItem("TEXTO B"),
    dbc.DropdownMenuItem("TEXTO C"),
    dbc.DropdownMenuItem("TEXTO D"),
    dbc.DropdownMenuItem("TEXTO E"),
],label="Menu",color="light",size="lg")

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.Div("ISSO É UM TEXTO")),
        dbc.Col(html.Div("ENGENHARIA DE MANUTENÇÃO",style={'fontSize':50,'text-align':'center'})),
        dbc.Col(dropdown_menu),
    ],align="center",className="text-center"),
    html.Hr(),
    dbc.Row([
        dbc.Col([dash.page_container])
    ])
],fluid=True)

if __name__ == "__main__":
    app.run(debug=True)