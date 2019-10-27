# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table as dt
import pandas as pd
import plotly.graph_objs as go
from dash.dependencies import Input, Output

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

colors = {
'background': '#111111',
'text': '#7FDBFF'
}

df = pd.read_csv(
    'https://gist.githubusercontent.com/chriddyp/'
    'c78bf172206ce24f77d6363a2d754b59/raw/'
    'c353e8ef842413cae56ae3920b8fd78468aa4cb2/'
    'usa-agricultural-exports-2011.csv')

dataframe = pd.read_csv(
    'https://gist.githubusercontent.com/chriddyp/' +
    '5d1ea79569ed194d432e56108a04d188/raw/' +
    'a9f9e8076b837d541398e999dcbac2b2826a81f8/'+
    'gdp-life-exp-2007.csv')



app.layout = html.Div(# style={'backgroundColor': colors['background']}, 
    children=[
    html.H1(
        children='Hello Dash',
        style={
        'textAlign': 'center',
        'color': colors['text']
        }
        ),

    html.Div(children='Dash: A web application framework for Python.', style={
        'textAlign': 'center',
        'color': colors['text']
        }),

    dcc.Dropdown(id= 'state_dropdown',
        options=[
        {'label': 'Alabama', 'value': 'Alabama'},
        {'label': 'Alaska', 'value': 'Alaska'},
        {'label': 'California', 'value': ' California'}
        ],
        value=[],
        multi=True
        ),

    html.Div(id='my-div-dropdown'),

    html.Div(
      dt.DataTable(

            id='data_table',
            columns=[{"name": i, "id": i} for i in df.columns],
            data=df.to_dict('records'))),

    html.Div([
    dcc.Input(id='my-id', value='initial value', type='text'),
    html.Div(id='my-div')
]),

    dcc.Graph(
        id='life-exp-vs-gdp',
        figure={
            'data': [
                go.Scatter(
                    x=dataframe[dataframe['continent'] == i]['gdp per capita'],
                    y=dataframe[dataframe['continent'] == i]['life expectancy'],
                    text=dataframe[dataframe['continent'] == i]['country'],
                    mode='markers',
                    opacity=0.7,
                    marker={
                        'size': 15,
                        'line': {'width': 0.5, 'color': 'white'}
                    },
                    name=i
                ) for i in dataframe.continent.unique()
            ],
            'layout': go.Layout(
                xaxis={'type': 'log', 'title': 'GDP Per Capita'},
                yaxis={'title': 'Life Expectancy'},
                margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
                legend={'x': 0, 'y': 1},
                hovermode='closest'
            )
        }
    ),

    dcc.Graph(
        id='example-graph-2',
        figure={
        'data': [
        {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'SF'},
        {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': u'Montréal'},
        ],
        'layout': {
        'plot_bgcolor': colors['background'],
        'paper_bgcolor': colors['background'],
        'font': {
        'color': colors['text']
        }
        }
        }
        ),

    dcc.Graph(
        id='example-graph-3',
        figure={
        'data': [
        {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'SF'},
        {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': u'Montréal'},
        ],
        'layout': {
        'plot_bgcolor': colors['background'],
        'paper_bgcolor': colors['background'],
        'font': {
        'color': colors['text']
        }
        }
        }
        )

    ])

@app.callback(
    Output(component_id='my-div', component_property='children'),
    [Input(component_id='my-id', component_property='value')]
)
def update_output_div(input_value):
    return 'You\'ve entered "{}"'.format(input_value)

# to print the message
@app.callback(
    Output(component_id='my-div-dropdown', component_property='children'),
    [Input(component_id='state_dropdown', component_property='value')]
)
def update_output_div(input_value):
    return 'You\'ve entered "{}"'.format(input_value)

# to output the changed dataframe 
@app.callback(
    Output(component_id='data_table', component_property='data'),
    [Input(component_id='state_dropdown', component_property='value')]
)
def update_output_div(input_value):
    if input_value == []:
        return df.to_dict('records')
    return df[df['state'].isin(input_value)].to_dict('records')

if __name__ == '__main__':
    app.run_server(debug=True)