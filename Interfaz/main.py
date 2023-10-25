import urllib.request as urlreq
from dash import Dash, html, dcc, callback, Output, Input, dash_table, State
import dash_bio as dashbio
import dash_bootstrap_components as dbc
import psycopg2
from dash.exceptions import PreventUpdate
import pandas as pd
import plotly.express as px
app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.themes.SLATE], prevent_initial_callbacks=True, title="RBPDB", suppress_callback_exceptions=True)

conn = psycopg2.connect(
    database="RBPDB",
    host="localhost",
    user="postgres",
    password="123456",
    port="5432"
)

cursor = conn.cursor()
cursor.execute("SELECT uniprotid FROM proteina")
UniProtIDs = [i[0] for i in cursor.fetchall()]
secuencia = '-'
titulo = " "

cursor.execute("SELECT nombre FROM especie")
especies = [i[0] for i in cursor.fetchall()]
options = [{"label": especie.capitalize(), "value": especie} for especie in especies]

puntoIso = html.Div([
    html.Div(
        className="card text-white bg-primary mb-3",
        children=[
            html.H4("Punto isoeléctrico", className="card-header", style={"text-align":"center"}),
            html.Div(id="resultado-texto-pi", style={"text-align":"center"})
        ]
    )
], className="six columns")


descripcion = html.Div([
    html.Div(
        className="card text-white bg-primary mb-3",
        children=[
            html.H4("Descripcion", className="card-header", style={"text-align":"center"}),
            html.Div(id="resultado-texto-desc", style={"text-align":"center"})
        ]
    )
], className="six columns")


dominios = html.Div([
    html.Div(
        className="card text-white bg-primary mb-3",
        children=[
            html.H4("Dominios", className="card-header", style={"text-align":"center"}),
            html.Div(id="resultado-texto-doms", style={"text-align":"center"})
        ]
    )
], className="six columns")


pesoMol = html.Div(
    className="card text-white bg-primary mb-3",
    children=[
        html.H4("Peso molecular", className="card-header", style={"text-align":"center"}),
        html.Div(id="resultado-texto-pesomol", style={"text-align":"center"})
    ]
)

infoProt = html.Div([
    html.Div([
        html.Div(className="col-6",
            children=[
                descripcion,
            ]),

        html.Div(className="col-6",
            children=[
                dominios,
            ]),
        html.Div(className="col-6",
            children=[
                pesoMol,
            ]),
        html.Div(className="col-6",
            children=[
                puntoIso,
            ]),  
    ], className="row")

], className="container",
style={'display': 'flex', 'flex-direction': 'column', 'align-items': 'center', 'justify-content': 'center'})

estructuraSec = html.Div([
    dcc.Graph(id='estructura-secundaria')
])

pie = html.Div(
    className="card text-white bg-primary mb-3",
    children=[
        html.H4("Fracciones de estructura secundaria", className="card-header", style={"text-align":"center"}),
        estructuraSec
    ],
)

seqvw = html.Div([
    html.H2("Proteínas"),
    dcc.Dropdown(options=especies, value=especies, multi=True, id='selector-especie', className="dropdown"),
    html.Div('', style={'margin':'20px'}),
    dcc.Dropdown(options=UniProtIDs, id='drop-down-proteina', style={'width':'100%', 'margin-left':'0px'}),
    html.Div('', style={'margin':'20px'}),
    dashbio.SequenceViewer(
        id='sequence-viewer',
        sequence=secuencia,
        showLineNumbers=True,
        charsPerLine=20,
        toolbar=True,
        title=titulo
    ),
    html.Button("Descargar secuencia", id="btn_txt", className="btn btn-primary"), 
    dcc.Download(id="download-text-index"),
    html.Div('', style={'margin':'10px'}),
    html.Div([
        html.A(children='UniProt', id="url-uniprot", className="btn btn-primary", target="_blank", style={"width":"100%"}),
        html.A(children="Genbank", id="url-genbank", className="btn btn-primary", target="_blank", style={"width":"100%"}),
    ], style={"display":"flex","flex-direction":"columns","justify-content":"space-between","margin":"auto","align-items":"center","width":"100%"},
    id="div-redirects"),
    html.Div('', style={'margin':'10px'}),
], style={"padding-left":"20px", 'display': 'flex', 'flex-direction': 'column'})


