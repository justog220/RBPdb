from dash import html
import dash_bootstrap_components as dbc

sidebar = html.Div(
    [
        html.Div(
            [
                html.Img(src="./assets/images/base-de-datos.png", style={"width": "3rem"}),
                html.H4("TIF-BD", className="m-0"),
            ],
            className="sidebar-header",
        ),
        html.Hr(),
        dbc.Nav(
            [
                dbc.NavLink(
                    [html.I(className="tf-icons bx bx-info-square fas fa-home"), html.Span("Dashboard" , className="me-2")],
                    href="/",
                    active="exact",
                    className="pe-3"
                ),
                dbc.NavLink(
                    [
                        html.I(className="menu-icon tf-icons bx bx-info-circle"),
                        html.Span("Sobre mí"),
                    ],
                    href="/about",
                    active="exact",
                    className="pe-3",
                ),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    className="sidebar bg-menu-theme",
)