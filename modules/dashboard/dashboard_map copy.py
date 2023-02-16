import pandas as pd
import geopandas as gpd
from dash import Dash, html, Output, Input, dcc
from dash.exceptions import PreventUpdate
import dash_leaflet as dl
import dash_bootstrap_components as dbc
from dash_extensions.enrich import html, DashProxy
from dash_extensions.javascript import arrow_function, assign
import plotly.express as px

import base64

###
# Driveways
###

polygon_geojson = dl.GeoJSON(url=f"assets/BB_polygons_final.json", 
                             id="polygon_geojson",
                             options = {"style": {"color": "#3D426B", 
                                                  "opacity": 0.8, 
                                                  "fillOpacity": 0.2, 
                                                  "weight": 2}},
                             hoverStyle = arrow_function({"color": "#3D426B", 
                                                          "fillColor":"#779ecb", 
                                                          "fillOpacity": 0.2, 
                                                          "opacity": 1, 
                                                          "weight": 2}))

# get maximum ranks
max_ranks = gpd.read_file("ds_project/modules/dashboard/assets/BB_polygons_final.json")[["overall_rank", "terrain_rank", "distance_rank", "irradiation_rank"]].agg("max").apply(int)

###
# Gemeinde
###

gemeinde_geojson = dl.GeoJSON(url=f"/assets/BB_gemeinde_final.json",  # url to geojson file
                     #zoomToBounds=True,  # when true, zooms to bounds when data changes (e.g. on load)
                     zoomToBoundsOnClick=True,  # when true, zooms to bounds of feature (e.g. polygon) on click
                     #hoverStyle=arrow_function(dict(weight=5, color='#666', dashArray='')),  # style applied on hover
                     #hideout = dict(colorscale=colorscale, classes=classes, style=style, colorProp="Score"),
                     #options = dict(style=style_handle),
                     options={"style":{"color":"grey", "opacity": 0.5, "fillOpacity": 0.2, "weight": 1}},
                     hoverStyle = arrow_function({"color":"purple", "fillColor":"grey", "fillOpacity": 0.2, "opacity": 0.8, "weight": 2}),
                     id="gemeinde_geojson")

###
# Kreis
###

kreis_geojson = dl.GeoJSON(url=f"/assets/BB_kreis_final.json",  # url to geojson file
                     #zoomToBounds=True,  # when true, zooms to bounds when data changes (e.g. on load)
                     zoomToBoundsOnClick=True,  # when true, zooms to bounds of feature (e.g. polygon) on click
                     options={"style":{"color":"grey", "opacity": 0.5, "fillOpacity": 0.2, "weight": 1}},
                     hoverStyle=arrow_function({"color":"purple", "fillColor":"grey", "fillOpacity": 0.2, "opacity": 0.8, "weight": 2}),
                     id="kreis_geojson")

