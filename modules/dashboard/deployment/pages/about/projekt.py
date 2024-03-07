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
                            ## Das Projekt SolarExit
                            
                            Der globale Klimawandel und die andauernde Energiekrise hat die deutsche Energiewirtschaft in Aufruhr versetzt.
                            Nach Jahren des starken Fokus auf Kohle und Gas (im Jahr 2010 wurden 25% des deutschen Energiemixes des deutschen Energiemixes auf diese Weise bezogen ([BDEW, 2022](https://www.bdew.de/energie/bruttostromerzeugung-seit-2010/))), binden Klimazusagen Politiker zunehmend, auf erneuerbare Energien umzusteigen ([Bundesregierung, 2022](https://www.bundesregierung.de/breg-en/issues/climate-action/government-climate-policy-1779414)).
                            
                            Der Bau von Onshore-Windparks wird immer wieder durch lokalen Widerstand gestoppt ([DW, 2022](https://p.dw.com/p/4K361))). Die installierte Leistung der Fotovoltaik (PV) ist in den letzten Jahren hingegen stetig und schnell gewachsen ([Bundesnetzagentur, 2022](https://www.smard.de/home/marktdaten)). Einer ihrer großen Vorteile ist der viel geringere Platzbedarf der Paneele im Vergleich zu Windkraftanlagen. Dadurch können PV-Anlagen an Orten installiert werden, die kaum anderweitig genutzt werden, vor allem auf Hausdächern. Mehrere deutsche Bundesländer die Installation von PV auf neuen Gebäuden sogar zur Pflicht gemacht ([Imolauer, 2022](https://www.roedl.com/insights/renewable-energy/2021/august/pv-obligation-germany-federal-states)).
                            
                            Die Potentialflächen, über die eine engagierte Kommune verfügen kann, sind allerdings begrenzt. Auf der Suche nach Möglichkeiten des Ausbaus entdeckte die Baden-Württembergische Stadt Tübingen ein Bauplatz innerhalb einer ihrer Autobahnauffahrten als sehr geeignet für die PV-Nutzung ([swt, 2022](https://www.swtue.de/energie/strom/erneuerbare-energien/bautagebuecher/solarpark-lustnauer-ohren.html)). Nach jahrelangen öffentlichen Debatten und einem aufwendigen Genehmigungsprozess ist die Fläche nun die größte Ökostromquelle der Stadt. 
                            
                            Der große Vorteil der Flächen in Autobahnauffahrten - ähnlich dessen der Hausdächer - besteht darin, dass es kaum alternative Nutzungsmöglichkeiten für das Land gibt. Umgeben von Verkehr und Emissionen halten die Stadt und wir Autoren die PV-Energieerzeugung für eine geniale Idee, um diese vom Menschen geschaffenen Brachflächen zu nutzen. Deutschland verfügt über ein großes Netz geteilter Fahrbahnen auf seinen Autobahn- und Bundesstraßennetz. Die vielen Verbindungen zu lokalen Straßen können in Zukunft als hervorragende Möglichkeiten für die künftige PV-Energieerzeugung dienen.
                            
                            In diesem Internetauftritt präsentieren wir die Ergebnisse mehrerer Monate der Analyse im Land Brandenburg. Wir hoffen, damit die Aufmerksamkeit für diese Idee außerhalb der Region Tübingen zu steigern.
                            """
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
