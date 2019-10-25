import pandas as pd
import numpy as np
import dash
import dash_core_components as dcc
import dash_html_components as html
import data_processing as dp
import plotly.graph_objs as go

# CSS 
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

chart1_df = dp.gen_chart_1()
colors = list(np.random.choice(range(256), size=chart1_df.shape[0]))
trace1 = {
    'labels': chart1_df["Industry"].values.tolist(),
    'values': chart1_df["Percentage"].values.tolist(),
    'marker': colors,
    'type': 'pie'
}
layout1 = {
    "title":'Population distribution across each industry'
}

chart4_df = dp.gen_chart_4(["Business", "Engineering", "Finance"]).T
trace2 = {
    'x': chart4_df["Business"].values.tolist(),
    'y': chart4_df.index.values.tolist(),
    'type': 'bar',
    'orientation':'h'
}
layout2 = {
    "title":'Movement of people moving across to other industries',
    'yaxis_tickangle': -45,
    'hovermode':'closest',
    'barmode': 'group'
}

# ----------------------------------------------------------------------------------------
"""
package all components into a dictionary

:keys: data, layout
:values: chart specs in dict format, 
         figure layout in dict format
"""
pie_1_fig = {'data':[trace1], 'layout':layout1}
data2 = [{
    'x': chart4_df[industry].values.tolist(),
    'y': chart4_df.index.values.tolist(),
    'type': 'bar',
    'name': industry,
    'orientation':'h'} for industry in chart4_df.columns]
stacked_bar_4_fig = {'data':data2, 'layout':layout2}

# ----------------------------------------------------------------------------------------
app = dash.Dash(external_stylesheets=external_stylesheets)
app.config.suppress_callback_exceptions = True

app.layout = html.Div(children=[
    html.H1(children='Workforce Health Analytics Dashboard', style={'textAlign': 'center'}),
    html.Div([
        html.Div([
            dcc.Graph(
                id='pie1',
                figure=pie_1_fig
                )
            ], className="six columns"),
            html.Div([
                dcc.Graph(
                    id='stacked_bar4',
                    figure=stacked_bar_4_fig
                    )
                ], className="six columns")
            ], className="row")
])

if __name__ == '__main__':
    app.run_server(debug=True)