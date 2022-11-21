import base64
import datetime
import io
import os
import random as rnd
import pandas as pd
import time
import datetime as dt
import dash
import plotly.graph_objects as go 
from dash import html, dcc, dash_table, callback,ctx
from dash.exceptions import PreventUpdate
from dash.dependencies import Input, Output, State
from collections import deque
import dash_bootstrap_components as dbc

dash.register_page(__name__, path='/',title="Utilização de AR nas práticas de Engenharia de Manutenção")

GRAPH_INTERVAL = os.environ.get("GRAPH_INTERVAL", 1000)

X = deque(maxlen=20)
X.append(1)

checklist_modal_layout = dbc.Modal([
    dbc.ModalHeader(dbc.ModalTitle("CHECKLIST 5S",id="modal-title")),
    dbc.ModalBody(id="modal-body",),
    dbc.ModalFooter("Última atualização:")
],id="modal-fs",fullscreen=True)

tab2_layout = html.Div([
    dbc.Label("Tipo de documento"),
    dbc.RadioItems(options=[
        {"label":"Checklist", "value":1},
        {"label":"Lista de compras", "value":2},
        {"label":"Notificação de trabalhos especiais", "value":3},
    ],value=1,id="radioitems-inline-input",inline=True),
    html.Hr(),
    html.Div(id='output-data-upload',style={'maxHeight':"200px",'overflow':"scroll"}),
    html.Hr(),
    dcc.Upload(
        id='upload-data',
        children=html.Div([
            "Arraste e solte ou",html.A(" selecione o arquivo")
        ]),
        style={
            "width":"100%",
            "height":"50px",
            "lineHeight":"50px",
            "borderWidth":"1px",
            "borderStyle":"dashed",
            "borderRadius":"5px",
            "textAlign":"center",
            "margin":"10px"
        },multiple=True
    )
])

tab1_layout = html.Div([
    dbc.Accordion([
        dbc.AccordionItem([dbc.ListGroup([
            dbc.ListGroupItem("DIÁRIO DE TURNO", id="",action=True, n_clicks=0),
            dbc.ListGroupItem("NÃO CONFORMIDADE", id="",action=True, n_clicks=0),
            dbc.ListGroupItem("PARADA NÃO PROGRAMADA", id="",action=True, n_clicks=0),
            dbc.ListGroupItem("PARADA PROGRAMADA", id="",action=True, n_clicks=0),
        ])],title="EMISSÃO DE RELATÓRIOS"),
        dbc.AccordionItem([dbc.ListGroup([
            dbc.ListGroupItem("LOGS DE MÁQUINAS", id="",action=True, n_clicks=0),
            dbc.ListGroupItem("CONSUMO DE INSUMOS", id="",action=True, n_clicks=0),
            dbc.ListGroupItem("LISTA DE COMPRAS", id="",action=True, n_clicks=0),
            dbc.ListGroupItem("DIÁRIOS DE TURNO", id="",action=True, n_clicks=0),
            dbc.ListGroupItem("NÃO CONFORMIDADES", id="",action=True, n_clicks=0),
            dbc.ListGroupItem("PARADAS NÃO PROGRAMADAS", id="",action=True, n_clicks=0),
            dbc.ListGroupItem("PARADAS PROGRAMADAS", id="",action=True, n_clicks=0),
            dbc.ListGroupItem("FECHAMENTO MENSAL", id="",action=True, n_clicks=0),
        ])],title="IMPRESSÃO DE RELATÓRIOS"),
    ],start_collapsed=True)
])

card_OEE = [
    dbc.CardBody([
        html.H5("OEE",className="card-title"),
        html.P("INDICADOR 1"),
    ])]

card_TEEP = [
    dbc.CardBody([
        html.H5("TEEP",className="card-title"),
        html.P("INDICADOR 1"),
    ])]

card_DOWTIME = [
    dbc.CardBody([
        html.H5("DOWNTIME",className="card-title"),
        html.P("INDICADOR 1"),
    ])
]

card_NP = [
    dbc.CardBody([
        html.H5("PARADAS NÃO PROGRAMADAS",className="card-title"),
        html.P("INDICADOR 1"),
    ])
]

