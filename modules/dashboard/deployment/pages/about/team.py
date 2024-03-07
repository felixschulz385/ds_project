import dash
from dash import html, dcc
import dash_bootstrap_components as dbc

dash.register_page(__name__)


content = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Div(
                            [
                                dbc.Button(
                                    "Zurück zu 'Über'",
                                    href="/about",
                                    className="btn btn-secondary",
                                ),
                                dbc.Button(
                                    "Zur Karte",
                                    href="/karte",
                                    className="btn btn-secondary",
                                ),
                            ],
                            className="d-flex justify-content-between",
                        ),
                    ],
                ),
            ],
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Div(
                            [
                                dcc.Markdown(
                                    """
                                    ## Das Team
                                    
                                    Dieses Projekt entstand 2023 im Rahmen des Abschlussprojekts des Masterstudiengangs Data Science in Business and Economics der Universität Tübingen.
                                    Unser Team erarbeite sich das Thema unter Betreuung von Prof. Dr. Papies und Dr. Aseem Behl vom Lehrstuhl für Marketing.
                                    """
                                ),
                                html.Div(
                                    [
                                        dbc.Card(
                                            dbc.CardBody(
                                                [
                                                    html.H6("Felix Schulz"),
                                                    dbc.Nav(
                                                        [
                                                            dbc.NavItem(
                                                                html.A(
                                                                    html.Img(
                                                                        src="/assets/linkedin-icon.svg",
                                                                        height="30px",
                                                                    ),
                                                                    href="https://www.linkedin.com/in/felix-schulz-a41bab165/",
                                                                )
                                                            ),
                                                            dbc.NavItem(
                                                                [
                                                                    html.A(
                                                                        [
                                                                            html.Img(
                                                                                src="/assets/github-mark.svg",
                                                                                height="30px",
                                                                            )
                                                                        ],
                                                                        href="https://github.com/felixschulz385/",
                                                                    )
                                                                ]
                                                            ),
                                                        ],
                                                        justified=True,
                                                    ),
                                                ],
                                            ),
                                            style={"width": "12rem"},
                                            className="m-1",
                                        ),
                                        dbc.Card(
                                            dbc.CardBody(
                                                [
                                                    html.H6("Marvin Hoberg"),
                                                    dbc.Nav(
                                                        [
                                                            dbc.NavItem(
                                                                html.A(
                                                                    html.Img(
                                                                        src="/assets/linkedin-icon.svg",
                                                                        height="30px",
                                                                    ),
                                                                    href="https://www.linkedin.com/in/marvin-hoberg-1a6326201/",
                                                                )
                                                            ),
                                                            dbc.NavItem(
                                                                [
                                                                    html.A(
                                                                        [
                                                                            html.Img(
                                                                                src="/assets/github-mark.svg",
                                                                                height="30px",
                                                                            )
                                                                        ],
                                                                        href="https://github.com/marvin-hoberg/",
                                                                    )
                                                                ]
                                                            ),
                                                        ],
                                                        justified=True,
                                                    ),
                                                ],
                                            ),
                                            style={"width": "12rem"},
                                            className="m-1",
                                        ),
                                        dbc.Card(
                                            dbc.CardBody(
                                                [
                                                    html.H6("Yvette Bodry"),
                                                    dbc.Nav(
                                                        [
                                                            dbc.NavItem(
                                                                [
                                                                    html.A(
                                                                        [
                                                                            html.Img(
                                                                                src="/assets/github-mark.svg",
                                                                                height="30px",
                                                                            )
                                                                        ],
                                                                        href="https://github.com/vivresursonnuage/",
                                                                    )
                                                                ]
                                                            ),
                                                        ],
                                                        justified=True,
                                                    ),
                                                ],
                                            ),
                                            style={"width": "12rem"},
                                            className="m-1",
                                        ),
                                        dbc.Card(
                                            dbc.CardBody(
                                                [
                                                    html.H6("Jan\nBesler"),
                                                    dbc.Nav(
                                                        [
                                                            dbc.NavItem(
                                                                html.A(
                                                                    html.Img(
                                                                        src="/assets/linkedin-icon.svg",
                                                                        height="30px",
                                                                    ),
                                                                    href="https://www.linkedin.com/in/janbesler/",
                                                                )
                                                            ),
                                                            dbc.NavItem(
                                                                [
                                                                    html.A(
                                                                        [
                                                                            html.Img(
                                                                                src="/assets/github-mark.svg",
                                                                                height="30px",
                                                                            )
                                                                        ],
                                                                        href="https://github.com/janbesler/",
                                                                    )
                                                                ]
                                                            ),
                                                        ],
                                                        justified=True,
                                                    ),
                                                ],
                                            ),
                                            style={"width": "12rem"},
                                            className="m-1"
                                        ),
                                    ],
                                    className="d-flex flex-row",
                                ),
                            ],
                        )
                    ],
                    width={"size":6, "offset":3}
                ),
            ],
            style={"margin-top": "-2rem"},
        ),
    ],
    className="px-4 py-4",
)

layout = html.Div([content])
