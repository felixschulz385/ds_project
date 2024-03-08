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
                        dcc.Markdown(
                            """
                            # Technische Umsetzung
                            
                            Mit diesem Projekt möchten wir einen Überblick über das Potenzial der Ausstattung von Autobahnabfahrten in Deutschland mit Photovoltaik zu geben.
                            Mithilfe modernster GIS-Software und Machine-Learning identifizieren wir Autobahnabfahrten und bewerten deren Eignung zum Ausbau für Solarenergie.
                            Beginnend mit einem Fokus auf das Bundesland Brandenburg planen wir, unsere Forschung auf das gesamte Straßennetz Deutschlands auszuweiten.
                            
                            #### Faktoren und Wertung
                            
                            Anhand mehrerer Experteninterviews identifizierte unser Team die größten Kostenfaktoren der Nutzung einer Fläche in Autobahnauffahrten für Photovoltaik. Die Elemente unserer Analyse sind die Landbedeckung, die Geländebeschaffenheit, das Sonnenpotential und der Netzanschluss. Um dem Nutzer einen schnellen Überblick zu verschaffen, fassen wir die Eignung in diesen Aspekten in einem Wertungssystem zusammen. 
                            
                            Die Relevanz der Landbedeckung ergibt sich aus §44 des Naturschutzgesetzes. Per Gesetz müssen sogenannte Ausgleichsflächen geschaffen werden, wenn in die Natur eingegriffen wird. Deshalb dokumentieren wir die prozentuale Verteilung relevanter ökologischer oder infrastruktureller Faktoren, wie Bäume oder Gebäude, innerhalb einer Fläche. Die Informationen zur Landbedeckung werden von uns eigens für dieses Projekt im unten erläuterten Verfahren erfasst. Die zentrale Datenquellen in diesem Prozess sind die [Luftaufnahmen DOP20](https://geobroker.geobasis-bb.de/gbss.php?MODE=GetProductPreview&PRODUCTID=7a503f0f-db46-4772-80e3-b27733fd7acd) des Landes Brandenburg. Aufgrund des hohen Aufwands für den Erwerb von Ausgleichsflächen ist die Landbedeckung ein wichtiger ökonomischer Faktor und fließt mit einem Anteil von 50% in unsere Gesamtbewertung ein.              

                            Der Bau von Netzwerkinfrastruktur ist regelmäßig mit hohem finanziellen Aufwand verbunden. Wir modellieren diese Kosten näherungsweise über die Distanz zum nächstgelegenen Netzanschlusspunkt. Die Daten hierzu beziehen wir aus [OpenStreetMap](https://www.openstreetmap.org/).
                            Diese gewichten wir zu 25%. 

                            Durch ungleichmäßige Bodenbeschaffenheit entstehen im Bauprozess Kosten. Das Höhenprofil analysieren wir anhand der Geländedaten [DGM01](https://geobroker.geobasis-bb.de/gbss.php?MODE=GetProductPreview&PRODUCTID=414f568f-639b-4b5a-ba92-57fdac396799) des Landes Brandenburg. Diesen Faktor gewichten wir zu 10%.

                            Das Sonnenpotential berücksichtigt die durchschnittlichen jährlichen Sonnenstunden, die auf einer bestimmten Fläche zu erwarten sind. Wir errechnen diesen Wert anhand des Datensatzes [CM SAF](https://doi.org/10.5676/EUM_SAF_CM/SARAH/V002) der Organisation EUMETSAT. Da auf Freiflächen wie der in Autobahnauffahrten mit einem neutralen Steigungsprofil eine optimale Ausrichtung nahezu immer möglich ist, bewerten wir diesen Faktor zu nur 15%.
                            """
                        ),
                        html.Table(
                            [
                                html.Caption("Faktoren, Datenquellen und Gewichtung in Gesamtwertung"),
                                html.Thead(
                                    html.Tr(
                                        [
                                            html.Th("Kriterien"),
                                            html.Th("Datenquelle"),
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
                                                html.Td(html.A("DOP20: GeoBasis-DE/LGB", href="https://geobroker.geobasis-bb.de/gbss.php?MODE=GetProductPreview&PRODUCTID=7a503f0f-db46-4772-80e3-b27733fd7acd")),
                                                html.Td(
                                                    "50 %",
                                                    style={"text-align": "right"},
                                                ),
                                            ]
                                        ),
                                        html.Tr(
                                            [
                                                html.Td("Geländebeschaffenheit"),
                                                html.Td(html.A("DGM01: GeoBasis-DE/LGB", href="https://geobroker.geobasis-bb.de/gbss.php?MODE=GetProductPreview&PRODUCTID=414f568f-639b-4b5a-ba92-57fdac396799")),
                                                html.Td(
                                                    "10 %",
                                                    style={"text-align": "right"},
                                                ),
                                            ]
                                        ),
                                        html.Tr(
                                            [
                                                html.Td("Sonnenpotential"),
                                                html.Td(html.A("CM SAF", href="https://doi.org/10.5676/EUM_SAF_CM/SARAH/V002")),
                                                html.Td(
                                                    "15 %",
                                                    style={"text-align": "right"},
                                                ),
                                            ]
                                        ),
                                        html.Tr(
                                            [
                                                html.Td("Netzanschluss"),
                                                html.Td(html.A("CM SAF", href="https://www.openstreetmap.org/")),
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
                        dcc.Markdown(
                            """
                            #### Unser Evaluationsprozess
                            """,
                            className="mb-2"
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
                            
                            Im Kern unserer Forschung steht ein künstliches neuronales Netzwerk, das anhand von Luftaufnahmen der Autobahnauffahrten Karten der Bebauung und Vegetation erstellt. Dafür ordnet das Modell in einem komplexen Verfahren einzelne Bildpixel einer der folgenden 5 Klassen zu: Gebäude, Straße, Landwirtschaft, Hoher Bewuchs, und Niedriger Bewuchs. 
                            
                            Technisch stellt unser adaptiertes [DeepLabV3-Modell](https://arxiv.org/abs/1706.05587v3) einen Durchbruch in der Bodenbedeckungssegmentierung dar. Ursprünglich konzipiert für die detaillierte Objekterkennung und basierend auf dem leistungsfähigen [ResNet101](https://arxiv.org/abs/1512.03385)-Netzwerk, wurde das Modell mit dem [COCO](https://cocodataset.org/#home)-Datensatz vortrainiert, einem umfassenden Bilderkorpus zur Mustererkennung. Darauf aufbauend haben wir das Modell mit dem [LoveDA](https://paperswithcode.com/dataset/loveda)-Datensatz weiter für Problemstellungen der Bodenbedeckungssegmentierung in Städten und ländlichen Regionen optimiert. Diese Anpassung erlaubt es uns, die vegetative Bedeckung an Autobahnausfahrten detailgenau zu quantifizieren.

                            Das Ergebnis: Ein Werkzeug, das die Segmentierung von Vegetation in Luftbildern automatisiert und genaue Daten für städtische und ökologische Anwendungen liefert. Unser adaptiertes DeepLabV3 Model hilft, grüne Flächen zu messen und zu analysieren, und unterstützt so aktiv die nachhaltige Stadt- und Landschaftsplanung sowie den Naturschutz.
                            """,
                        ),
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
            ]
        ),
    ],
    className="px-4 py-4",
)

layout = html.Div([content])
