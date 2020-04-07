import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_gif_component as gif
import json
from dash.dependencies import Input, Output, State

import requests
import numpy as np
import os

# external stylesheets
external_stylesheets = [dbc.themes.BOOTSTRAP]

# launch app
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.scripts.config.serve_locally = True
app.config.suppress_callback_exceptions = True


class DashCallbackVariables:
    """Class to store information useful to callbacks"""

    def __init__(self):
        self.n_clicks = {1: 0}

    def update_n_clicks(self, nclicks, bt_num):
        self.n_clicks[bt_num] = nclicks


callbacks_vars = DashCallbackVariables()

colors = {
    'background': '#FFFFFF',
    'text': '#383c4a',
    'styledBackground': '#30333d'
}

style_cell={
    'font-size': 14,
    'color': colors['text'],
    'backgroundColor': colors['background'],
    'whiteSpace':'normal'
}

app.layout = html.Div([
    html.Div([], style={'padding':30}),
    html.H1(
            children='May the rng gods amuse you',
            style={
                'textAlign': 'center',
                'color': colors['text']
                }
    ),
    html.Div(
        children='Modern Talking lyrics are a few words away from you:', style={
                'textAlign': 'center',
                'color': colors['text']
                }
    ),
    html.Div([], style={'padding':15}),
    dbc.Row([
        dbc.Col('', width=3),
        dbc.Col([
            dbc.Input(
                    id='question',
                    type='text',
                    placeholder='Input starting lyrics...',
                    style=style_cell
                ),
            html.Div([],style={
                'textAlign': 'center',
                'color': colors['text'],
                'padding':10}),
            dbc.Button('Le go', id='button', color='primary'),
        ]),
        dbc.Col('', width=3)                                        
    ],style={
                'textAlign': 'center',
                'color': colors['text'],
                'padding':10}),
    html.Div([],style={
                'textAlign': 'center',
                'color': colors['text'],
                'padding':10}),
    html.Div(
        [
        dbc.Modal(
            [
                dbc.ModalHeader(id='question_modal'),
                dbc.ModalBody(children=[
                    html.Div(
                        'Cyber monkeys are trying to find the typewriter...', 
                        id='answer_1'),
                    html.Div(children=[
                        gif.GifPlayer(
                            gif='../assets/monkey.gif',
                            still='../assets/monkey_still.png',
                            autoplay=True
                        ),], style={
                                    'textAlign': 'center',
                                    'color': colors['text'],
                                    'padding':10}, id='monkeys')                    
                                    ]
                ),
                dbc.ModalFooter(
                    dbc.Button("Close", id="close", color='light', className="ml-auto")
                ),
            ],
            id="modal",
        ),
        ], style={
                'textAlign': 'center',
                'color': colors['text'],
                'padding':10},
    )
], style={'backgroundColor': colors['background']})


# callbacks
@app.callback(
    [Output('answer_1', 'children'),
    Output('monkeys', 'children'),
    Output('question_modal', 'children')],
    [Input('button', 'n_clicks')],
    [State('question', 'value')])
def update_output(n_clicks, value):
    if n_clicks:
        # It was triggered by a click on the button 1
        url = 'http://0.0.0.0/generator?text='+value  # change to actual api ip
        callbacks_vars.update_n_clicks(n_clicks, 1)
        answer = requests.get(url, timeout=60)       
        
        return dcc.Markdown(answer.json()[0], id='answer_modal'), None, value

@app.callback(
    Output('modal','is_open'),
    [Input('button', 'n_clicks'), Input('close','n_clicks')],
    [State('modal', 'is_open')]
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open
            
        

if __name__ == '__main__':
    app.run_server()
