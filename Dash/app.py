import sys
import os
module_path = os.path.abspath(os.path.join(
    os.path.dirname(os.path.abspath(__file__))))
if module_path not in sys.path:
    sys.path.append(module_path)

import dash
import dash_bootstrap_components as dbc
from dash import dcc, html, callback
from components.NavbarVertical import sidebar
from components.Footer import Footer
import glob

ROOT_FOLDER = os.path.abspath(os.path.join(
    os.path.dirname(os.path.abspath(__file__)), os.pardir))
SRC_FOLDER = os.path.join(ROOT_FOLDER, "src/")
DATA_FOLDER = os.path.join(ROOT_FOLDER, "data/")
ASSETS_FOLDER = os.path.join(SRC_FOLDER, "assets")

external_style_sheet = glob.glob(os.path.join(
    ASSETS_FOLDER, "bootstrap/css") + "/*.css")
external_style_sheet += glob.glob(os.path.join(ASSETS_FOLDER,
                                  "css") + "/*.css")
external_style_sheet += glob.glob(os.path.join(ASSETS_FOLDER,
                                  "fonts") + "/*.css")

app = dash.Dash(__name__, title="TIF-BD Dashboard", external_stylesheets=[dbc.themes.BOOTSTRAP] + external_style_sheet, suppress_callback_exceptions =True)

server = app.server

data_store = html.Div()
app.layout = html.Div(className="layout-wrapper layout-content-navbar",
                      children=[
                          html.Div(className="layout-container",
                                   children=[
                                       dcc.Location(id="url"),
                                       data_store,
                                       html.Aside(className="",
                                                  children=[
                                                      sidebar

                                                  ]),
                                       html.Div(className="layout-page",
                                                children=[
                                                    html.Div(className="content-wrapper",
                                                             children=[
                                                                 html.Div(className="container-xxl flex-grow-1 container-p-y p-0",
                                                                          id="page-content",
                                                                          children=[

                                                                          ]),
                                                                 html.Footer(className="content-footer footer bg-footer-theme",
                                                                             children=[
                                                                                 Footer
                                                                             ], style={"margin-left": "6rem"})

                                                             ])
                                                ])

                                   ])
                      ])
if __name__ == "__main__":
    app.run_server(host="0.0.0.0", port=5050)