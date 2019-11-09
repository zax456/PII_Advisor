import pandas as pd
import numpy as np
import random
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import data_processing as dp
import plotly.graph_objs as go

# CSS 
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

"""
Generate all chart dataframes, and create data structure (data and layout) to fit into Dash chart's parameters
"""
## Chart 1
chart1_df = dp.gen_chart_1()
colors_chart1 = list(np.random.choice(range(256), size=chart1_df.shape[0]))
trace1 = {
    'labels': chart1_df["Industry"].values.tolist(),
    'values': chart1_df["Percentage"].values.tolist(),
    'marker': colors_chart1,
    'type': 'pie'
}
layout1 = {
    "title":'Population distribution <br>across each industry',
    'showlegend': False
    # 'legend': {'font': {'size':5}}
}

## Chart 2
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

## Chart 3
chart3_df = dp.gen_chart_3()
colors_3 = dp.color_generator(n=chart3_df.shape[0])

## set X and Y values
data3 = [{
    'x': chart3_df.index.tolist(),
    'y': chart3_df["count"].tolist(),
    'type': 'bar',
    'name': chart3_df.index.tolist(),
    'marker': dict(
        color=colors_3,
        line=dict(color='rgb(248, 248, 249)', width=1)
        ),
    'hovertext': chart3_df["count"].tolist(),
    'hoverinfo': "text" 
}]

## set layout params
layout3 = {
    "title":'Distribution of the top 10 skills in the population',
    'yaxis':{'automargin':True},
    'xaxis':{'tickfont':{
        'size': 17
    }},
    'hovermode':'closest',
}

## Chart 6
chart6_df = dp.gen_chart_6(["IT", "Business"])
colors_6 = dp.color_generator(n=chart6_df.shape[0])

y_data_6 = chart6_df.columns.tolist()
x_data_6 = chart6_df.values.T
indices_6 = chart6_df.index.tolist()

hovertext_6 = []
## to get hover information
for i in range(len(x_data_6)):
    tmp = []
    for j in range(len(x_data_6[0])):
        txt = "{} years: {}%".format(indices_6[j], x_data_6[i][j])
        tmp.append((indices_6[j], txt))
    hovertext_6.append(tmp)

data6 = []
tracker = []
## to get X and Y values
for i in range(len(x_data_6[0])):
    for years, ind, hover in zip(x_data_6, y_data_6, hovertext_6):
        if hover[i][0] in tracker:
            data6.append({
                'x': [years[i]],
                'y': [ind],
                'type': 'bar',
                'orientation':'h',
                'marker':dict(
                    color=colors_6[i],
                    line=dict(color='rgb(248, 248, 249)', width=1)
                    ),
                'hovertext': [hover[i][1]],
                'hoverinfo': "text",
                'showlegend': False 
            })
        else:
            tracker.append(hover[i][0])
            data6.append({
                'x': [years[i]],
                'y': [ind],
                'type': 'bar',
                'orientation':'h',
                'name':"{} years".format(hover[i][0]),
                'marker':dict(
                    color=colors_6[i],
                    line=dict(color='rgb(248, 248, 249)', width=1)
                    ),
                'hovertext': [hover[i][1]],
                'hoverinfo': "text" 
            })

## set the layout params
layout6 = {
    "title":'Distribution of experiences in industry',
    'yaxis':{'automargin':True, 
    'tickfont':{
        'size': 14
    }},
    'xaxis':{'visible':False},
    'hovermode':'closest',
    'barmode': 'stack'
}

## Chart 7
chart7_df = dp.gen_chart_7(["Admin", "Business", "Engineering"])
colors_7 = dp.color_generator(n=chart7_df.shape[0])
y_data_7 = chart7_df.columns.tolist()
x_data_7 = chart7_df.values.T
indices_7 = chart7_df.index.tolist()

hovertext_7 = []
## to get hover information
for i in range(len(x_data_7)):
    tmp = []
    for j in range(len(x_data_7[0])):
        txt = "{} years: {}%".format(indices_7[j], x_data_7[i][j])
        tmp.append((indices_7[j], txt))
    hovertext_7.append(tmp)

data7 = []
tracker = []
## to get X and Y values
for i in range(len(x_data_7[0])):
    for duration, ind, hover in zip(x_data_7, y_data_7, hovertext_7):
        if hover[i][0] in tracker:
            data7.append({
                'x': [duration[i]],
                'y': [ind],
                'type': 'bar',
                'orientation':'h',
                'marker':dict(
                    color=colors_7[i],
                    line=dict(color='rgb(248, 248, 249)', width=1)
                    ),
                'hovertext': [hover[i][1]],
                'hoverinfo': "text",
                'showlegend': False 
            })
        else:
            tracker.append(hover[i][0])
            data7.append({
                'x': [duration[i]],
                'y': [ind],
                'type': 'bar',
                'orientation':'h',
                'name': "{} years".format(hover[i][0]),
                'marker':dict(
                    color=colors_7[i],
                    line=dict(color='rgb(248, 248, 249)', width=1)
                    ),
                'hovertext': [hover[i][1]],
                'hoverinfo': "text" 
            })            

