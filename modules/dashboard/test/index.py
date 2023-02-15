
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from dash import dcc, html

# import all pages in the app
from app import app
from apps import karte, rohdaten, home

#hardcoded paths
# logo from https://www.vectorstock.com/royalty-free-vector/road-sun-shine-logo-vector-17131606
import base64
with open("/home/jan/Uni/DS-Project/modules/dashboard/test/apps/assets/RoadToRenewables.jpg", "rb") as file:
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
    brand_href="#",
    color="primary",
    dark=True,
    sticky= 'top',
    fluid=True,
    #className="mb-4",
)

def toggle_navbar_collapse(n, is_open):
    if n:
        return not is_open
    return is_open

for i in [2]:
    app.callback(
        Output(f"navbar-collapse{i}", "is_open"),
        [Input(f"navbar-toggler{i}", "n_clicks")],
        [State(f"navbar-collapse{i}", "is_open")],
    )(toggle_navbar_collapse)

# embedding the navigation bar
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    navbar,
    html.Div(id='page-content')
])


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/karte':
        return karte.layout
    elif pathname == '/rohdaten':
        return rohdaten.layout
    else:
        return home.layout

if __name__ == '__main__':
    app.run_server(debug=True)