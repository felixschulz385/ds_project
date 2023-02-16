import dash
import dash_bootstrap_components as dbc

# bootstrap theme
# https://bootswatch.com/lux/
external_stylesheets = [dbc.themes.LITERA]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

path_directory = "/home/jan/Uni/DS-Project/modules/dashboard/test/"
#path_directory = "/home/ubuntu/ext_drive/dashboard/ds_project/modules/dashboard/test/"

server = app.server
app.config.suppress_callback_exceptions = True