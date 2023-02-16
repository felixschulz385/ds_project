import dash_bootstrap_components as dbc
from dash import Dash, Input, Output, html, dcc
from dash_iconify import DashIconify
import dash_mantine_components as dmc

import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

from app import path_directory


# import data
kreise_df = pd.read_csv(path_directory + 'apps/assets/kreise_df.csv')
# rename and drop columns
kreise_df = kreise_df.drop(columns=['Unnamed: 0']).rename(columns={'NAME_1': 'Bundesland', 'NAME_2': 'Region', 'NAME_3': 'Landkreis', 'ENGTYPE_3': 'Land_Stadt'})


# create sunburst plot
Ohren_sunburst = px.sunburst(kreise_df, path=['Bundesland', 'Region', 'Landkreis'], values='avg_Score')
Ohren_sunburst = Ohren_sunburst.update_traces(
    insidetextorientation='radial',
    hovertemplate = '<b>%{label}</b> <br>Score: %{value}')


# the style arguments for the sidebar. We use position:fixed and a fixed width
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 62.5,
    "left": 0,
    "bottom": 0,
    "width": "26rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}
FOOTER_STYLE = {
    "position": "fixed",
    "top": 720,
    "left": 0,
    "bottom": 0,
    "width": "26rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}
# the styles for the main content position it to the right of the sidebar and add some padding.
CONTENT_STYLE = {
    "margin-left": "28rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

# --------------------
# SIDEBAR
# --------------------

sidebar = html.Div([
    dbc.Row([
      html.H3('Road to Renewables'),
      html.H5('Erneuerbare Energie Potenziale an Deutschlands Schnellstraßen'),
      html.Hr()
    ]),
    dbc.Row([
        html.H5("Autoren"),
        dmc.List(icon=DashIconify(icon="openmoji:man-student", width=25),
            size="md",
            spacing="sm",
            children=[
                dmc.ListItem((dmc.HoverCard(
        shadow="md",children=[
            dmc.HoverCardTarget("Yvette Bodry"),
            dmc.HoverCardDropdown([
                dmc.Group([
                    dmc.Anchor(
                        DashIconify(icon="bi:github", width=40),
                                    href="https://github.com/vivresursonnuage/",
                                    target="_blank")],
                        p=0,
                    )])], position = "right")), DashIconify(icon="openmoji:woman-student", width=25)),
                dmc.ListItem(
       (dmc.HoverCard(
        shadow="md",children=[
            dmc.HoverCardTarget("Felix Schulz"),
            dmc.HoverCardDropdown([
                dmc.Group([
                    dmc.Anchor(
                        DashIconify(icon="bi:linkedin", width=40),
                                    href="https://www.linkedin.com/in/felix-schulz-a41bab165/",
                                    target="_blank"),
                    dmc.Anchor(
                        DashIconify(icon="bi:github", width=40),
                                    href="https://github.com/felixschulz385/",
                                    target="_blank")],
                        p=0,
                    )])], position = "right"))
                    ),
                dmc.ListItem(
       (dmc.HoverCard(
        shadow="md",children=[
            dmc.HoverCardTarget("Marvin Hoberg"),
            dmc.HoverCardDropdown([
                dmc.Group([
                    dmc.Anchor(
                        DashIconify(icon="bi:linkedin", width=40),
                                    href="https://www.linkedin.com/in/marvin-hoberg-1a6326201/",
                                    target="_blank"),
                    dmc.Anchor(
                        DashIconify(icon="bi:github", width=40),
                                    href="https://github.com/marvin-hoberg/",
                                    target="_blank")],
                        p=0,
                    )])], position = "right"))
                    ),
                dmc.ListItem(
        (dmc.HoverCard(
        shadow="md",children=[
            dmc.HoverCardTarget("Jan Besler"),
            dmc.HoverCardDropdown([
                dmc.Group([
                    dmc.Anchor(
                        DashIconify(icon="bi:linkedin", width=40),
                                    href="https://www.linkedin.com/in/janbesler/",
                                    target="_blank"),
                    dmc.Anchor(
                        DashIconify(icon="bi:github", width=40),
                                    href="https://github.com/janbesler/",
                                    target="_blank")],
                        p=0,
                    )])], position = "right")),
                    ),
]),
    ]),
], style=SIDEBAR_STYLE)

# --------------------
# SIDEBAR FOOTER
# --------------------

footer = html.Div([
        # Links und Erklärungen
    dbc.Row([
      dbc.Col([
        dmc.Center([
        dmc.Anchor(
            DashIconify(icon="bi:github", width=40),
                        href="https://github.com/felixschulz385/ds_project",
                        target="_blank",
        )])]),
      dbc.Col([
        dmc.Center([
        dmc.Anchor(
            DashIconify(icon="bi:newspaper", width=40),
                        href="https://www.badische-zeitung.de/ob-palmer-will-solaranlagen-auf-freien-stellen-neben-bundesstrassen--211487616.html",
                        target="_blank",
        )])]),
      html.P('This project is being developed as part of the \
              Data Science in Business and Economics Master degree course at the University of Tübingen.')
    ], className="fixed-row-bottoms", align="end")
], style=FOOTER_STYLE)


# --------------------
# MAIN PAGE
# --------------------

# images
import base64
with open(path_directory + "apps/assets/economic_model.jpeg", "rb") as file:
    economic_model_img = "data:image/jpg;base64, {}".format(base64.b64encode(file.read()).decode("utf-8"))
with open(path_directory + "apps/assets/brandenburg_driveways.jpg", "rb") as file:
    BB_ohren = "data:image/jpg;base64, {}".format(base64.b64encode(file.read()).decode("utf-8"))
# carousel pictures
with open(path_directory + "apps/assets/Lustnauer_Ohren_vorher.jpg", "rb") as file:
    carousel_1 = "data:image/jpg;base64, {}".format(base64.b64encode(file.read()).decode("utf-8"))
with open(path_directory + "apps/assets/Lustnauer_Ohren_danach.jpg", "rb") as file:
    carousel_2 = "data:image/jpg;base64, {}".format(base64.b64encode(file.read()).decode("utf-8"))
    
# change to app.layout if running as single page app instead
content = html.Div([
    dmc.Tabs([
        dmc.TabsList([
            dmc.Tab("Einleitung & Motivation", value = "einleitung"),
            dmc.Tab("Informationen", value = "dashboard"),
            dmc.Tab("Projektstruktur", value = "aufbau"),
            dmc.Tab("Daten", value = "daten"),
        ], grow=True),

        # Einleitung
    dmc.TabsPanel(
        dbc.Container([
        dmc.Accordion(
            value="einleitung_accordion",
            children=[
            dmc.AccordionItem([
                dmc.AccordionControl("Einleitung"),
                dmc.AccordionPanel(
                    dbc.Row([
                    dbc.Col([
                        dcc.Markdown('''
                        Das 'Road to Renewables' Projekt hilft bisher ungenutzte Flächen für den Ausbau von Erneuerbaren Energien
                        aufzuzeigen. Ziel ist es interessierten Bürger:innen und Gemeinden visuell ansprechend darzulegen, wo in
                        Deutschland Potenziale vorhanden sind. Die betrachteten Flächen, werden so ausgewählt, dass es keine
                        Interessenskonflikte über Verwendungsmöglichkeiten geben soll.

                        Dazu gehören die sogenannten 'Ohren' in Ausfahrten von Schnellstraßen. Diese Flächen haben bisher keine
                        nennenswerte wirtschaftliche Verwendung. Mit dem Pilotprojekt aus Tübingen hat sich die Idee gefestigt, diese
                        Freiflächen für den Ausbau von Erneuerbaren Energien zu nutzen.

                        Wir wollen mit Hilfe von Machine Learning ähnliche Flächen in Deutschland identifizieren und diese interaktiv
                        zum freien Erkunden auf einer Karte darstellen.
                            ''')
                    ], width = 7),
                    dbc.Col([
                        dbc.Carousel(items=[
                        {"key": "1",
                        "src": carousel_1,
                        "header": "Lustnauer 'Ohren' vor Bebauung"},
                        {"key": "1",
                        "src": carousel_2,
                        "header": "Lustnauer 'Ohren' nach Bebauung"}], style={"width": "60vh"})
                    ], width=4)])
                ),], 
            value="einleitung_accordion"),
            dmc.AccordionItem([
                dmc.AccordionControl("Motivation"),
                dmc.AccordionPanel([
                    dbc.Row([
                        dbc.Col([
                        dcc.Markdown('''
                        Der globale Klimawandel hat die deutsche Energiewirtschaft in Aufruhr versetzt. 
                        Nach Jahren der starken Abhängigkeit von Kohle und Gas (im Jahr 2010 wurden 25% des deutschen Energiemixes 
                        des deutschen Energiemixes auf diese Weise bezogen ([BDEW, 2022](https://www.bdew.de/energie/bruttostromerzeugung-seit-2010/)), 
                        haben die Klimazusagen die Politiker gezwungen, auf erneuerbare Energien umzusteigen 
                        ([Bundesregierung, 2022](https://www.bundesregierung.de/breg-en/issues/climate-action/government-climate-policy-1779414)). 

                        Der Bau von Onshore-Windparks wird immer wieder durch lokalen Widerstand gestoppt ([DW, 2022](https://p.dw.com/p/4K361)),
                        die installierte Leistung der Photovoltaik (PV) ist in den letzten Jahren hingegen stetig und schnell gewachsen
                        ([Bundesnetzagentur, 2022](https://www.smard.de/home/marktdaten)). Einer ihrer großen Vorteile ist der viel geringere Platzbedarf
                        der Paneele im Vergleich zu Windkraftanlagen. Dadurch können PV-Anlagen an Orten installiert werden, die kaum anderweitig genutzt werden, 
                        vor allem auf Hausdächern. Mehrere deutsche Bundesländer haben die Installation von PV auf neuen Gebäuden sogar zur Pflicht gemacht 
                        ([Imolauer, 2022](https://www.roedl.com/insights/renewable-energy/2021/august/pv-obligation-germany-federal-states)). 

                        Auf der Suche nach weiteren Möglichkeiten entdeckte die süddeutsche Stadt Tübingen den Platz innerhalb einer ihrer Autobahnauffahrten
                        als sehr geeignet für die PV-Nutzung
                        ([swt, 2022](https://www.swtue.de/energie/strom/erneuerbare-energien/bautagebuecher/solarpark-lustnauer-ohren.html)).
                        Nach jahrelangem juristischem Hin und Her ist die Fläche nun die größte Ökostromquelle der Stadt.

                        Ihr großer Vorteil - ähnlich wie bei Hausdächern - besteht darin, dass es kaum alternative Nutzungsmöglichkeiten für die Fläche gibt.
                        Umgeben von Verkehr und Umweltverschmutzung halten die Stadt und wir Autoren die PV-Energieerzeugung für eine geniale Idee
                        um diese vom Menschen geschaffenen Brachflächen neu zu nutzen. Deutschland verfügt über ein großes Netz geteilter Fahrbahnen auf seinen
                        Autobahn- und Bundesstraßennetz. Die vielen Verbindungen zu lokalen Straßen können in Zukunft als hervorragende Möglichkeiten
                        für die künftige PV-Energieerzeugung dienen.
                            ''')], width=7),
                        dbc.Col([
                            dbc.Card([
                            dbc.CardImg(src = BB_ohren, top=True),
                            dbc.CardBody(html.P("Beispielbild der potenziellen Flächen.", className="card-text")),
                            ],style={"height": "60vh", "width": "60vh"})
                        ], width=4)]),
                ]),
            ],value="motivation_accordion")
        ]),
        ]), value = 'einleitung'
    ),

        # Dashboard Erklärung
    dmc.TabsPanel(
        dbc.Container([
        dmc.Accordion(value= 'home_accordion',children=[
            dmc.AccordionItem([
                dmc.AccordionControl("Home"),
                dmc.AccordionPanel(
                    dbc.Row([dbc.Col([
                        dcc.Markdown('''
                            Auf dieser ersten Seite unserer Webseite leiten wir unser Projekt ein und geben Interessenten 
                            alle notwendigen Informationen an die Hand um unser interaktives Dashboard nutzen zu können.
                            Dazu gehören die Hintergründe sowohl zu diesem Projekt als auch zu dem realisierten Tübinger Projekt,
                            die Motivation uns mit diesem Thema auseinander zu setzen und die Erklärung wie genau 
                            wir das Projekt angegangen sind und welche Lösungsansätze wir uns zu diesem Pilotprojket 
                            herausgesucht haben.
                            
                            Desweiteren möchten wir, die Autoren, uns presentieren und den universitären Rahmen erläutern.
                        ''')
                    ], width=7),
                        dbc.Col([
                            html.H5("Funktionalitäten"),
                            dmc.List([
                                dmc.ListItem(dmc.Text(
                                    "Links zu allen relevanten Erklärungen, Quellen und weiterführenden Informationen"
                                )),
                                dmc.ListItem(dmc.Text(
                                    "Hintergründe zu allen Bestandteilen des Projekts"
                                )),
                                dmc.ListItem(dmc.Text(
                                    "Graph mit allen evaluierten 'Ohren' und dem dazugehörigen Score"
                                )),
                            ])                            
                    ], width=4)
                ]))], value="home_accordion"),
            dmc.AccordionItem([
                dmc.AccordionControl("Karte"),
                dmc.AccordionPanel(
                    dbc.Row([dbc.Col([
                        dcc.Markdown('''
                            Die Karte stellt das Herzstück unserer Arbeit dar, hier fließen alle bisherigen Überlegungen 
                            und Arbeitsschritte zusammen. Auf der OpenStreetMap Karte sind alle 'Ohren' verzeichnet und 
                            farbig markiert. Die Alle Entitäten besitzen einen Score, dies gilt neben den 'Ohren' auch für
                            die Gemeinden, Kreise und Bundesländer.
                            
                            Unterhalb der Karte sind in der Informationsbox alle relevanten Information für die ausgewählte
                            Entität genauer aufgezeigt, sodass besser nachvollzogen werden kann, woher die Einflüsse für die
                            Erstellung der Bewertung kommen.
                        ''')
                    ], width=7),
                        dbc.Col([
                            html.H5("Funktionalitäten"),
                            dmc.List([
                                dmc.ListItem(dmc.Text(
                                    "Alle Gegenstände innerhalb der Karte sind interaktiv"
                                )),
                                dmc.ListItem(dmc.Text(
                                    "Infofenster für das ausgewählte Element"
                                )),
                                dmc.ListItem(dmc.Text(
                                    "Detaillierte Informationen für das ausgewählte Element unterhalb der Karte"
                                )),
                            ])   
                    ], width=4)
                ]))], value="karte_accordion"),
            dmc.AccordionItem([
                dmc.AccordionControl("Tabelle"),
                dmc.AccordionPanel(
                    dbc.Row([dbc.Col([
                        dcc.Markdown('''
                            Die Tabelle dient dem Zweck alle Informationen in alternativer Darstellung zu zeigen und dient
                            in erster Sicht dem Suchen und Filtern von der 'Ohren' um spezifische Informationen oder
                            Gebiete schneller und gezielter finden zu können. Dies wird durch die Filter OPtionen für die
                            Variable Bundesland ermöglicht sowie die Sortier Optionen für alle Spalten. Desweiteren erleichtert
                            eine visuelle Hervorhebung der Score Spalte die Suche nach aussichtsreichen Orten.
                        ''')
                    ], width=7),
                        dbc.Col([
                            html.H5("Funktionalitäten"),
                            dmc.List([
                                dmc.ListItem(dmc.Text(
                                    "Filter Optionen für Bundesländer"
                                )),
                                dmc.ListItem(dmc.Text(
                                    "Sortier Optionen für alle Variablen"
                                )),
                                dmc.ListItem(dmc.Text(
                                    "Heat-Spalte für einfachere Suche von aussichtsreichen 'Ohren'"
                                )),
                            ]) 
                    ], width=4)
                ]))], value="tabelle_accordion"),
    ]),
        ]), value = "dashboard"
    ),
        
        # Aufbau
    dmc.TabsPanel(
        dbc.Container([
        dmc.Accordion(
            value="aufbau_accordion",
            children=[
            dmc.AccordionItem([
                dmc.AccordionControl("Aufbau"),
                dmc.AccordionPanel(
            dbc.Row([
            dbc.Col([
                dcc.Markdown('''
                Unser Projekt zielt darauf ab, einen umfassenden Überblick über das Potenzial der Ausstattung von Autobahnabfahrten in Deutschland mit Photovoltaik zu geben.
                Mit Hilfe modernster GIS-Software und Machine-Learning-Techniken identifizieren wir Abzweigungen und bewerten deren Eignung.
                Beginnend mit einem begrenzten Umfang auf das Bundesland Brandenburg, planen wir, unsere Modelle auf das gesamte Straßennetz Deutschlands auszuweiten.
                '''),
            dmc.Timeline(
                active=5, bulletSize=15, lineWidth=2,
                children=[
                    dmc.TimelineItem(
                        title="hochauflösende Satelitenbilder",
                        children=[
                            dmc.Text([
                                dmc.Anchor("Landesvermessungsämter", href="https://www.geoportal.de/Themen/Raum_und_Lage/4_Luftbilder%20(DOP).html", size="sm"),
                                " bieten Flugzeugaufnahmen in 0,2m x 0,2m an"],
                                color="dimmed",
                                size="sm"),
                        ]),
                    dmc.TimelineItem(
                        title="Identifizerung Ausfahrten",
                        children=[
                            dmc.Text([
                                "In ",
                                dmc.Anchor("Open Street Map", href="https://www.openstreetmap.org/", size="sm"),
                                " sind Abschnitte von Ausfahrten markiert"],
                                color="dimmed",
                                size="sm"),
                        ]),
                    dmc.TimelineItem(
                        title="Beschaffenheitsanalyse der 'Ohren'",
                        children=[
                            dmc.Text([
                                "Festlegung auf ein ",
                                dmc.Anchor("Convolutional Neural Network", href="https://de.wikipedia.org/wiki/Convolutional_Neural_Network", size="sm"),
                                " zur Erkennung von Bäumen und anderen Objekten in Satellitenbildern"],
                                color="dimmed",
                                size="sm"),
                        ]),
                    dmc.TimelineItem(
                        title="Trainingsdaten",
                        children=[
                            dmc.Text([
                                "Nutzung von pixelweise gelabelten Daten der  ",
                                dmc.Anchor("China Daten", href="", size="sm")],
                                color="dimmed",
                                size="sm"),
                        ]),
                    dmc.TimelineItem(
                        title="Ranking der 'Ohren'",
                        children=[
                            dmc.Text([
                                "Um die Flächen vergleichbar zu gestalten wurde ein Score aus verschiedenen Parametern erstellt"],
                                color="dimmed",
                                size="sm"),
                        ]),
                    dmc.TimelineItem(
                        title="Visualisierung",
                        children=[
                            dmc.Text([
                                dmc.Anchor("Dash-Leaflet", href="https://pypi.org/project/dash-leaflet/", size="sm"),
                                " integriert die schnelle Leaflet Karte nahtlos in die Python Library Dash"],
                                color="dimmed",
                                size="sm"),
                        ]),
                ]),
            ], width=7),
            dbc.Col([
            dbc.Card([
                html.Img(src = economic_model_img),
                dbc.CardBody(
                    html.P("Parameter des ökonomischen Modells", className="card-text")),
            ],style={"height": "60vh", "width": "60vh"})
            ], width=4),
        ])), # end of accordion #1
            ], value="aufbau_accordion"),
        # start accordion #2
            dmc.AccordionItem([
                dmc.AccordionControl("Hintergründe"),
                dmc.AccordionPanel(
                    dcc.Markdown('''
                            In einem Interview mit den begründern des Pilotprojekts den Stadtwerken Tübingen ist herausgekommen,
                            dass die KLärung der rechtlichen Grundlagen 8 Jahre gedauert hat, während der Bau in wenigen Wochen abgeschlossen war.
                        ''')
                )], value="probleme_ohren",
        ),# end accordion #2
        # start accordion #3
            dmc.AccordionItem([
                dmc.AccordionControl("Zusammensetzung Score"),
                dmc.AccordionPanel(
                    dcc.Markdown('''
                            Der Score setzt sich aus verschiedenen Komponenten zusammen.
                        ''')
                )], value="probleme_projekt",
        ),# end accordion #3
        ])# end acordion
        ]), value= "aufbau"
    ),
        
    # Sunburst Plot
    dmc.TabsPanel(
        dbc.Container([
        # Sunburst Plot
        dbc.Row([
            dbc.Col([
                dcc.Graph(figure = Ohren_sunburst, responsive=True, style = {'height': '85vh', 'width': '100vh'})
            ], width=7, class_name = "d-flex justify-content-center"),
            dbc.Col([
                html.H5("Funktionalitäten"),
                dmc.List([
                    dmc.ListItem(dmc.Text(
                        "Links zu allen relevanten Erklärungen, Quellen und weiterführenden Informationen"
                    )),
                    dmc.ListItem(dmc.Text(
                        "Hintergründe zu allen Bestandteilen des Projekts"
                    )),
                    dmc.ListItem(dmc.Text(
                        "Graph mit allen evaluierten 'Ohren' und dem dazugehörigen Score"
                    )),
                ])], width=4)
        ])
        ]), value = "daten"
    )
    ],
    color = "yellow",
    orientation = "horizontal",
    value = "einleitung"
    )

], style=CONTENT_STYLE)

layout = html.Div([sidebar, footer, content])