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
from function import data_analyse, distributions

#-----
'''
format data
'''
# datatest, len_data, datatest_make, datatest_make_T, datatest_index, col_list, constancy = Get_data()

#-----
# it is html page showing visualisations in row4(Whole Dataset Pgae)
def Row4():
    row4 = dbc.Row(
        [
            dbc.Col(
                [
                    dbc.Row(
                        [
                            dbc.Col(
                                [
                                    dcc.Dropdown(
                                        id='chart1',
                                        options=[{'label': i, 'value': i} for i in ['distinct','num_rows','null_values','uniqueness','value_length']],
                                        value='distinct',
                                        className="text-dark"
                                    )
                                ]
                            )                            
                        ],
                        justify="center"
                    ),
                    dbc.Row(
                        [
                            dbc.Col(
                                [
                                    dcc.RadioItems(
                                        id='chart_mini_type',
                                        options=[{'label': i, 'value': i} for i in ['Line','Bar']],
                                        value='Bar',
                                        labelStyle={'display': 'inlineBlock', 'marginLeft': '50px'}
                                    )
                                ]
                            ),
                            dbc.Col(
                                [
                                    dcc.RadioItems(
                                        id='chart_mini_sort',
                                        options=[{'label': i, 'value': i} for i in ['asc', 'desc']],
                                        value='asc',
                                        labelStyle={'display': 'inlineBlock', 'marginLeft': '50px'}
                                    )
                                ]
                            )                            
                        ],
                        justify="center",
                        className="mt-3"
                    ),
                    dbc.Row(
                        [
                            dbc.Col(
                                dcc.Graph(id='mini_line1')
                            )                            
                        ],
                        justify="center")
                ]
            )
        ],
        className="mt-5 text-white"
    )
    return row4



'''
callback
'''

@ehr.callback(
    Output('mini_line1', 'figure'),
    [Input('chart1', 'value'),
    Input('chart_mini_type', 'value'),
    Input('chart_mini_sort', 'value')]
    )


def update_chart_select(chart, chart_mini_type, chart_mini_sort):
    '''update chart'''
    datatest, len_data, datatest_make, datatest_make_T, datatest_index, col_list, constancy = Get_data()
    if not chart or not chart_mini_sort or not chart_mini_type:
        raise PreventUpdate
    else:
        if chart != 'value_length':
            if chart_mini_sort == 'asc':
                datatest_make_sort = datatest_make.sort_values(by=chart, ascending = True,inplace = False)
            elif chart_mini_sort == 'desc':
                datatest_make_sort = datatest_make.sort_values(by=chart, ascending = False,inplace = False)
            len_data = ''
        else:
            len_data, datatest_make_sort = data_analyse(datatest)
        return update_chart(datatest_make_sort, chart, chart_mini_type, len_data)


def update_chart(df, chart, chart_mini_type, len_data):
    '''update chart'''
    # print('chart is:', chart)
    if chart == 'value_length':
        fig = px.box(len_data, x='len', y='name', color="name")
        fig.update_xaxes(visible=False, fixedrange=True)
        fig.update_yaxes(visible=True, fixedrange=True, title='')
    else:
        if chart_mini_type == 'Line':
            # fig = px.line(df, y=chart,x=df.index, height=500)
            fig = go.Figure()
            fig = fig.add_trace(go.Scatter(x=df.index, y=df[chart], mode='lines', line=dict(color='rgb(255,255,0)', width=4),connectgaps=True))
            fig.update_xaxes(visible=True, fixedrange=True, showgrid=False)
            fig.update_yaxes(visible=False, fixedrange=True)
            # fig.update_layout(xaxis=dict(showline=True,,showticklabels=True,ticks='outside'))
        elif chart_mini_type == 'Bar':
            fig = px.bar(df, x=chart,y=df.index ,orientation='h', barmode="group", color=chart)
            fig.update_xaxes(visible=False, fixedrange=True)
            fig.update_yaxes(visible=True, fixedrange=True, title='')
            fig.update_coloraxes(colorbar=dict(thickness=10))
    fig.update_layout(
        annotations=[],                                 # remove facet/subplot labels
        overwrite=True,
        showlegend=False,                                # strip down the rest of the plot
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="#7F9BB4",
        height=300,
        # width=450,
        bargap=0.4,
        margin=dict(t=10,l=10,b=10,r=10)
    )
    
    return fig