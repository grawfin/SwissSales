import chart_studio
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash import callback_context
import dash_daq as daq

chart_studio.tools.set_credentials_file(username='griffin123', api_key='XLkOUTSmAhXbMImJGRd2')
mapbox_access_token = 'pk.eyJ1IjoiZ3JpZmZpbjEyMyIsImEiOiJjazV2YnFndHIwYmliM2ptZGNiMGpxbDE1In0._iZvbdWb--5eNSF7Q3sI9g'

n = 100  # every 100th line = 1% of the lines
# df = pd.read_csv(filename, header=0, skiprows=lambda i: i % n != 0)
buildings = pd.read_csv("../sample2.csv",on_bad_lines='skip')
DATE = "GWAERDATH1"
buildings[DATE] = buildings[DATE].fillna(method="bfill")
buildings = buildings.fillna(0)
buildings['YEAR'] = [str(str(i)[:4]) for i in list(buildings[DATE])]
years = list(buildings['YEAR'].unique())
colors = ["#7FB290", "#83DBEE", "#D67445","#90f5d3","#dd90f5","#fc425e", "#faf06b", "#629bfc", "#3C799D", "green", "brown", "yellow"]
names = ["Product " + str(int(i+1)) for i in range(10)]

mapping = {list(buildings['GKSCE'].unique())[i]:colors[i] for i in range(len(list(buildings['GKSCE'].unique())))}
mapping2= {list(buildings['GKSCE'].unique())[i]:names[i] for i in range(len(list(buildings['GKSCE'].unique())))}
buildings['PRODUCT'] = [mapping2[elt] for elt in list(buildings['GKSCE'])]

fig3 = go.Figure()
pie = go.Figure()
fig4 = go.Figure()
mu=0
sigma=20
iyrs = range(2000, 2022, 1)
print(iyrs)
xs1 = []
ys1 = []

for elt in list(buildings['GDEKT'].unique()):

    xs = []
    ys = []

    for yr in iyrs:
        if int(yr) > 2003:
            tmp = buildings[(buildings['GDEKT'] == elt) & (buildings['YEAR'] == str(yr))]
            ys.append(sum(list(tmp['GANZWHG'])))
            xs.append(int(yr))

        else:
            continue
    fig4.add_trace(
            go.Scatter(
                y=ys,
                x=xs,
                name=elt,
                marker={
                    # "color":colors[e],
                }
            )
        )
e = -1

txs = []
tys = []

for elt in list(buildings['PRODUCT'].unique()):
    e += 1
    xs = []
    ys = []
    tmp1 = buildings[buildings['PRODUCT'] == elt]
    tys.append(elt)
    txs.append(sum(list(tmp1['GANZWHG'])))
    for yr in years:
        if int(yr) > 2003:
            tmp = buildings[(buildings['PRODUCT'] == elt) & (buildings['YEAR'] == yr)]
            xs.append(sum(list(tmp['GANZWHG'])))
            ys.append(int(yr))

        else:
            continue
    fig3.add_trace(
            go.Bar(
                y=ys,
                x=xs,
                name=elt,
                orientation="h",
                marker={
                    "color":colors[e],
                }
            )
        )
fig3.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    margin=dict(l=0, r=0, t=35, b=0),
    font_family="Paytone One",
    font_color="#3C799D",
    title="Number of Yearly Sales",
    font_size=16,
    height=300
)
fig4.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    margin=dict(l=0, r=0, t=50, b=0),
    font_family="Paytone One",
    font_color="#3C799D",
    title="Yearly Sales by Canton",
    font_size=16,
    height=300
)
pie.add_trace(
    go.Pie(
        labels=tys,
        values=txs,
        name="Total Distribution of Sales",
        marker_colors=colors
    )
)
pie.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    showlegend=False,
    margin=dict(l=0, r=0, t=35, b=0),
    font_family="Paytone One",
    font_color="#3C799D",
    title="Distribution of Yearly Sales",
    font_size=16,
    height=300
)
fig3.update_layout(barmode='stack')

fig = go.Figure()

fig.add_trace(
    go.Scattermapbox(
        lat = buildings['long'],
        lon = buildings['lat'],
        mode="markers",
        text=[mapping2[elt] for elt in list(buildings['GKSCE'])],
        marker=go.scattermapbox.Marker(
            size=[max(x*2, 5) for x in list(buildings['GANZWHG'])],
            color=[mapping[elt] for elt in list(buildings['GKSCE'])],

        )
    )
)