# define animated icons
def svg_handler(type, score, size = 70):
    if type == "overall":
        string = f"""
        <svg width="{size}px" height="{size}px" version="1.1" viewBox="-20 0 520 347" xml:space="preserve" xmlns="http://www.w3.org/2000/svg">
            <linearGradient id="lg1" x1="0.5" y1="1" x2="0.5" y2="0">
            <stop offset="0%" stop-opacity="1" stop-color="#03c03c"/>
            <stop offset="{score * 100}%" stop-opacity="1" stop-color="#03c03c">
            <animate attributeName="offset" values="0;{score}" repeatCount="1" dur="1s" begin="0s"/>
            </stop>
            <stop offset="{score * 100}%" stop-opacity="0" stop-color="#03c03c">
            <animate attributeName="offset" values="0;{score}" repeatCount="1" dur="1s" begin="0s"/>
            </stop>
            <stop offset="100%" stop-opacity="0" stop-color="#03c03c"/>
            </linearGradient>
            <g fill="url(#lg1)" stroke="#292D32" stroke-linecap="round" stroke-linejoin="round" stroke-width="25">
                <path d="m486.25 4.25v9c-14.15 31.03-30.58 72.23-46 109-3.52 8.39-8.83 31.86-20 31-9.24-0.71-14.1-24.24-17-33-4.94-14.93-7.62-25.51-12-38-50.74 20.65-87.69 53.67-86 122 1.34 54.26 21.16 99.67 33 143h-148c-4.55-115.45-8.99-231.01-13-347h51c11.73 38.61 24.47 76.2 36 115 25.44-24.63 60.55-50.85 103-63-6.69-8.75-16.41-15.01-25-22-7.83-6.37-20.32-12.24-20-26 1.99-0.68 2.29-3.05 4-4h156c0.44 1.23 1.28 2.05 3 2-0.16 1.16 0.22 1.78 1 2z"/>
                <path d="m111.25 0.25h51c-4.53 115.47-8.94 231.06-13 347h-149v-3c37.73-113.94 73.56-229.77 111-344z"/>
            </g>
        </svg>
        """
    if type == "irradiation":
        string = f"""
        <svg height="{size}px" width="{size}px" version="1.1" id="_x32_" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="-64 -64 576 576" xml:space="preserve">
            <linearGradient id="lg2" x1="0.5" y1="1" x2="0.5" y2="0">
            <stop offset="0%" stop-opacity="1" stop-color="#03c03c"/>
            <stop offset="{score * 100}%" stop-opacity="1" stop-color="#03c03c">
            <animate attributeName="offset" values="0;{score}" repeatCount="1" dur="1s" begin="0s"/>
            </stop>
            <stop offset="{score * 100}%" stop-opacity="0" stop-color="#03c03c">
            <animate attributeName="offset" values="0;{score}" repeatCount="1" dur="1s" begin="0s"/>
            </stop>
            <stop offset="100%" stop-opacity="0" stop-color="#03c03c"/>
            </linearGradient>
            <g>
                <path class="st0" d="M458.503,298.25c-9.779-13.392-15.332-26.817-15.308-42.254c-0.024-15.445,5.529-28.846,15.308-42.246
                    c9.803-13.232,23.727-26.343,41.031-36.87c-20.194,1.634-39.164-0.796-54.874-5.746c-15.784-5.078-28.146-12.693-37.192-25.144
                    c-9.062-12.443-12.524-26.568-12.492-43.155c0.13-16.468,3.703-35.261,11.526-53.949c-15.372,13.191-32.146,22.358-47.784,27.558
                    c-15.783,5.135-30.262,6.23-44.846,1.473c-14.616-4.724-25.674-14.117-35.437-27.534C268.842,36.999,260.648,19.71,255.996,0
                    c-4.652,19.71-12.838,36.999-22.439,50.383c-9.755,13.416-20.829,22.81-35.437,27.534c-14.592,4.757-29.063,3.662-44.838-1.473
                    c-15.638-5.2-32.411-14.358-47.784-27.558c7.823,18.688,11.389,37.481,11.518,53.949c0.024,16.588-3.428,30.712-12.491,43.155
                    c-9.055,12.451-21.409,20.065-37.2,25.144c-15.694,4.95-34.665,7.38-54.858,5.746c17.304,10.528,31.228,23.638,41.024,36.87
                    c9.787,13.4,15.332,26.801,15.316,42.246c0.016,15.437-5.529,28.862-15.316,42.254c-9.795,13.232-23.72,26.334-41.024,36.87
                    c20.194-1.634,39.164,0.789,54.858,5.739c15.791,5.086,28.145,12.7,37.2,25.152c9.063,12.435,12.515,26.568,12.491,43.164
                    c-0.129,16.475-3.695,35.252-11.518,53.94c15.373-13.2,32.145-22.359,47.784-27.558c15.774-5.134,30.246-6.229,44.838-1.473
                    c14.608,4.725,25.682,14.117,35.437,27.534c9.602,13.392,17.787,30.672,22.439,50.382c4.652-19.71,12.846-36.99,22.439-50.382
                    c9.763-13.417,20.822-22.81,35.437-27.534c14.592-4.756,29.063-3.662,44.846,1.473c15.638,5.2,32.412,14.358,47.784,27.558
                    c-7.823-18.689-11.396-37.466-11.526-53.949c-0.032-16.588,3.429-30.72,12.492-43.155c9.054-12.452,21.408-20.065,37.192-25.152
                    c15.71-4.95,34.68-7.372,54.874-5.739C482.229,324.585,468.305,311.482,458.503,298.25z M255.996,396.707
                    c-77.7,0-140.702-63.003-140.702-140.711c0-77.708,63.003-140.702,140.702-140.702c77.716,0,140.702,62.994,140.702,140.702
                    C396.699,333.704,333.712,396.707,255.996,396.707z" stroke="#292D32" stroke-width="21.3" stroke-linecap="round" stroke-linejoin="round" fill="url(#lg2)"></path>
            </g>
        </svg>
        """
    if type == "land cover":
        string = f"""
        <svg fill="#000000" height="{size}px" width="{size}px" version="1.1" id="animation_land_cover" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 24 24" xml:space="preserve">
        <linearGradient id="lg3" x1="0.5" y1="1" x2="0.5" y2="0">   
            <stop offset="0%" stop-opacity="1" stop-color="#03c03c"/>
            <stop offset="{score * 100}%" stop-opacity="1" stop-color="#03c03c">
            <animate attributeName="offset" values="0;{score}" repeatCount="1" dur="1s" begin="0s"/>
            </stop>
            <stop offset="{score * 100}%" stop-opacity="0" stop-color="#03c03c">
            <animate attributeName="offset" values="0;{score}" repeatCount="1" dur="1s" begin="0s"/>
            </stop>
            <stop offset="100%" stop-opacity="0" stop-color="#03c03c"/>
        </linearGradient>
        <g>
            <path d="M16.17 10.0599H7.82994C6.64995 10.0599 6.23995 9.26994 6.92995 8.30994L11.1 2.46995C11.59 1.76995 12.41 1.76995 12.89 2.46995L17.06 8.30994C17.76 9.26994 17.35 10.0599 16.17 10.0599 M17.59 17.9999H6.41998C4.83998 17.9999 4.29998 16.9499 5.22998 15.6699L9.21997 10.0599H14.79L18.78 15.6699C19.71 16.9499 19.17 17.9999 17.59 17.9999Z" stroke="#292D32" stroke-width="1" stroke-linecap="round" stroke-linejoin="round" fill="url(#lg3)"></path>
            <path d="M12 22V18" stroke="#292D32" stroke-width="1" stroke-linecap="round" stroke-linejoin="round"></path>
        </g>
        </svg>
        """
    if type == "grid":
        string = f"""
        <svg fill="#000000" height="{size*0.8}px" width="{size*0.8}px" version="1.1" id="Layer_1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" 
            viewBox="-50 0 535 485" xml:space="preserve">
        <linearGradient id="lg4" x1="0.5" y1="1" x2="0.5" y2="0">   
            <stop offset="0%" stop-opacity="1" stop-color="#03c03c"/>
            <stop offset="{score * 100}%" stop-opacity="1" stop-color="#03c03c">
            <animate attributeName="offset" values="0;{score}" repeatCount="1" dur="1s" begin="0s"/>
            </stop>
            <stop offset="{score * 100}%" stop-opacity="0" stop-color="#03c03c">
            <animate attributeName="offset" values="0;{score}" repeatCount="1" dur="1s" begin="0s"/>
            </stop>
            <stop offset="100%" stop-opacity="0" stop-color="#03c03c"/>
        </linearGradient>
        <g>
        <polygon fill="url(#lg4)" points="485,141.748 485,76.926 308.644,0 176.356,0 0,76.926 0,141.748 159.45,141.748 67.511,455 0,455 0,485 485,485 485,455 417.48900000000003,455 325.55,141.748 485,141.748" stroke = "none" stroke-width="0"></polygon>
            <path d="M485,141.748V76.926L308.644,0H176.356L0,76.926v64.822h159.45L67.511,455H0v30h485v-30h-67.511L325.55,141.748H485z
                M194.485,111.748V30h96.029v81.748H194.485z M455,111.748H320.515v-73.84L455,96.57V111.748z M30,96.57l134.485-58.663v73.84H30
                V96.57z M372.125,455h-259.25L242.5,313.804L372.125,455z M262.863,291.624l57.142-62.243l53.706,182.985L262.863,291.624z
                M111.289,412.366l53.706-182.985l57.142,62.243L111.289,412.366z M310.139,195.766L242.5,269.442l-67.639-73.676l15.854-54.018
                h103.569L310.139,195.766z" fill="#292D32"/>
        </g>
        </svg>
        """
    if type == "terrain":
        string = f"""
        <svg width="{size}px" height="{size}px" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
        <linearGradient id="lg5" x1="0.5" y1="1" x2="0.5" y2="0">   
            <stop offset="0%" stop-opacity="1" stop-color="#03c03c"/>
            <stop offset="{score * 100}%" stop-opacity="1" stop-color="#03c03c">
            <animate attributeName="offset" values="0;{score}" repeatCount="1" dur="1s" begin="0s"/>
            </stop>
            <stop offset="{score * 100}%" stop-opacity="0" stop-color="#03c03c">
            <animate attributeName="offset" values="0;{score}" repeatCount="1" dur="1s" begin="0s"/>
            </stop>
            <stop offset="100%" stop-opacity="0" stop-color="#03c03c"/>
        </linearGradient>
        <path d="M13 14L17 9L22 18H2.84444C2.46441 18 2.2233 17.5928 2.40603 17.2596L10.0509 3.31896C10.2429 2.96885 10.7476 2.97394 10.9325 3.32786L15.122 11.3476" stroke="#292D32" stroke-width="1" stroke-linecap="round" stroke-linejoin="round" fill="url(#lg5)"></path>
        </svg>
        """
    img_data = base64.b64encode(string.encode())
    img_data = img_data.decode()
    return "{}{}".format("data:image/svg+xml;base64, ", img_data)

