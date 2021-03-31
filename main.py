import os
import dash
from dash.exceptions import PreventUpdate
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objs as go
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output

from ehr import ehr, Get_data
from function import data_analyse, distributions, Attach
from component.row1 import Row1
from component.row2 import Row2
from component.row3 import Row3
from component.row4 import Row4
from component.leftlist import leftlist
from component.upfile import Upfile

#------------------------------
'''
set app name is ehr
'''
#-----
'''
format data
'''
# datatest, len_data, datatest_make, datatest_make_T, datatest_index, col_list, constancy = Get_data()
# year_list = datatest['Payment_Year'].dropna().unique().tolist()
#-----
'''
set main layout
'''

ehr.layout = dbc.Container(
        [
            dbc.Row(
                [
                    dbc.Col(
                        [
                            leftlist()
                        ],
                        width=2,
                        className="sidebar border-right border-white min-vh-100",
                    ),
                    dbc.Col(
                        [
                            html.Div(
                                [
                                    Attach()               
                                ],
                                id="pagecontent"
                            ),
                        ]
                    ),
                ],
                justify="center"
            ),
            dcc.Location(id='url', refresh=False),
        ],
        id="Container",
        className="mw-100 bg-dark", 
    )

#------------------------------
'''
callback
Jump by Url
'''
@ehr.callback(
    Output('pagecontent', 'children'),
    [Input('url', 'pathname')]
)
def index(url):
    datatest, len_data, datatest_make, datatest_make_T, datatest_index, col_list, constancy = Get_data()
    if url == '/index':
        return Upfile() 
    elif url == '/row1':
        return [Row1(datatest_index),Row2()]
    elif url == '/row3':
        return Row3(col_list)
    elif url == '/row4':
        return Row4()
    else:
        raise PreventUpdate

#------------------------------
#-----
'''
run server 
'''

if __name__ == '__main__':
    ehr.run_server(debug=True)
#-----------------------------