card_CA = [
    dbc.CardBody([
        html.H5("CHAMADOS EM ABERTO",className="card-title"),
        html.P("INDICADOR 1"),
    ])
]

indicadores_layout = dbc.Row([
    dbc.Col(dbc.Card(card_OEE,color="light"),class_name="shadow-sm p-3 mb-5 bg-white rounded text-center"),
    dbc.Col(dbc.Card(card_TEEP,color="light"),class_name="shadow-sm p-3 mb-5 bg-white rounded text-center"),
    dbc.Col(dbc.Card(card_DOWTIME,color="light"),class_name="shadow-sm p-3 mb-5 bg-white rounded text-center"),
    dbc.Col(dbc.Card(card_NP,color="light"),class_name="shadow-sm p-3 mb-5 bg-white rounded text-center"),
    dbc.Col(dbc.Card(card_CA,color="light"),class_name="shadow-sm p-3 mb-5 bg-white rounded text-center"),
])

checklist_layout = html.Div([
    dbc.Accordion([
        dbc.AccordionItem([dbc.ListGroup([
            dbc.ListGroupItem("CHECKLIST 5S", id="check1",action=True, n_clicks=0),
            dbc.ListGroupItem("CHEKLIST TROCA DE TURNO",id="check2",action=True,n_clicks=0)])],
            title="CHECKLIST DIÁRIO"),
        dbc.AccordionItem([dbc.ListGroup([
            dbc.ListGroupItem("PARTIDA APÓS PARADA DE EMERGÊNCIA",id="check3",action=True,n_clicks=0),
            dbc.ListGroupItem("PARTIDA APÓS PARADA POR ENTUPIMENTO VÁLVULA X",id="check4",action=True,n_clicks=0),
            dbc.ListGroupItem("PARTIDA APÓS QUEDA DE ENERGIA",id="check5",action=True,n_clicks=0),
            ])],
            title="CHECKLIST SINISTROS"),
        dbc.AccordionItem([dbc.ListGroup([
            dbc.ListGroupItem("PARTIDA APÓS PARADA PROGRAMADA",id="check6",action=True,n_clicks=0),
            dbc.ListGroupItem("PARTIDA APÓS TROCA DE ROLAMENTO DO REDUTOR",id="check7",action=True,n_clicks=0),
            ])],
            title="CHECKLIST PREVENTIVA"),
        dbc.AccordionItem([dbc.ListGroup([
            dbc.ListGroupItem("CHECKLIST 120H",id="check8",action=True,n_clicks=0),
            dbc.ListGroupItem("CHECKLIST 720H",id="check9",action=True,n_clicks=0),
            dbc.ListGroupItem("CHECKLIST 6 MESES",id="check10",action=True,n_clicks=0),
            dbc.ListGroupItem("CHECKLIST 12 MESES",id="check11",action=True,n_clicks=0),            
            ])],
            title="CHECKLIST PREDITIVA"),
        dbc.AccordionItem([dbc.ListGroup([
            dbc.ListGroupItem("MANUAL MOTOREDUTOR WEG 10HP",id="check12",action=True,n_clicks=0),
            dbc.ListGroupItem("MANUAL MOTOR WEG 20HP",id="check13",action=True,n_clicks=0),
            dbc.ListGroupItem("MANUAL GERADOR NEMA 800Kva ",id="check14",action=True,n_clicks=0),           
            ])],
            title="MANUAIS"),                                
    ],start_collapsed=True,)

])

relatorios_layout = html.Div([
    dbc.Tabs([
        dbc.Tab(tab1_layout,label="Relatórios",),
        dbc.Tab(tab2_layout,label="Upload Documentos"),
    ])
])

chat_layout = html.Div([

])

gaugue_figure = go.Figure(go.Indicator(
    mode = "gauge+number",
    value = 0,
    title = {'text':"Motor A - RPM"},
    domain = {'x':[0,1],'y':[0,1]},
    gauge={
        'bar':{'color':'midnightblue'},
        'axis':{'range':[None,1500]},
        'steps':[{'range':[0,800],'color':"red"},
        {'range':[800,1000],'color':'#ffd700'},
        {'range':[1000,1100],'color':"green"},
        {'range':[1100,1300],'color':'#ffd700'},
        {'range':[1300,1500],'color':"red"}]}
        ))

