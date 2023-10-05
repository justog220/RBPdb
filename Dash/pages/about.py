import sys
import os
from dash import html
import utils.theme as theme
from utils.consts import GITHUB_PROFILE

about_me_text= "Soy Justo Garcia"

about_page_content = html.Div(className="col-md-12 col-sm-12 col-lg-8 mb-md-0 mb-4 card-chart-container", children=[html.Div(className="card", children=[
        html.Div(className="card-body p-0", children=[
            html.Div(className="d-flex justify-content-between", children=[
                html.Div(className="card-info p-4 w-75",
                         children=[html.H3(className="card-text", children=["Quién soy?"]),
                                    html.H2(className="card-text m-0 p-0", children=["Justo Garcia"] , style={"color":theme.COLOR_PALLETE[0]}),
                                   html.Div(className="mb-2 mt-2", children=[
                                       html.P(className="card-title mb-2",
                                            children=[about_me_text], style={"font-size":"1rem"}),
                                   ]),
                                   html.Small(
                             className="card-text", children=[]),

                             html.A(href=GITHUB_PROFILE,target="_blank",
                             children=[html.I(className="bx bxl-github mt-3" , style={"font-size":"2.5rem" , "color":"#24292f"})]),
                         ])
            ])

        ])
    ])
    ]
    )

