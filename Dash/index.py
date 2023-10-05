from dash import callback
from dash.dependencies import Input, Output
from pages.about import about_page_content



@callback(
    Output(component_id='page-content', component_property='children'),
    Input(component_id='url', component_property='pathname')
)
def routing(path):
    if path == "/":
        return worldcup_page_content
    elif path == "/about":
        return about_page_content