fig.update_layout(
    hovermode='closest',
    mapbox=go.layout.Mapbox(
        accesstoken=mapbox_access_token,
        bearing=0,
        style="mapbox://styles/griffin123/clesip64o00jn01lk5bl0fqku",
        center=go.layout.mapbox.Center(
            lat=46.849110,
            lon=8.392482
        ),
        pitch=0,
        zoom=7.8,
    ),
    plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)"
)
#
# fig2 = go.Figure()

fig.update_layout(
    margin=dict(l=0, r=0, t=0, b=0),
)

app = dash.Dash(
        external_stylesheets=[
            dbc.themes.CYBORG,
            dbc.icons.FONT_AWESOME,
            'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css',
            "https://fonts.googleapis.com/css2?family=Paytone+One&display=swap"
        ]
    )

pcard = dbc.Card(
    [
        dbc.Row(
            [
                dbc.Col(
                    dbc.CardImg(
                        src="/assets/mugshot-modified.png",
                        className="img-fluid rounded-start",
                    ),
                    className="col-md-4",
                    style={"margin-left":"1vw","height":"4vh","width":"4vw"}
                ),
                dbc.Col(
                    dbc.CardBody(
                        [
                            html.H5("Welcome, GW", className="card-title",style={"color":"white"}),
                            html.P(
                                "This is a sample dashboard using static data. It can be easily modified to fit your use case!",
                                className="card-text",
                                style={
                                    "font-size":"14px"
                                }
                            ),
                            html.Small(
                                "Last login 3 mins ago",
                                className="card-text text-muted",
                            ),
                        ]
                    ),
                    className="col-md-8",
                ),
            ],
            className="g-0 d-flex align-items-center",
        )
    ],
    className="mb-3",
    style={
        "maxWidth": "540px",
        "margin-right":"1vw",
        "margin-left":"1vw",
        "margin-top":"6vh",
        "background-color":"#2B323D",
        "font-family":"'Paytone One'",
        "color":"#3C799D",
        "border-weight":"1px",
        "border-color":"white"
    },
)