# define info box
def get_info(feature=None):
    header = [html.H4("Gemeindestatistiken")]
    if not feature:
        return header + [html.P("Zoome für weitere Statistiken\nauf eine Gemeinde")]
    if feature["properties"]["NAME_3"] is not None:
        if feature["properties"]["suitable_area"] is not None:
            return header + [html.B(feature["properties"]["NAME_3"]), html.Br(),
                            "Potentialfläche in m2: {:.2f}".format(feature["properties"]["suitable_area"]), html.Br(),
                            "Durchschnittliche Wertung: {:.2f}".format(feature["properties"]["overall_score"]), html.Br(),
                            "Klicke für weitere Statistiken auf eine Potentialfläche!"]
        else:
            return header + [html.B(feature["properties"]["NAME_3"]), html.Br(),
                            "Potentialfläche in m2: 0", html.Br(),
                            "Durchschnittliche Wertung: --", html.Br(),
                            "Klicke für weitere Statistiken auf eine Potentialfläche!"]
info = html.Div(children=get_info(), id="info", className="info",
                style={"position": "absolute", "top": "10px", "right": "50px", "z-index": "1000"})


tile_layer = dl.TileLayer(url="http://localhost:8080/styles/positron/{z}/{x}/{y}.png", id="tile_layer", 
                          attribution = '&copy; <a href="https://openmaptiles.org/">OpenMapTiles</a> &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, &copy; <a href="https://gadm.org">GADM</a>')

