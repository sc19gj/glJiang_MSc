import os
import dash
import base64
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objs as go
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

from ehr import ehr
from function import up_file_func
#upload file function
def Upfile():
    upfile = dbc.Row(
        [
            dbc.Col(
                [
                    dbc.Row(
                        [
                            html.H1("Upload Your File", className="mt-5 text-white")
                        ],
                        justify="center"
                    ),
                    dbc.Row(
                        [
                            dbc.Col(
                                [
                                    html.Div([
                                        dcc.Upload(
                                            id='upload_file',
                                            children=html.Div(
                                                [
                                                    html.A(html.H3('click upload file'))
                                                ],
                                                className="w-100",
                                                id="upload_live"
                                            ),
                                            className="d-flex align-items-center",
                                            style={
                                                'width': '100%',
                                                'height': '100px',
                                                # 'lineHeight': '60px',
                                                'borderWidth': '1px',
                                                'borderStyle': 'dashed',
                                                'borderRadius': '5px',
                                                'textAlign': 'center',
                                                # 'margin': '10px'
                                            },
                                            # Allow multiple files to be uploaded
                                            multiple=False
                                        ),
                                    ])
                                ],
                                width=6
                            )
                        ],
                        justify="center",
                        className="mt-5 text-white"
                    ),
                    dbc.Row(
                        [
                            dbc.Col(
                                [dbc.Button("Submit", id="up_btn", block=True)],
                                width=6
                            )
                        ],
                        justify="center",
                        className="mt-5"
                    )
                ]
            ),
        ],
        id="up_page",
        justify="center",
        className="mt-2 ml-3"
    )
    return upfile
#------------------------------
#------------------------------
'''
callback
'''
@ehr.callback(
    Output('up_page', 'children'),
    [Input('up_btn', 'n_clicks')],
    [State('upload_file', 'contents')]
    # State('upload_col', 'value')]
)
#return success or error message
def upload_file(btn, content):
    if not btn or btn == 0:
        raise PreventUpdate
    elif btn and content:
        try:
            up_file_func(content)
        except:
            return html.H1('Your Upload File is ERROR！', className="mt-5 text-white")
        else:
            return html.H1('Your Upload File is SCCUESS', className="mt-5 text-white")


@ehr.callback(
    Output('upload_live','children'),
    # Output('upload_col', 'options'),
    # Output('upload_col_row', 'style')],
    [Input('upload_file','contents')],
    [State('upload_file','filename')]
)
def upload(content, name):
    if content:
        up_live_name = [html.A(name)]
    else:
        raise PreventUpdate
    return up_live_name