app.layout = html.Div([
    dbc.Row([
        html.H3("Your Company Name",
            style={
                "font-size":"4vh",
                "font-family":"'Paytone One'",
                "color":"#3C799D",
                "margin-top":"2vh",
                "margin-left":"20vw",
                "margin-bottom":"2vh",
            }
        ),
    ],
    style={
        "background-color":"#1C2026",'box-shadow':'6px 6px 6px grey',"width":"100vw"
    }),
    dbc.Row([
        dbc.Col(
            dbc.Card(
                [
                    html.Br(),
                    html.H2(
                        'Swiss Sales Dashboard',
                        style={
                            'font-size':'32px',
                            'font-family':"'Paytone One'",
                            'font-weight':'bold',
                            "margin-top":"6vh",
                            "color":"#3C799D"
                        }
                    ),
                    pcard,
                    html.Br(),
                    dbc.Button(
                        id="map",
                        children=[
                            html.I(className="fa fa-map-pin"),
                            " Sales Map"
                        ],
                        color="rgba(0,0,0,0)",
                        style={
                            "color":"#3C799D",
                            "height":"8vh",
                            "font-size":"24px",
                            "margin-top":"7vh",
                            'font-family':"'Paytone One'"
                        }
                    ),
                    dbc.Button(
                        id="chart",
                        children=[
                            html.I(className="fa fa-line-chart"),
                            "   Sales Statistics"
                        ],
                        color="rgba(0,0,0,0)",
                        style={
                            "color":"#3C799D",
                            "font-size":"24px",
                            "height":"10vh",
                            'font-family':"'Paytone One'"
                        }
                    ),
                    # dbc.Button(id="report",children=[html.I(className="fa fa-file-text"),"  Generate Report"], color="rgba(0,0,0,0)",style={"color":"#3C799D", "font-size":"24px","height":"10vh",'font-family':"'Paytone One'"}),
                    # dbc.Button(id="report",children=["Logout"], color="rgba(0,0,0,0)",style={"color":"red", "font-size":"24px","height":"10vh",'font-family':"'Paytone One'", "border":"3px"}),
                    dbc.Button(
                        id="report",
                        children=["Logout"],
                        external_link=True,
                        href="https://www.gwcustom.com/copy-of-home",
                        color="rgba(0,0,0,0)",
                        style={
                            "color":"red",
                            "font-size":"24px",
                            "height":"10vh",
                            'font-family':"'Paytone One'",
                            "border":"3px"
                        }
                    ),
                    dbc.ButtonGroup(
                        [dbc.Button([html.I(className="fa fa-linkedin-square")],external_link=True, href="https://www.linkedin.com/in/griffin-#3C799D-3aa20918a/",target="_blank", color="rgba(0,0,0,0)",style={"color":"#3C799D","font-size":"28px"}),
                         dbc.Button([html.I(className="fa fa-google")],external_link=True, href="https://www.gwcustom.com/",target="_blank", color="rgba(0,0,0,0)",style={"color":"#3C799D","font-size":"28px"}),
                         dbc.Button([html.I(className="fa fa-github")],external_link=True, href="https://github.com/GriffinWhitePortfolio",target="_blank", color="rgba(0,0,0,0)",style={"color":"#3C799D","font-size":"28px"})],
                         style={"margin-left":"2vw", "margin-right":"2vw", "margin-top":"4vh"}
                    )
                    # html.Shadow(dcc.RangeSlider(2000, 2022, 2, value=[2000, 2021], id='years'))

                ],style={"height":"100vh",'background-color':'#1F2732', 'box-shadow':'6px 6px 6px grey',"position":"sticky"}
            ),
            style={'textAlign': 'center'},
            width=3
        ),
        dbc.Col(
            id="main-out",
            children=[
            dbc.Card([
                html.H1(
                    [
                        "Swiss Sales Map     ",
                        html.I(className="fa fa-info-circle")
                    ],
                    style={
                        'font-size':'26px',
                        "margin-left":"8vw",
                        "bg-color":"rgba(0,0,0,0)",
                        "color":"#3C799D"
                    }
                )],
                style={
                    "margin-top":"8vh",
                    "background-color":"rgba(0,0,0,0)",
                    'font-family':"'Paytone One'",
                    'font-weight':'bold'
                }
            ),
            dbc.Card(
                id="main-graph",
                children=[
                    dcc.Graph(figure=fig,
                        style={
                            "height":"75vh",
                            "width":"70vw",
                            "bg-color":"rgba(0,0,0,0)",
                            'box-shadow':'6px 6px 6px grey'
                        }
                    )
                ],
            style={
                "background-color":'rgba(0,0,0,0)',
                "margin-top":"2vh",
                "margin-left":"2vw",
                "border-radius":"30px"
                }
            )],
            width=9,
            style={}
        )
    ])
# ],style={'background-image':'url(/assets/bg.jpg)','height':'100vh', 'width':'100vw'})
],style={'background-color':'#2B323D','height':'110vh', 'width':'100vw'})



@app.callback(
    Output("main-out","children"),
    [Input("map","n_clicks"),
     Input("chart","n_clicks"),
     Input("report","n_clicks"),
     Input("main-out","children")])
