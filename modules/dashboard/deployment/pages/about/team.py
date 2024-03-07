import dash
from dash import html, dcc
import dash_bootstrap_components as dbc

dash.register_page(__name__)


content = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Button(
                            "Zurück",
                            href="/",
                            className="btn btn-secondary",
                        ),
                    ],
                    className="order-1 mb-4", 
                    xs=4, md = 2,
                ),
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
                                                className="text-center",
                                            ),
                                            style={"width": "10rem"},
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
                                                className="text-center",
                                            ),
                                            style={"width": "10rem"},
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
                                                className="text-center",
                                            ),
                                            style={"width": "10rem"},
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
                                                className="text-center",
                                            ),
                                            style={"width": "10rem"},
                                            className="m-1",
                                        ),
                                    ],
                                    className="d-flex flex-row flex-wrap",
                                ),
                            ]
                        )
                    ],
                    xs=12, md = 8,
                    className="order-3 order-md-2",
                ),
                dbc.Col(
                    [
                        dbc.Button(
                            "Zur Karte",
                            href="/karte",
                            className="btn btn-secondary",
                        ),
                    ],
                    className="order-2 order-md-3 mb-4", 
                    xs={"size": 4, "offset": 4}, md={"size": 2, "offset":0},
                ),
            ],
        ),
    ],
    className="d-flex justify-content-baseline align-items-start px-4 py-4 mw-100"
)

layout = html.Div([content])
