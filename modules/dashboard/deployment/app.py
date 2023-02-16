import dash_bootstrap_components as dbc
import dash
from dash import Dash, Input, Output, html, dcc, callback
from dash_iconify import DashIconify
import dash_mantine_components as dmc

import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# bootstrap theme
# https://bootswatch.com/lux/
external_stylesheets = [dbc.themes.LITERA]

app = dash.Dash(__name__, 
                external_stylesheets = external_stylesheets, 
                use_pages = True)

path_directory = "ds_project/modules/dashboard/deployment/"

#hardcoded paths
# logo from https://www.vectorstock.com/royalty-free-vector/road-sun-shine-logo-vector-17131606
import base64
with open(path_directory + "assets/SolarExit_logo.jpeg", "rb") as file:
    logo = "data:image/jpg;base64, {}".format(base64.b64encode(file.read()).decode("utf-8"))


navbar = dbc.NavbarSimple(
    children = [
        dbc.NavItem(dbc.NavLink("Karte", href="/karte")),
        dbc.NavItem(dbc.NavLink("Tabelle", href="/rohdaten"))
    ],
    brand=dbc.Row([
            dbc.Col(html.Img(src=logo, height="30px")),
            dbc.Col(dbc.NavbarBrand("Road to Renewables", className="ml-1")),
                    ]),
    brand_href="/",
    color="primary",
    dark=True,
    sticky= 'top',
    fluid=True,
    #className="mb-4",
)

# embedding the navigation bar
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    navbar,
    dash.page_container
])

if __name__ == '__main__':
	app.run_server(host="0.0.0.0", port=8050, debug = False)