gaugue_layout = html.Div([
        dcc.Graph(
            id="rpm-gauge",
            figure=gaugue_figure,
            animate=True
        ),
        dcc.Interval(
            id="rpm-gauge-update",
            interval=int(GRAPH_INTERVAL),
            n_intervals=5000,
        )
])

raw_layout = dbc.Container([
    dbc.Row([indicadores_layout]),
    dbc.Row([
        dbc.Col((gaugue_layout),class_name="shadow p-3 mb-5 bg-white rounded border border-light border rounded-3"),
        dbc.Col((checklist_layout),class_name="shadow p-3 mb-5 bg-white rounded border border-light border rounded-3"),
        dbc.Col((relatorios_layout),class_name="shadow p-3 mb-5 bg-white rounded border border-light border rounded-3 overflow-hidden p-3 mb-3 me-sm-3 "),
        dbc.Col((chat_layout),class_name="shadow p-3 mb-5 bg-white rounded border border-light border rounded-3")
    ]),
    html.Div(checklist_modal_layout)
],fluid=True)

layout = raw_layout

@callback(Output("rpm-gauge","figure"), [Input("rpm-gauge-update","n_intervals")])
def update_rpm_gauge (interval):

    X = rnd.randrange(999,1101,1)
    traces = gaugue_figure.update_traces(value=X,selector=dict(type='indicator'))

    now = dt.datetime.now()
    now_str = now.strftime("%d-%m-%Y %H:%M:%S")

    if X <= 1005 or X >= 1090:
        data = {"Velocidade":X,"Turno":"A","Operador":"Eduardo"}
        from pages.db import Setup
        #Setup.db.child("Logs").child("Máquina 1").child("LogVelocidade").child(now_str).set(data)               
 
    return traces
    
def parse_contents(contents,filename,date):
    content_type,content_string = contents.split(',')
    decoded = base64.b64decode(content_string)

    try:
        if "csv" in filename:
            df = pd.read_csv(io.StringIO(decoded.decode("utf-8")))
        elif "xls" in filename:
            df = pd.read_excel(io.BytesIO(decoded))
    except Exception as e:
        print(e)
        return html.Div(["Permitido apenas .xls ou .csv"])
    
    return html.Div([
        html.H5(filename),
        html.H6(datetime.datetime.fromtimestamp(date)),

        dash_table.DataTable(
            df.to_dict("records"),
            [{"name":i, "id":i} for i in df.columns]
        ),
        html.Hr(),
        html.Div("Conteúdo"),
        html.Pre(contents[0:200]+ "...", style={
            "whiteSpace":"pre-wrap",
            "wordBreak":"break-all"
        })
    ])

@callback(Output('output-data-upload', 'children'),
              Input('upload-data', 'contents'),
              State('upload-data', 'filename'),
              State('upload-data', 'last_modified'))
def update_output(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        children = [
            parse_contents(c, n, d) for c, n, d in
            zip(list_of_contents, list_of_names, list_of_dates)]
        return children

@callback(
    Output("modal-fs", "is_open"),
    Input("check1", "n_clicks"),
    Input("check12", "n_clicks"),
    State("modal-fs", "is_open"),
)
def toggle_modal(check1,check12, is_open):
    btn_id = ctx.triggered_id if not None else 'Sem clicks'

    if ctx.triggered_id == "check1" or ctx.triggered_id == "check12":
        return is_open,

@callback(Output("modal-body","children"),
[Input("check1", "n_clicks"),
Input("check12", "n_clicks")])
def modal_content(check1,check12):  

    if ctx.triggered_id == "check1":
        body = html.Iframe(src="/assets/check1.pdf",height="100%",width="100%")
        return body

    if ctx.triggered_id == "check12":
        body = html.Iframe(src="/assets/weg.pdf",height="100%",width="100%")
        return body        


