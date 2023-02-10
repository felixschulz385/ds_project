import dash_html_components as html
import dash_bootstrap_components as dbc

# change to app.layout if running as single page app instead
layout = html.Div([
    dbc.Container([
        dbc.Row([
            dbc.Col(html.H1("Lustnauer 'Ohren' skaliert auf ganz Deutschland", className="text-center")
                    , className="mb-5 mt-5")
        ]),
        dbc.Row([
            dbc.Col(html.H5(children='Erkennen von ungenutzten Potenzialen in ungenutzten Flächen.'
                                     )
                    , className="mb-4")
            ]),

        dbc.Row([
            dbc.Col(html.H5(children='Auf der zweiten Seite wird eine interaktive Karte dargestellt, welche die verschiedenen Ohren ranked '
                                     'Die dritte Seite präsentiert dieselben Daten in tabellarischer Form, zum erkunden und nachschlagen.')
                    , className="mb-5")
        ]),

        dbc.Row([
            dbc.Col(dbc.Card(children=[html.H3(children='Get the original datasets used in this dashboard',
                                               className="text-center"),
                                       dbc.Row([dbc.Col(dbc.Button("Global", href="https://data.europa.eu/euodp/en/data/dataset/covid-19-coronavirus-data/resource/55e8f966-d5c8-438e-85bc-c7a5a26f4863",
                                                                   color="primary"),
                                                        className="mt-3"),
                                                dbc.Col(dbc.Button("Singapore", href="https://data.world/hxchua/covid-19-singapore",
                                                                   color="primary"),
                                                        className="mt-3")], justify="center")
                                       ],
                             body=True, color="dark", outline=True)
                    , width=4, className="mb-4"),

            dbc.Col(dbc.Card(children=[html.H3(children='GitHub Repository',
                                               className="text-center"),
                                       dbc.Button("GitHub",
                                                  href="https://github.com/felixschulz385/ds_project",
                                                  color="primary",
                                                  className="mt-3"),
                                       ],
                             body=True, color="dark", outline=True)
                    , width=4, className="mb-4"),

            dbc.Col(dbc.Card(children=[html.H3(children='Wie alles begann',
                                               className="text-center"),
                                       dbc.Button("Medium",
                                                  href="https://www.badische-zeitung.de/ob-palmer-will-solaranlagen-auf-freien-stellen-neben-bundesstrassen--211487616.html",
                                                  color="primary",
                                                  className="mt-3"),

                                       ],
                             body=True, color="dark", outline=True)
                    , width=4, className="mb-4")
        ], className="mb-5"),

        html.A("Special thanks to Flaticon for the icon in COVID-19 Dash's logo.",
               href="https://www.flaticon.com/free-icon/coronavirus_2913604")

    ])

])