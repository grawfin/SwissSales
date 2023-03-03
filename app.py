import chart_studio
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

chart_studio.tools.set_credentials_file(username='griffin123', api_key='XLkOUTSmAhXbMImJGRd2')
mapbox_access_token = 'pk.eyJ1IjoiZ3JpZmZpbjEyMyIsImEiOiJjazV2YnFndHIwYmliM2ptZGNiMGpxbDE1In0._iZvbdWb--5eNSF7Q3sI9g'

n = 100  # every 100th line = 1% of the lines
# df = pd.read_csv(filename, header=0, skiprows=lambda i: i % n != 0)
buildings = pd.read_csv("./sample2.csv",on_bad_lines='skip').fillna(0)

print(buildings)

fig = go.Figure()

fig.add_trace(
    go.Scattermapbox(
        lat = buildings['long'],
        lon = buildings['lat'],
        mode="markers",
        marker=go.scattermapbox.Marker(
            size=[max(x*2, 5) for x in list(buildings['GANZWHG'])],
            color=buildings['GKSCE']
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
    plot_bgcolor="#282b38", paper_bgcolor="#282b38"
)

app = dash.Dash(external_stylesheets=[dbc.themes.CYBORG])

app.layout = dbc.Row([
    dbc.Col(
        [
            html.Br(),
            html.H1('Swiss Sales Dashboard'),
            html.Br(),

        ],
        style={'textAlign': 'center',},
        width=3,
        className="bg-secondary"
    ),
    dbc.Col(
        dcc.Graph(figure=fig,
            style={"height":"90vh", "width":"70vw", "bg-color":"primary",}
        ),
        width=9,
        className="bg-secondary"
    )
],className="bg-primary")

if __name__ == '__main__':
    app.run_server(debug=True)
