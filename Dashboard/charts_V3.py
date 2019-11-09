import pandas as pd
import numpy as np
import random
from colour import Color
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import data_processing_V2 as dp
import plotly.graph_objs as go

# print(dp.polylinear_gradient(dp.rand_hex_color(3), 16))

"""
Generate all chart dataframes, and create data structure (data and layout) to fit into Dash chart's parameters
"""
## Chart 1
def get_chart_1_fig():
    chart1_df = dp.gen_chart_1()
    colors_1 = dp.rand_hex_color(num=chart1_df.shape[0])
    # dp.polylinear_gradient(dp.rand_hex_color(num=2), n=chart1_df.shape[0])

    trace1 = {
        'labels': chart1_df["Industry"].values.tolist(), # Y axis
        'values': chart1_df["Percentage"].values.tolist(), # X axis
        'marker': dict(
            colors=colors_1, 
            line=dict(color='#000000', width=2)
            ),
        'type': 'pie'
    }
    layout1 = {
        "title":'Population distribution <br>across each industry',
        'showlegend': False
        # 'legend': {'font': {'size':5}}
    }
    return {
        'data': [trace1],
        'layout': layout1
    }

## Chart 2
def get_chart_2_fig():
    chart2_df = dp.gen_chart_2()
    years_group = chart2_df.index.tolist()
    colors_2 = dp.rand_hex_color(num=chart2_df.shape[0])
    # dp.polylinear_gradient(dp.rand_hex_color(num=2), n=chart2_df.shape[0])
    trace2 = {
        'labels': years_group,                 # Y axis
        'values': chart2_df["percentage"].values.tolist(),  # X axis
        'marker':dict(
            colors=colors_2, 
            line=dict(color='#000000', width=2)
            ),
        'type': 'pie',
        'hole': 0.3,
        'sort': False,
        'name': [f'{group} years' for group in years_group]
    }
    layout2 = {
        "title": {
            'text': 'Population Experience distribution <br>across each industry'
            # 'font': {'size': 14}
            },
        'showlegend': True,
        'legend_orientation': 'h',
        # 'sort': True
        'legend': {
            'font': {'size':12},
            'x': 1,
            'y': 0.5,
            },
        'annotations': [
            dict(x=1.21, y=0.81, xref='paper', yref='paper', text='Years', 
            font=dict(size=14), showarrow=False)
            ]
    }
    return {
        'data': [trace2],
        'layout': layout2
    }

## Chart 3
def get_chart_3_fig():
    chart3_df = dp.gen_chart_3()
    colors_3 = dp.rand_hex_color(num=chart3_df.shape[0])

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
        'xaxis':{'tickangle': -45, 
                'tickfont':{
                    'size': 9.5
                    }
                },
        'hovermode':'closest',
        'plot_bgcolor': "#F4F4F4"
    }

    return {
        'data': data3,
        'layout': layout3
    }

## Chart 4
def get_chart_4_fig(selected_inds):
    chart4_df = dp.gen_chart_4(selected_inds)
    colors_4 = dp.rand_hex_color(num=chart4_df.shape[1], from_pcodes=True)

    data4 = []
    tracker = [] # see which columns has been added to chart
                 # to prevent duplicates in legend
    x_data_4 = chart4_df.values.T # previous industry data
    columns_data_4 = chart4_df.columns.tolist() # previous industries
    indices_4 = chart4_df.index.values.tolist() # current industries

    hovertext_4 = {}
    ## to get hover information
    for i in range(x_data_4.shape[0]):
        tmp = []
        for j in range(len(x_data_4[0])):
            txt = "{}% was from {}".format((x_data_4[i][j])*100, columns_data_4[i] )
            tmp.append(txt)
        hovertext_4[columns_data_4[i]] = tmp

    for i in range(len(columns_data_4)):
        if columns_data_4[i] in tracker:
            tmp = {
                'x': chart4_df.loc[:, columns_data_4[i]].tolist(),
                'y': indices_4,
                'type': 'bar',
                'orientation': 'h',
                'name': columns_data_4[i],
                'marker': {
                    'color': colors_4[i],
                    'line': dict(color='rgb(248, 248, 249)', width=1)
                },
                'hovertext': hovertext_4[columns_data_4[i]],
                'hoverinfo': "text",
                'showlegend': False
            }
        else:
            tracker.append(columns_data_4[i])
            tmp = {
                'x': chart4_df.loc[:, columns_data_4[i]].tolist(),
                'y': indices_4,
                'type': 'bar',
                'orientation': 'h',
                'name': columns_data_4[i],
                'marker': {
                    'color': colors_4[i],
                    'line': dict(color='rgb(248, 248, 249)', width=1)
                },
                'hovertext': hovertext_4[columns_data_4[i]],
                'hoverinfo': "text"
            }
        data4.append(tmp)

    layout4 = {
        "title":'Movement of people moving across to other industries',
        'yaxis':{'tickangle': 0, 
                 'tickfont':{
                     'size': 10
                    }
                },
        'hovermode':'closest',
        'barmode': 'group',
        'plot_bgcolor': "#F4F4F4",
        'margin':{'l':130}
    }
    return {
        'data':data4,
        'layout':layout4
    }