###
# App assembly
###

# core
app = Dash(prevent_initial_callbacks = True, external_stylesheets = [dbc.themes.BOOTSTRAP])
# layout
app.layout = html.Div([
    dbc.Row([
        dbc.Col([dl.Map(children = [tile_layer, 
                                    dl.Pane([kreis_geojson], id = "regional-polygon", style = {"zIndex": 200}), 
                                    dl.Pane([polygon_geojson], style = {"zIndex": 300}), 
                                    dl.Pane(dl.FeatureGroup(id = "grid-access"), style = {"zIndex": 350}),
                                    dl.Pane([info], style = {"zIndex": 400})], 
                        style={'width': '100%', 'height': '75vh', 'margin': "auto", "display": "block"},
                        id = "map", center = [52.47288, 13.39777], zoom = 7)],
                width = {"size": 12, "offset": 0})
        ]),
    html.Div(id = "test"),
    html.Div(id = "info-panel")
    
])

###
# Interactivity
###

# a lagged state variable
state = {"zoom": 7, "clickedPolygon": ""}

# a callback that controls what polygons are shown
@app.callback(Output("regional-polygon", "children"), Input("map", "zoom"))
def func(viewport):
    #if ((viewport > 12) & (state["zoom"] <= 12)):
    #    state["zoom"] = viewport
    #    print("A2")
    #    return [tile_layer, polygon_geojson, info]
    if ((viewport > 8) & (state["zoom"] <= 8)):#(((viewport > 7) & (viewport <= 12)) & ((state["zoom"] <= 7) | (state["zoom"] > 12))):
        state["zoom"] = viewport
        return [gemeinde_geojson]
    elif ((viewport <= 8) & (state["zoom"] > 8)):
        state["zoom"] = viewport
        return [kreis_geojson]
    else:
        state["zoom"] = viewport
        raise PreventUpdate()