def main_out(map, chart, report, current):

    trigger = callback_context.triggered[0]['prop_id']
    print(trigger)

    if trigger == "map.n_clicks":
        send = [
        dbc.Card(
            [html.H1([
                "Swiss Sales Map     ",
                html.I(className="fa fa-info-circle")],
                style={
                    'font-size':'26px',
                    "margin-left":"8vw",
                    "bg-color":"rgba(0,0,0,0)",
                    "color":"#3C799D"
                }
            )],
            style={
                "margin-top":"8vh",
                "background-color":"rgba(0,0,0,0)",
                'font-family':"'Paytone One'",
                'font-weight':'bold'
            }
        ),
        dbc.Card(
            id="main-graph",
            children=[
                dcc.Graph(figure=fig,
                    style={
                        "height":"75vh",
                        "width":"70vw",
                        "bg-color":"rgba(0,0,0,0)",
                        'box-shadow':'6px 6px 6px grey'
                    }
                )
            ],
        style={
            "background-color":'rgba(0,0,0,0)',
            "margin-top":"2vh",
            "margin-left":"2vw",
            "border-radius":"30px"
            }
        )]
    elif trigger == "chart.n_clicks":
        send = [
            dbc.Card(
                [
                    html.H1(
                        [
                            "Swiss Sales Statistics     ",
                            html.I(className="fa fa-info-circle")
                        ],
                        style={
                            'font-size':'26px',
                            "margin-left":"8vw",
                            "bg-color":"rgba(0,0,0,0)",
                            "color":"#3C799D"
                        }
                    )
                ],
                style={
                    "margin-top":"8vh",
                    "background-color":"rgba(0,0,0,0)",
                    'font-family':"'Paytone One'",
                    'font-weight':'bold'
                }
            ),
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dcc.Graph(
                            figure=pie
                        )],
                        style={
                            'box-shadow':'6px 6px 6px grey',
                            'background-color':'#1C2026',
                            "font-family":"'Paytone One'",
                            "color":"#3C799D",
                            "border-radius":"20px",
                            "height":"36vh"
                        }
                    )
                ], width=4),
                dbc.Col([
                    dbc.Card([
                        dbc.Row([
                            dbc.Col([
                                daq.Gauge(
                                    color={"gradient":True,"ranges":{"red":[0,0.6],"yellow":[0.6,0.8],"green":[0.8,1]}},
                                    value=0.6,
                                    label={'label':'Sales to Inventory Ratio','style':{"font-size":"22px","margin-top":"1vh"}},
                                    max=1,
                                    min=0,
                                )
                            ],
                            width=9),
                            dbc.Col([
                                html.H1("0.6",
                                    style={
                                        "color":"yellow",
                                        "font-size":"32px",
                                        "margin-top":"10vh"
                                    }
                                )
                            ],
                            width=3)
                        ])
                    ],
                    style={
                        'box-shadow':'6px 6px 6px grey',
                        'background-color':'#1C2026',
                        "font-family":"'Paytone One'",
                        "color":"#3C799D",
                        "border-radius":"20px",
                        "height":"36vh"
                    }
                )], width=4),
                dbc.Col([
                    dbc.Card([
                        dbc.Row([
                            dbc.Col([
                                daq.Gauge(
                                    color={"gradient":True,"ranges":{"red":[0,0.6],"yellow":[0.6,0.8],"green":[0.8,1]}},
                                    value=0.864,
                                    label={'label':'Industry Percentile','style':{"font-size":"22px","margin-top":"1vh"}},
                                    max=1,
                                    min=0,
                                )
                            ],width=9),
                            dbc.Col([
                                html.H1("0.86",
                                    style={
                                        "color":"green",
                                        "font-size":"32px",
                                        "margin-top":"10vh"
                                    }
                                )
                            ],
                            width=3)
                        ])
                    ],
                    style={
                        'box-shadow':'6px 6px 6px grey',
                        'background-color':'#1C2026',
                        "font-family":"'Paytone One'",
                        "color":"#3C799D",
                        "border-radius":"20px",
                        "height":"36vh"
                    }
                )],
                width=4
                ),],
                style={
                    "margin-right":"4vw",
                    "margin-left":"4vw",
                    "margin-top":"6vh"
                }
            ),
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dcc.Graph(
                            figure=fig3
                        )],
                        style={
                            'box-shadow':'6px 6px 6px grey',
                            'background-color':'#1C2026',
                            "font-family":"'Paytone One'",
                            "color":"#3C799D",
                            "border-radius":"20px",
                            "margin-top":"3vh"
                        }
                    )], width=5
                ),
                dbc.Col([
                    dbc.Card([
                        dcc.Graph(
                            figure=fig4
                        )],
                        style={
                            'box-shadow':'6px 6px 6px grey',
                            'background-color':'#1C2026',
                            "font-family":"'Paytone One'",
                            "color":"#3C799D",
                            "border-radius":"20px",
                            "margin-top":"3vh"
                        }
                    )
                ],width=7)
            ],
            style={
                "margin-bottom":"20vh",
                "margin-right":"4vw",
                "margin-left":"4vw",
                "margin-top":"3vh"
            }
        )]
    # elif trigger == "report.n_clicks":
    #     # send = [dbc.Card([html.H1(["Swiss Sales Report Generation     ", html.I(className="fa fa-info-circle")], style={'font-size':'26px',"margin-left":"8vw", "bg-color":"rgba(0,0,0,0)"})],style={"margin-top":"8vh", "background-color":"rgba(0,0,0,0)",'font-family':"'Paytone One'", 'font-weight':'bold', "border-radius":"20px"}),]
    #     #3C799D
    else:
        send = current

    return send

if __name__ == '__main__':
    app.run_server(debug=True)