## Chart 5
def get_chart_5_fig(selected_inds):
    chart5_df = dp.gen_chart_5(selected_inds)
    # print(chart5_df.shape)
    # print(chart5_df['Engineering'])
    colors_5 = dp.rand_hex_color(num=chart5_df.shape[0], from_pcodes=True)

    ## set X and Y values
    data5 = []
    tracker = []
    x_data_5 = chart5_df.columns.tolist() # industries
    y_data_5 = chart5_df.T.values # rows=industries; cols=skills
    # print(len(x_data_5))
    # print(y_data_5.shape)
    all_skills = chart5_df.index.tolist()
    for industry, skills in zip(x_data_5, y_data_5):
        for h in range(len(y_data_5[0])): # num of skills
            if type(skills[h]) == str:
                tmp = {
                    'x': [industry],
                    'y': [skills[h]],
                    'type': 'bar',
                    'name': all_skills[h],
                    'marker': {
                        'color':colors_5[h],
                        'line':dict(color='rgb(248, 248, 249)', width=1)
                    },
                    'hovertext': [all_skills[h] + ":" + str(skills[h])[:-1]],
                    'hoverinfo': "text",
                    # 'showlegend': False
                }
                if all_skills[h] not in tracker:
                    tracker.append(all_skills[h])
                data5.append(tmp)

    ## set layout params
    layout5 = {
        'title': "Top 10 skills in industry",
        'barmode': 'group',
        'hovermode': 'closest',
        'xaxis': {'tickfont':{
            'size': 14
        }}, 
        'plot_bgcolor': "#F4F4F4"
    }

    return {
        'data': data5,
        'layout': layout5
    }

## Chart 6
def get_chart_6_fig(selected_inds):
    chart6_df = dp.gen_chart_6(selected_inds)
    start_color = Color("#FFEC8B") # lightgoldenrod1
    finish_color = Color("#8B814C") # lightgoldenrod4
    colors_6 = dp.linear_gradient(start_hex=start_color.hex_l, finish_hex=finish_color.hex_l, n = chart6_df.shape[0])

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
                    'showlegend': False,
                    'sort': False
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
                    'hoverinfo': "text",
                    'sort': False
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
        'barmode': 'stack',
        'plot_bgcolor': "#F4F4F4",
        'sort': False
    }

    return {
        'data': data6,
        'layout': layout6
    }

## Chart 7
def get_chart_7_fig(selected_inds):
    chart7_df = dp.gen_chart_7(selected_inds)
    y_data_7 = chart7_df.columns.tolist()
    x_data_7 = chart7_df.values.T

    indices_7 = chart7_df.index.tolist()
    start_color = Color("#7FFFD4") # aquamarine1
    finish_color = Color("#458B74") # aquamarine4
    colors_7 = dp.linear_gradient(
        start_hex=start_color.hex_l, 
        finish_hex=finish_color.hex_l, 
        # n = dp.gen_chart_6(selected_inds).shape[0]
        n = len(x_data_7[0])
        )

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
        'barmode': 'stack',
        'plot_bgcolor': "#F4F4F4"
    }

    return {
        'data': data7,
        'layout': layout7
    }

# ----------------------------------------------------------------------------------------
app = dash.Dash(__name__)
app.config.suppress_callback_exceptions = True

app.layout = html.Div(children=[
    ## Logo
    ## Headers
    html.Div([
        html.Img(height="100px", width="250px", src='assets/logo_govtech_hort.gif', className="top shadow"),
        html.Img(height="100px", width="250px", src='assets/mycareersfuture.JPG', className="shadow", style={'float':'right', 'margin-top': '1%', 'margin-right':'2%'}),
        html.H1(children=['Workforce Health Analytics'], className="header"),
        html.H3(children='Interactive Dashboard', className="subHeader")
    ], className="top"),

    ## Filter bar
    html.Div([
        html.Div([
            dcc.Dropdown(
                id='main-filter',
                placeholder='Select an industry',
                options=[
                    {'label': ind, 'value': ind} for ind in dp.get_df()['industry'].unique()
                ],
                value=[],
                multi=True,
                searchable=True
            )
        ], className="twelve column")
    ], id="navbar", className="row bar", style={'margin-bottom': '2%', 'margin-left':'2%', 'margin-right':'2%'}), 

    ## 1st level of charts (Anchor charts)
    html.Div([        
        html.Div([
            dcc.Graph(
                id='pie1',
                figure=get_chart_1_fig()
                )
            ], className="four columns shadow"),
        html.Div([
            dcc.Graph(
                id='donut2',
                figure=get_chart_2_fig()
                )
            ], className="four columns shadow"),

        html.Div([
            dcc.Graph(
                id='bar3',
                figure=get_chart_3_fig()
                )
            ], className="four columns shadow")

        ], className="row", style={'margin-bottom': '3%'}),

    ## 2nd level of charts
    html.Div([
        html.Div([
            dcc.Graph(
                id='stacked_bar4',
                )
                ], className="seven columns shadow"),

        html.Div([
            dcc.Graph(
                id='stacked_bar5',
                )], className="seven columns shadow")

    ], className="row", style={'margin-bottom': '2%'}),

    ## 3rd level of charts
    # Chart 6
    html.Div([
        html.Div([
            dcc.Graph(
                id='stacked_bar6'
                )
                ], className="seven columns shadow"), 

        html.Div([
            dcc.Graph(
                id='stacked_bar7'
                )
                ], className="seven columns shadow")

    ], className="row", style={'margin-bottom': '2%'})

], className="container")

# ---------------------------------------------------------------------------------------------------------
## CALLBACKS

@app.callback(
    [Output(component_id='stacked_bar4', component_property='figure'),
    Output(component_id='stacked_bar5', component_property='figure'),
    Output(component_id='stacked_bar6', component_property='figure'),
    Output(component_id='stacked_bar7', component_property='figure')],
    [Input(component_id='main-filter', component_property='value')]
)
def get_selected_ind(selected_inds):
    if selected_inds == []:
        selected_inds = dp.get_top_n(10)
    return \
        get_chart_4_fig(selected_inds), \
        get_chart_5_fig(selected_inds), \
        get_chart_6_fig(selected_inds), \
        get_chart_7_fig(selected_inds)

if __name__ == '__main__':
    app.run_server(debug=True)
