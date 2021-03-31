import os
import dash
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objs as go
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output


# it is html page showing visualisations in row1(Filtering Pgae)
def Row2():
    id_list = ['fig1', 'fig2', 'fig3', 'fig4']
    row2 = dbc.Row(
        [
            dbc.Col(
                [
                    dbc.Row(
                        [
                            dbc.Col(
                                dcc.Graph(id=fig_id),width=3
                            ) for fig_id in id_list
                        ],
                        className=""
                    ),
                    dbc.Row(
                        [
                            dbc.Col(
                                dcc.Graph(id="fig5"),width=12
                            )
                        ],
                        className="mt-5"
                    )
                
                ]
            )            
        ],
        className="text-white"
    )
    return row2