div_seq_info = html.Div([
    html.Div(seqvw, className="col-6"),
    html.Div(infoProt, className="col-6", style={'display': 'flex', 'justify-content': 'center'}),
    html.Div(pie, className="col-6", style={"margin":"0 auto"})
], className="row")

cursor.execute("SELECT * FROM vista_recuento_entradas")
dfCounts = pd.DataFrame(cursor.fetchall(), columns=[desc[0] for desc in cursor.description])

info = html.Div([
    html.Div([
        html.H2("Información")
    ], className="row"),

    html.Div([
        html.Div(className="col-6",
            children=[
                html.Div(className="card text-white bg-dark mb-3",
                    children=[
                        html.H4("Número de proteínas", className="card-header"),
                        html.P(children=dfCounts["proteina_count"], style={"text-align":"center"}),
                    ]),
            ]),

        html.Div(className="col-6",
            children=[
                html.Div(className="card text-white bg-dark mb-3",
                    children=[
                        html.H4("Número de Referencias", className="card-header"),
                        html.P(children=dfCounts["referencia_count"], style={"text-align":"center"}),
                    ]),
            ]),
        html.Div(className="col-6",
            children=[
                html.Div(className="card text-white bg-dark mb-3",
                    children=[
                        html.H4("Número de especies", className="card-header"),
                        html.P(children=dfCounts["especie_count"], style={"text-align":"center"}),
                    ]),
            ]),
        html.Div(className="col-6",
            children=[
                html.Div(className="card text-white bg-dark mb-3",
                    children=[
                        html.H4("Número de autores", className="card-header"),
                        html.P(children=dfCounts["autor_count"], style={"text-align":"center"}),
                    ]),
            ]),
    ], className="row")

], className="container",
style={'height': '90vh', 'display': 'flex', 'flex-direction': 'column', 'align-items': 'center', 'justify-content': 'center'})


autores = html.Div([
])

def load_data_autores():
    consulta = "SELECT au.nombre AS Autor, COUNT(rel.id_autor) AS TotalReferencias FROM autor as au JOIN ref_tiene_autor as rel ON au.id_autor = rel.id_autor GROUP BY au.nombre ORDER BY TotalReferencias DESC"
    cursor.execute(consulta)
    return pd.DataFrame(cursor.fetchall(), columns=[desc[0] for desc in cursor.description])

def load_data_table():
    df = load_data_autores()
    return html.Div([
        dash_table.DataTable(
            df.to_dict('records'),
            columns=[
                {"name":i, "id":i, "deletable": False, "selectable":False} for i in df.columns
            ],
            editable=False,
            filter_action="native",
            row_deletable=False,
            page_action="native",
            page_current=0,
            page_size=10,
        )
    ], id="datatable-autores", style={'display':'flex','flex-direction':'column','align-items':'center','justify-content':'center', 'height':'100vh', 'margin':'auto'})


navbar = dbc.Navbar(
    children=[
        html.A(
            dbc.Row(
                [
                    # dbc.Col(
                    #     html.Img(src="/assets/base-de-datos.png", width="40px", style={"margin-right":"10px"}),
                    #     width="auto",
                    # ),
                    dbc.Col(dbc.NavbarBrand("RBPDB", className="ml-2"), style={"margin":'0'}, width="auto")
                ],
                align="center",
            ),
            href="/"
        ),
        dbc.NavItem(dbc.NavLink("Proteínas", href="/seqview")),
        dbc.NavItem(dbc.NavLink("Autores", href="/autores"))
    ],
    className="navbar navbar-expand-lg navbar-dark bg-dark",
)

footer = dbc.Container(
    dbc.Row(
        dbc.Col(
            html.P("2023 Garcia Justo", className="text-muted"),
            className="mt-3"
        )
    )
)

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    navbar,
    html.Div(id="page-content", className="navbar bg-primary"),
    footer,  
], style={"overflow-x":"hidden","max-width":"100%"},)