## set the layout params
layout7 = {
    "title":'Average job duration in each industry',
    'xaxis':{'visible':False,},
    'yaxis':{'automargin':True, 
    'tickfont':{
        'size': 14
    }},
    'hovermode':'closest',
    'barmode': 'stack'
}

## Chart 5
chart5_df = dp.gen_chart_5(["IT", "Business"])
colors_5 = dp.color_generator(chart5_df.shape[0])

## set X and Y values
data5 = []
tracker = []
x_data_5 = chart5_df.columns.tolist()
y_data_5 = chart5_df.T.values
for h in range(len(y_data_5[0])):
    for industry, skills in zip(x_data_5, y_data_5):
        if chart5_df.index.tolist()[h] in tracker:
            tmp = {
                'x': [industry],
                'y': [skills[h]],
                'type': 'bar',
                'name': chart5_df.index.tolist()[h],
                'marker': {
                    'color':colors_5[h],
                    'line':dict(color='rgb(248, 248, 249)', width=1)
                },
                'hovertext': [chart5_df.index.tolist()[h] + ":" + str(skills[h])[:-1]],
                'hoverinfo': "text",
                'showlegend': False
            }
        else:
            tracker.append(chart5_df.index.tolist()[h])
            tmp = {
                'x': [industry],
                'y': [skills[h]],
                'type': 'bar',
                'name': chart5_df.index.tolist()[h],
                'marker': {
                    'color':colors_5[h],
                    'line':dict(color='rgb(248, 248, 249)', width=1)
                },
                'hovertext': [chart5_df.index.tolist()[h] + ":" + str(skills[h])[:-1]],
                'hoverinfo': "text"
            }
        data5.append(tmp)

## set layout params
layout5 = {
    'title': "Top 10 skills in industry",
    'barmode': 'group',
    'hovermode': 'closest',
    'xaxis': {'tickfont':{
        'size': 14
    }}
}
# ----------------------------------------------------------------------------------------
"""
package all components into a dictionary

:keys: data, layout
:values: chart specs in dict format, 
         figure layout in dict format
"""
## Chart 1
pie_1_fig = {'data':[trace1], 'layout':layout1}

## Chart 2
donut_2_fig = {'data':[trace2], 'layout':layout2}

## Chart 3
bar_3_fig = {'data':data3, 'layout':layout3}

## Chart 5
bar5_fig = {'data':data5, 'layout':layout5}

## Chart 6
stack_bar_6_fig = {'data':data6, 'layout':layout6}

## Chart 7
stack_bar_7_fig = {'data':data7, 'layout':layout7}
# ----------------------------------------------------------------------------------------
app = dash.Dash(external_stylesheets=external_stylesheets)
app.config.suppress_callback_exceptions = True

app.layout = html.Div(children=[
    html.H1(children='Workforce Health Analytics Dashboard', style={'textAlign': 'center'}),
    html.Div([
        html.Div([
            dcc.Dropdown(
                id='main-filter',
                options=[
                    {'label': ind, 'value': ind} for ind in dp.get_df()['industry'].unique()
                ],
                value=[],
                multi=True
            )
        ])

    ], className="row"), 

    html.Div([
        html.Div([
            dcc.Graph(
                id='stacked_bar4',
                figure={}
                )
                ], className="six columns"),

        html.Div([
            dcc.Graph(
                id='stacked_bar5',
                figure=bar5_fig
                )], className="six columns")

    ], className="row"),

    html.Div([
        html.Div([
            dcc.Graph(
                id='stacked_bar6',
                figure=stack_bar_6_fig
                )
                ], className="six columns"), 

        html.Div([
            dcc.Graph(
                id='stacked_bar7',
                figure=stack_bar_7_fig
                )
                ], className="six columns")

    ], className="row"),

    html.Div([        
        html.Div([
            dcc.Graph(
                id='pie1',
                figure=pie_1_fig
                )
            ], className="four columns"),

        html.Div([
            dcc.Graph(
                id='donut2',
                figure=donut_2_fig
                )
            ], className="four columns"),

        html.Div([
            dcc.Graph(
                id='bar3',
                figure=bar_3_fig
                )
            ], className="four columns")

        ], className="row")
        
], className="container")

# ---------------------------------------------------------------------------------------------------------
## CALLBACKS

@app.callback(
    Output(component_id='stacked_bar4', component_property='figure'),
    [Input(component_id='main-filter', component_property='value')]
)
def get_selected_ind(selected_inds):
    if selected_inds == []:
        selected_inds = dp.get_top_n(10)
    chart4_df = dp.gen_chart_4(selected_inds)
    data4 = [{
        'x': chart4_df[industry].values.tolist(),
        'y': chart4_df.index.values.tolist(),
        'type': 'bar',
        'name': industry,
        'orientation':'h'
    } for industry in chart4_df.columns]
    layout4 = {
        "title":'Movement of people moving across to other industries',
        'yaxis':{'tickangle': -35},
        'hovermode':'closest',
        'barmode': 'group',
        "width": 500
    }
    return {
        'data':data4,
        'layout':layout4
    }


if __name__ == '__main__':
    app.run_server(debug=True)