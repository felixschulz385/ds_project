import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc

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
                        )
                    ],
                ),
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dcc.Markdown(
                            """
                            # Die technische Umsetzung
                            
                            Mit diesem Projekt möchten wir einen Überblick über das Potenzial der Ausstattung von Autobahnabfahrten in Deutschland mit Photovoltaik zu geben.
                            Mithilfe modernster GIS-Software und Machine-Learning identifizieren wir Autobahnabfahrten und bewerten deren Eignung zum Ausbau für Solarenergie.
                            Beginnend mit einem Fokus auf das Bundesland Brandenburg planen wir, unsere Modelle auf das gesamte Straßennetz Deutschlands auszuweiten.
                            """
                        ),
                        dmc.Timeline(
                            active=5,
                            bulletSize=15,
                            lineWidth=2,
                            children=[
                                dmc.TimelineItem(
                                    title="Identifizerung Ausfahrten",
                                    children=[
                                        dmc.Text(
                                            [
                                                "Analyse von Vektordaten aus ",
                                                dmc.Anchor(
                                                    "Open Street Map",
                                                    href="https://www.openstreetmap.org/",
                                                    size="sm",
                                                ),
                                                " zur Identifizierung von Straßensegmenten",
                                            ],
                                            color="dimmed",
                                            size="sm",
                                        ),
                                    ],
                                ),
                                dmc.TimelineItem(
                                    title="Hochauflösende Satelitenbilder",
                                    children=[
                                        dmc.Text(
                                            [
                                                dmc.Anchor(
                                                    "Landesvermessungsämter",
                                                    href="https://www.geoportal.de/Themen/Raum_und_Lage/4_Luftbilder%20(DOP).html",
                                                    size="sm",
                                                ),
                                                " bieten Luftaufnahmen in 0,2m x 0,2m an",
                                            ],
                                            color="dimmed",
                                            size="sm",
                                        ),
                                    ],
                                ),
                                dmc.TimelineItem(
                                    title="Beschaffenheitsanalyse der Auffahrten",
                                    children=[
                                        dmc.Text(
                                            [
                                                "Anwendung eines ",
                                                dmc.Anchor(
                                                    "Convolutional Neural Network",
                                                    href="https://de.wikipedia.org/wiki/Convolutional_Neural_Network",
                                                    size="sm",
                                                ),
                                                " zur Segmentierung der Landbedeckung in den Auffahrten mittels Bilddaten",
                                            ],
                                            color="dimmed",
                                            size="sm",
                                        ),
                                    ],
                                ),
                                dmc.TimelineItem(
                                    title="Berechnung einer Wertung",
                                    children=[
                                        dmc.Text(
                                            [
                                                "Ergebnisse aus Neuronalem Netzwerk und andere Daten fließen in Wertung ein"
                                            ],
                                            color="dimmed",
                                            size="sm",
                                        ),
                                    ],
                                ),
                                dmc.TimelineItem(
                                    title="Visualisierung",
                                    children=[
                                        dmc.Text(
                                            [
                                                "Ergebnisse werden mit ",
                                                dmc.Anchor(
                                                    "Dash-Leaflet",
                                                    href="https://pypi.org/project/dash-leaflet/",
                                                    size="sm",
                                                ),
                                                " auf Webseite präsentiert",
                                            ],
                                            color="dimmed",
                                            size="sm",
                                        ),
                                    ],
                                ),
                            ],
                            className="my-4",
                        ),
                        dcc.Markdown(
                            """
                            #### Das Neuronale Netzwerk
                            
                            > TODO: Marvin
                            
                            #### Gesamtwertung
                            
                            Der Gesamtwertung setzt sich aus den Komponenten Landbedeckung, Geländebeschaffenheit, Sonnenpotential und Netzanschluss zusammen. 
                            
                            Die Relevanz der Landbedeckung ergibt sich aus §44 des Naturschutzgesetzes. 
                            Per Gesetz müssen sogenannte Ausgleichsflächen geschaffen werden, 
                            wenn in die Natur eingegriffen wird. 
                            Deshalb dokumentieren wir die prozentuale Verteilung relevanter ökologischer oder 
                            infrastruktureller Faktoren, wie Bäume oder Gebäude, innerhalb einer Fläche. 
                            Aufgrund des hohen Aufwands für den Erwerb von Ausgleichsflächen ist die Landbedeckung ein 
                            wichtiger ökonomischer Faktor und fließt mit einem Anteil von 50% in unsere Gesamtbewertung ein.              

                            Der Bau von Netzwerkinfrastruktur ist regelmäßig mit hohem finanziellen Aufwand verbunden. 
                            Wir modellieren diese Kosten näherungsweise über die Distanz zum nächstgelegenen Netzanschlusspunkt. 
                            Diese gewichten wir zu 25%. 

                            Durch ungleichmäßige Bodenbeschaffenheit entstehen im Bauprozess Kosten. Diesen Faktor gewichten wir zu 10%.

                            Das Sonnenpotential berücksichtigt die Sonnenstunden, die auf einer bestimmten Fläche 
                            durchschnittlich zur Verfügung stehen. Da in der Regel eine Photovoltaikanlage in Deutschland 
                            immer ökonomisch attraktiv ist, bewerten wir diesen Faktor zu nur 15%.
                            """
                        ),
                        html.Table(
                            [
                                html.Thead(
                                    html.Tr(
                                        [
                                            html.Th("Kriterien"),
                                            html.Th(
                                                "Gewichtung",
                                                style={"text-align": "right"},
                                            ),
                                        ]
                                    )
                                ),
                                html.Tbody(
                                    [
                                        html.Tr(
                                            [
                                                html.Td("Landbedeckung"),
                                                html.Td(
                                                    "50 %",
                                                    style={"text-align": "right"},
                                                ),
                                            ]
                                        ),
                                        html.Tr(
                                            [
                                                html.Td("Geländebeschaffenheit"),
                                                html.Td(
                                                    "10 %",
                                                    style={"text-align": "right"},
                                                ),
                                            ]
                                        ),
                                        html.Tr(
                                            [
                                                html.Td("Sonnenpotential"),
                                                html.Td(
                                                    "15 %",
                                                    style={"text-align": "right"},
                                                ),
                                            ]
                                        ),
                                        html.Tr(
                                            [
                                                html.Td("Netzanschluss"),
                                                html.Td(
                                                    "25 %",
                                                    style={"text-align": "right"},
                                                ),
                                            ]
                                        ),
                                    ]
                                ),
                            ],
                            className="table my-2",
                        ),
                    ],
                    width={"size": 6, "offset": 3},
                ),
            ],
            style={"margin-top": "-2rem"},
        ),
    ],
    className="px-4 py-4",
)

layout = html.Div([content])