@callback(
        Output('page-content', 'children'),
        Input('url', 'pathname')
)
def display_page(pathname):
    if pathname == '/seqview':
        # return seqvw
        return div_seq_info
    elif pathname == '/autores':
        tabla = load_data_table()
        return tabla
    else:
        return info



@callback(
    Output('sequence-viewer', 'sequence'),
    Output('sequence-viewer', 'title'),
    Output('resultado-texto-pi', 'children'),
    Output('resultado-texto-desc', 'children'),
    Output('resultado-texto-pesomol','children'),
    Output('resultado-texto-doms', 'children'),
    Output('estructura-secundaria', 'figure'),
    Output('url-uniprot','href'),
    Output('url-genbank','href'),
    Input('drop-down-proteina', 'value')
)
def actualizar_seq(value):
    if value is None:
        secuencia = "-"
        pi = '-'
        desc = '-'
        pesomol = '-'
        doms = "-"
        fig = px.pie(None)
        url = None
        urlGB = None
    else:
        consulta = f"SELECT * FROM proteina WHERE uniprotid = '{value}'"
        cursor.execute(consulta)
        df = pd.DataFrame(cursor.fetchall(), columns=[desc[0] for desc in cursor.description])
        id_prot = int(df["id_proteina"])
        consulta = f"SELECT sec.secuencia FROM secuencia as sec WHERE sec.id_proteina = '{id_prot}'"
        cursor.execute(consulta)
        secuencia = [i[0] for i in cursor.fetchall()]
        # consulta = f"SELECT pi FROM proteina WHERE uniprotid = '{value}'"
        # cursor.execute(consulta)
        # pi = [i[0] for i in cursor.fetchall()][0]
        pi = df["pi"]
        # consulta = f"SELECT descripcion FROM proteina WHERE uniprotid = '{value}'"
        # cursor.execute(consulta)
        # desc = [i[0] for i in cursor.fetchall()][0]
        desc = df["descripcion"]
        pesomol = df["pesomol"]
        # consulta = f"SE"
        doms = df['dominios']

        fracciones = [df["fracciongiro"], df["fraccionhelice"], df["fraccionhoja"]]
        fracciones = [float(i) for i in fracciones]
        data = pd.DataFrame({
            "fraccion" : ["Giro", "Helice", "Hoja"],
            "porcentaje" : fracciones
        })
        
        fig = px.pie(data, values="porcentaje", names="fraccion")
        value = value + "\n" 


        url = f"https://www.uniprot.org/uniprotkb/{value}/entry"

        consulta = f"SELECT gen.nombre FROM gen WHERE gen.id_proteina = {id_prot}"
        cursor.execute(consulta)
        gen = [i[0] for i in cursor.fetchall()][0]
        if gen:
            urlGB = f'https://www.ncbi.nlm.nih.gov/gene/?term={gen}'
        else:
            urlGB = None

    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        legend_title_font=dict(color='white'),
        legend_font=dict(color='white')
    ) 


    fig.update_traces(
        textfont=dict(color='white'),
        textinfo='percent+label',
        hovertemplate='%{label}: %{percent} <br>',
        insidetextfont=dict(color="white")
        )

    return secuencia, value, pi, desc, pesomol, doms, fig, url, urlGB

@callback(
    Output('drop-down-proteina', 'options'),
    Input('selector-especie', 'value')
)
def filtrado(values):
    opciones = []
    for i in values:
         consulta = f"SELECT prot.uniprotid FROM proteina as prot WHERE prot.id_especie = (SELECT esp.id_especie FROM especie as esp WHERE esp.nombre = '{i}')"
         cursor.execute(consulta)
         buff = [j[0] for j in cursor.fetchall()]
         opciones.extend(buff)
    return opciones

@callback(
    Output("download-text-index", "data"),
    Input("btn_txt", "n_clicks"),
    Input("drop-down-proteina", "value"),
    Input("sequence-viewer", "sequence")
)
def func(n_clicks, value, sequence):
    if n_clicks is None:
        raise PreventUpdate
    else:
        contenido = f">{value}\n{sequence}"
        return dict(content=contenido, filename=f"{value}.fasta")
if __name__ == '__main__':
    app.run_server()