# a callback that controls the info box
@app.callback(Output("info", "children"), [Input("gemeinde_geojson", "hover_feature")])
def info_hover(feature):
    return get_info(feature)


# a callback that updates the info panel
@app.callback(Output("info-panel", "children"), Input("polygon_geojson", "click_feature"))
def info_click(feature):
    if feature is not None:
        # try and get core data
        state["clickedPolygon"] = [feature["properties"]["link_id"], feature["properties"]["id"]]
        link_name = "Nr. " + str(int(feature["properties"]["link_id"][-4:])) + \
            "/" + str(int(feature["properties"]["id"])) + \
            " (" + feature["properties"]["NAME_4"] + ")"
        suitable_area = "{:.2f}".format(feature["properties"]["suitable_area"])
        overall_score = "{:.2f}".format(feature["properties"]["overall_score"])
        overall_rank = "{:.0f}".format(feature["properties"]["overall_rank"])
        # make pie chart
        df = px.data.tips()
        fig = px.pie(df, values='tip', names='day')
        fig.layout.update()
        fig.update_traces(textposition='inside')
        fig.update_layout(uniformtext_minsize=12, uniformtext_mode='hide',
                          margin = dict(l=0, r=0, t=0, b=0), showlegend = False)
        # get image of terrain
        try:
            with open("ds_project/modules/dashboard/assets/imagery/height_profile/" + feature["properties"]["link_id"] + "_" + str(int(feature["properties"]["id"])) + ".png", "rb") as image_file:
                terrain_image = "data:image/png;base64,{}".format(
                    base64.b64encode(image_file.read()).decode('ascii'))
        except:
            terrain_image = None
        # terrain data
        terrain_roughness = "{:.2f}".format(
            feature["properties"]["terrain_roughness"])
        terrain_high = "{:.2f}".format(feature["properties"]["terrain_high"])
        terrain_low = "{:.2f}".format(feature["properties"]["terrain_low"])
        terrain_score = "{:.2f}".format(feature["properties"]["terrain_score"])
        terrain_rank = "{:.0f}".format(feature["properties"]["terrain_rank"])
        # get distance data
        
        grid_subset = grid.loc[((grid["link_id"] == state["clickedPolygon"][0]) & (grid["id"] == state["clickedPolygon"][1])),:].sort_values("distance_substation")
        distance = "{} in {:.0f}m".format(grid_subset["municipality"][grid_subset.distance_substation.idxmin()], grid_subset["distance_substation"][grid_subset.distance_substation.idxmin()])
        distance_score = "{:.2f}".format(
            feature["properties"]["distance_score"])
        distance_rank = "{:.0f}".format(feature["properties"]["distance_rank"])
        # get irradiation data
        irradiation = "{:.2f}".format(feature["properties"]["irradiation"])
        irradiation_score = "{:.2f}".format(
            feature["properties"]["irradiation_score"])
        irradiation_rank = "{:.0f}".format(feature["properties"]["irradiation_rank"])
        #
        return [dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4("Fläche", className="card-title"),
                        html.B(link_name), html.Br(),
                        html.Span("Potentialfläche in m²: ", style={
                                  "color": "grey"}), suitable_area, html.Br(),
                        html.Span([
                            html.Span("Gesamtwertung: ", style={"color": "grey"}), overall_score, " ⓘ"],
                            id = "item-overall-score", style={"cursor": "pointer"},
                        ), html.Br(),
                        dbc.Tooltip(["Die Gesamtwertung errechnet sich als ein gewichtetes Mittel der anderen Wertungen. ", html.Br(),
                                    "Dabei fließt die Landbedeckung zu 50%, die Geländebeschaffenheit zu 10%, ",
                                    "der Netzanschluss zu 30% und das Sonnenpotential zu 10% ein."], 
                                    delay = {"show": 20, "hide": 50}, target = "item-overall-score", placement = "right"),
                        html.Span("Gesamtrang: ", style={"color": "grey"}), overall_rank, "/", max_ranks["overall_rank"]]),
                        dbc.CardFooter([
                            html.Img(src = svg_handler("overall", feature["properties"]["overall_score"]),
                                id = "sym-overall", style = {"cursor": "pointer"}),
                            dbc.Tooltip("Gesamtwertung", target = "sym-overall"),
                            #
                            html.Img(src = svg_handler("land cover", 1),
                                id = "sym-land", style = {"cursor": "pointer"}),
                            dbc.Tooltip(["Wertung der", html.Br(), "Landbedeckung"], target = "sym-land"),
                            #
                            html.Img(src = svg_handler("terrain", feature["properties"]["terrain_score"]),
                                id = "sym-terrain", style = {"cursor": "pointer"}),
                            dbc.Tooltip(["Wertung der", html.Br(), "Geländebeschaffenheit"], target = "sym-terrain"),
                            #
                            html.Img(src = svg_handler("grid", feature["properties"]["distance_score"]),
                                id = "sym-distance", style = {"cursor": "pointer"}),
                            dbc.Tooltip(["Wertung des", html.Br(), "Netzanschlusses"], target = "sym-distance"),
                            #
                            html.Img(src = svg_handler("irradiation", feature["properties"]["irradiation_score"]),
                                id = "sym-irradiation", style = {"cursor": "pointer"}),
                            dbc.Tooltip(["Wertung des", html.Br(), "Sonnenpotentials"], target = "sym-irradiation")
                        ], class_name = "text-center") #style = {"margin-left": "auto", "margin-right": "auto", "display": "block"}
                ], class_name="mt-1 h-100")
            ], md = {"size": 4}, xs = {"size": 12}),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4("Landbedeckung", className="card-title"),
                        dbc.Row([
                            dbc.Col([html.Img(src=terrain_image, width="100px", height="100px"), html.Br(),
                                         html.Span("© GeoBasis-DE/LGB", style = {"font-size": "0.8rem"})
                                     ], width={
                                    "size": 4}),
                            dbc.Col([html.Span("Nutzbare Fläche in m2: ", style={"color": "grey"}), "--", html.Br(),
                                     html.Span("Wertung: ", style={
                                               "color": "grey"}), "--", html.Br(),
                                     html.Span("Rang: ", style={"color": "grey"}), "--"], width={"size": 4}),
                            dbc.Col([dcc.Graph(id="graph", figure=fig, style={
                                    'width': '150px', 'height': '150px'})], width={"size": 4})
                        ])
                    ]),
                ], class_name="mt-1 h-100")
            ], md = {"size": 8}, xs = {"size": 12})], class_name="m-1"),
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H4("Geländebeschaffenheit",
                                    className="card-title"),
                            dbc.Row([
                                dbc.Col([html.Img(src = terrain_image, width="150px", height="150px"), html.Br(),
                                         html.Span("© GeoBasis-DE/LGB", style = {"font-size": "0.8rem"})], width={
                                        "size": 6}, class_name = "h-100 justify-content-center align-items-center"),
                                dbc.Col([html.Span("Mittlere Abweichung der Steigung in Grad: ", style={"color": "grey"}), terrain_roughness, html.Br(),
                                         html.Span("Hochpunkt: ", style={"color": "grey"}), terrain_high, html.Span(
                                             "  Tiefpunkt: ", style={"color": "grey", "cursor": "pointer"}), terrain_low, html.Br(),
                                         html.Span([html.Span("Wertung: ", style={"color": "grey"}), terrain_score, " ⓘ"],
                                            id = "item-terrain-score", style={"cursor": "pointer"},
                                        ), html.Br(),
                                         dbc.Tooltip(["Die Geländebeschaffenheit wird relativ zum unteren Referenzwert ",
                                                      "von 90 Grad bewertet"], 
                                                     delay = {"show": 20, "hide": 50}, target = "item-terrain-score"),
                                         html.Span("Rang: ", style={"color": "grey"}), terrain_rank, "/", max_ranks["terrain_rank"]], width={"size": 6})
                            ])
                        ]),
                    ], class_name="mt-1 h-100")
                ], md = {"size": 4}, xs = {"size": 12}),
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H4("Netzanschluss", className="card-title"),
                            html.Span("Nächster Netzanschlusspunkt: ", style={
                                      "color": "grey"}), html.Br(),
                            "  ", distance, html.Br(),
                            html.Span([html.Span("Wertung: ", style={"color": "grey"}), distance_score, " ⓘ"],
                                            id = "item-grid-score", style={"cursor": "pointer"}), html.Br(),
                            dbc.Tooltip(["Der Netzanschluss wird relativ zum schlechtesten ",
                                         "in Brandenburg beobachteten Wert bewertet"], 
                                         delay = {"show": 20, "hide": 50}, target = "item-grid-score"),
                            html.Span("Rang: ", style={"color": "grey"}), distance_rank, "/", max_ranks["distance_rank"], html.Br(),
                            dbc.Button("Nächstgelegene 3 Netzanschlusspunkte anzeigen", id="show-grid-access", color="primary", class_name="mr-1 float-end", style={"margin-top": "10px"})
                        ]),
                    ], class_name="mt-1 h-100")
                ], md = {"size": 4}, xs = {"size": 12}),
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H4("Sonnenpotential", className="card-title"),
                            html.Span("Durchschnittliche Wh/m² pro Monat: ",
                                      style={"color": "grey"}), irradiation, html.Br(),
                            html.Span([html.Span("Wertung: ", style={"color": "grey"}), irradiation_score, " ⓘ"],
                                            id = "item-irradiation-score", style={"cursor": "pointer"}), html.Br(),
                            dbc.Tooltip(["Das Sonnenpotential wird relativ zum schlechtesten ",
                                         "in Deutschland beobachteten Wert bewertet"], 
                                         delay = {"show": 20, "hide": 50}, target = "item-irradiation-score"),
                            html.Span("Rang: ", style={"color": "grey"}), irradiation_rank, "/", max_ranks["irradiation_rank"]
                        ]),
                    ], class_name="mt-1 h-60"),
                    dbc.Card([
                        dbc.CardBody([
                            html.H4("Quellen", className="card-title"), 
                            html.Div([
                                dcc.Link("OpenStreetMap", href = "https://www.openstreetmap.org/", target="_blank"), ", ",
                                dcc.Link("DOP20: GeoBasis-DE/LGB", href = "https://geobroker.geobasis-bb.de/gbss.php?MODE=GetProductPreview&PRODUCTID=7a503f0f-db46-4772-80e3-b27733fd7acd", target="_blank"), ", ",
                                dcc.Link("DGM01: GeoBasis-DE/LGB", href = "https://geobroker.geobasis-bb.de/gbss.php?MODE=GetProductPreview&PRODUCTID=414f568f-639b-4b5a-ba92-57fdac396799", target="_blank"), ", ",
                                dcc.Link("GADM", href = "https://gadm.org/data.html", target="_blank"), ", ",
                                dcc.Link("CM SAF", href = "https://doi.org/10.5676/EUM_SAF_CM/SARAH/V002", target="_blank"), html.Br(),
                            ], style = {"font-size": "0.8rem"})
                        ]),
                    ], class_name="mt-1 h-40")
                ], md = {"size": 4}, xs = {"size": 12})
            ], class_name="m-1")
        ]

    else:
        return dbc.Row()
    
# loading the data on grid access
grid = pd.read_csv("ds_project/modules/dashboard/assets/BB_ps_auxiliary.csv")

# a callback that add lines to the closest grid points
@app.callback([Output("grid-access", "children"), Output("show-grid-access", "children")], Input("show-grid-access", "n_clicks")) #
def info_click(n):
    if n is None:
        raise PreventUpdate()
    elif n % 2 == 1:
        tmp = grid.loc[((grid["link_id"] == state["clickedPolygon"][0]) & (grid["id"] == state["clickedPolygon"][1])),:]
        return [dl.Marker(position=(tmp["lat_substation"][i], tmp["lon_substation"][i])) for i in tmp.index], "Nächstgelegene 3 Netzanschlusspunkte ausblenden"
    else:
        return [], "Nächstgelegene 3 Netzanschlusspunkte anzeigen"
###
# Run app
###

if __name__ == '__main__':
        app.run_server(host="0.0.0.0", port=8050, debug = False)# 
#docker run -it -v $(pwd):/data -p 8080:8080 maptiler/tiles