import pandas as pd
import numpy as np
import dash
import dash_core_components as dcc
import dash_html_components as html
import data_processing as dp
import plotly.graph_objs as go

# CSS 
external_stylesheets = ['https://codepen.io/tony-tong-the-selector/pen/GRRONpE?editors=0100.css']

chart1_df = dp.gen_chart_1()
colors_chart1 = list(np.random.choice(range(256), size=chart1_df.shape[0]))
trace1 = {
    'labels': chart1_df["Industry"].values.tolist(), # x is label
    'values': chart1_df["Percentage"].values.tolist(), # y is value
    'marker': colors_chart1,
    'type': 'pie'
}
layout1 = {
    "title":'Population distribution <br>across each industry',
    'showlegend': False
    # 'legend': {'font': {'size':5}}
}

chart2_df = dp.gen_chart_2()
colors_chart2 = list(np.random.choice(range(256), size=chart2_df.shape[0]))
trace2 = {
    'labels': chart2_df.index.tolist(),
    'values': chart2_df["percentage"].values.tolist(),
    'marker': colors_chart2,
    'type': 'pie',
    'hole': 0.3
}
layout2 = {
    "title": {
        'text': 'Population Experience distribution <br>across each industry'
        # 'font': {'size': 14}
        },
    'showlegend': False
    # 'legend': {'font': {'size':10}}
}

trace3 = {
    'labels': chart1_df["Industry"].values.tolist(),
    'values': chart1_df["Percentage"].values.tolist(),
    'marker': colors_chart1,
    'type': 'pie'
}
layout3 = {
    "title":'Population distribution <br>across each industry',
    'showlegend': False
    # 'legend': {'font': {'size':5}}
}

chart4_df = dp.gen_chart_4(["Business", "Engineering", "Finance"])
trace4 = {
    'x': chart4_df.loc["Business",].values.tolist(),
    'y': chart4_df.index.values.tolist(),
    'type': 'bar',
    'orientation':'h'
}
layout4 = {
    "title":'Movement of people moving across to other industries',
    'tickangle': -45,
    'hovermode':'closest',
    'barmode': 'group',
    "width": 500
}

# ----------------------------------------------------------------------------------------
"""
package all components into a dictionary

:keys: data, layout
:values: chart specs in dict format, 
         figure layout in dict format
"""
pie_1_fig = {'data':[trace1], 'layout':layout1}

donut_2_fig = {'data':[trace2], 'layout':layout2}

pie_3_fig = {'data':[trace1], 'layout':layout1}

data4 = [{
    'x': chart4_df[industry].values.tolist(),
    'y': chart4_df.index.values.tolist(),
    'type': 'bar',
    'name': industry,
    'orientation':'h'} for industry in chart4_df.columns]
stacked_bar_4_fig = {'data':data4, 'layout':layout4}

# ----------------------------------------------------------------------------------------

#############################################
# STYLES
#############################################

shadow = {'border-radius': '4px',
  'box-shadow': '#d3d3d3 5px 5px 5px',
  'padding': '0px'}

#############################################

app = dash.Dash(external_stylesheets=external_stylesheets)
app.config.suppress_callback_exceptions = True

app.layout = html.Div(children=[
    html.H1(children='Workforce Health Analytics', className="header"),
    html.H3(children='Interactive Dashboard', className="subHeader"),
    # 1st layer of charts
    html.Div([
        html.Div([
            dcc.Graph(
                id='pie1',
                figure=pie_1_fig
                )
            ], className="four columns", style=shadow),

    html.Div([
            dcc.Graph(
                id='donut2',
                figure=donut_2_fig
                ), 
            ], className="four columns", style=shadow),

    html.Div([
            dcc.Graph(
                id='pie3',
                figure=pie_3_fig
                )
            ], className="four columns", style=shadow)

        ], className="row", style={'margin-bottom': '2%'}),
    
    # 2nd layer of charts
    html.Div([
        html.Div([
            dcc.Graph(
                id='stacked_bar4',
                figure=stacked_bar_4_fig
                )
                ], className="seven columns", style=shadow),
        html.Div([
            dcc.Graph(
                id='stacked_bar5',
                figure=stacked_bar_4_fig
                )
                ], className="seven columns", style=shadow)
    ], className="row", style={'margin-bottom': '2%'}),

    # 3nd layer of charts
    html.Div([
        html.Div([
            dcc.Graph(
                id='pie10',
                figure=pie_1_fig
                )
            ], className="four columns", style=shadow),

    html.Div([
            dcc.Graph(
                id='donut20',
                figure=donut_2_fig
                ), 
            ], className="four columns", style=shadow),

    html.Div([
            dcc.Graph(
                id='pie30',
                figure=pie_3_fig
                )
            ], className="four columns", style=shadow)

        ], className="row", style={'margin-bottom': '3%'})

], className="container")


if __name__ == '__main__':
    app.run_server(debug=True)