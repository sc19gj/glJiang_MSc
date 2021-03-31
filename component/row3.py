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

# -----
'''
format data
'''
# datatest, len_data, datatest_make, datatest_make_T, datatest_index, col_list, constancy = Get_data()
# it is html page showing visualisations in row3(Comparison Pgae)
def Row3(col_list):
    
    row3 = dbc.Row(
        [
            dbc.Col(
                [
                    dbc.Row(
                        [
                            dbc.Col(
                                [
                                    dcc.Dropdown(
                                        id='chart_T',
                                        options=[{'label': i, 'value': i} for i in col_list],
                                        value=col_list[0],
                                        className="text-dark"
                                    )
                                ]
                            )
                        ],
                        className="text-white",
                        justify="center"
                    ),
                    dbc.Row(
                        [
                            dbc.Col(
                                [
                                    dcc.RadioItems(
                                        id='chart_T_type',
                                        options=[{'label': i, 'value': i} for i in ['Line', 'Bar']],
                                        value='Bar',
                                        labelStyle={'marginLeft': '10px'}
                                    ),
                                ]
                            ),
                            dbc.Col(
                                [
                                    dcc.RadioItems(
                                        id='chart_T_sort',
                                        options=[{'label': i, 'value': i} for i in ['asc', 'desc']],
                                        value='asc',
                                        labelStyle={'marginLeft': '10px'}
                                    )
                                ]
                            )
                        ],
                        justify="center",
                        className="mt-3"
                    ),
                    dbc.Row(
                        [
                            dbc.Col(dcc.Graph(id='mini_line_T')),
                        ],
                        justify="center",
                        className="mt-2"
                    ),
                    dbc.Row(
                        [
                            dbc.Col(dcc.Graph(id='mini_line_T_box'))
                        ],
                        justify="center",
                        className=""
                    )
                ],
                # width=6
            ),
            # col2
            dbc.Col(
                [
                    dbc.Row(
                        [
                            dbc.Col(
                                [
                                    dcc.Dropdown(
                                        id='chart_T_2',
                                        options=[{'label': i, 'value': i} for i in col_list],
                                        value=col_list[0],
                                        className="text-dark"
                                    )
                                ]
                            )
                        ],
                        className="text-white",
                        justify="center"
                    ),
                    dbc.Row(
                        [
                            dbc.Col(
                                [
                                    dcc.RadioItems(
                                        id='chart_T_type_2',
                                        options=[{'label': i, 'value': i} for i in ['Line', 'Bar']],
                                        value='Bar',
                                        labelStyle={'marginLeft': '10px'}
                                    ),
                                ]
                            ),
                            dbc.Col(
                                [
                                    dcc.RadioItems(
                                        id='chart_T_sort_2',
                                        options=[{'label': i, 'value': i} for i in ['asc', 'desc']],
                                        value='asc',
                                        labelStyle={'marginLeft': '10px'}
                                    )
                                ]
                            )
                        ],
                        justify="center",
                        className="mt-3"
                    ),
                    dbc.Row(
                        [
                            dbc.Col(dcc.Graph(id='mini_line_T_2')),
                        ],
                        justify="center",
                        className="mt-2"
                    ),
                    dbc.Row(
                        [
                            dbc.Col(dcc.Graph(id='mini_line_T_box_2'))
                        ],
                        justify="center",
                        className=""
                    )
                ],
                # width=6
            )
        ],
        className="mt-5 text-white"
    )
    return row3


'''
callback
'''


@ehr.callback(
    [Output('mini_line_T', 'figure'),
     Output('mini_line_T_box', 'figure')],
    [Input('chart_T', 'value'),
     Input('chart_T_type', 'value'),
     Input('chart_T_sort', 'value')]
)
def update_chart_select(chart, chart_T_type, chart_T_sort):
    '''update chart'''
    datatest, len_data, datatest_make, datatest_make_T, datatest_index, col_list, constancy = Get_data()
    if not chart or not chart_T_sort or not chart_T_type:
        raise PreventUpdate
    else:
        if chart_T_sort == 'asc':
            datatest_make_T_sort = datatest_make_T.sort_values(by=chart, ascending=True, inplace=False)
        elif chart_T_sort == 'desc':
            datatest_make_T_sort = datatest_make_T.sort_values(by=chart, ascending=False, inplace=False)
        return [update_chart_T(datatest_make_T_sort, chart, chart_T_type),
                update_chart_T_box(len_data[len_data['name'] == chart])]


'''
callback about col2
'''


@ehr.callback(
    [Output('mini_line_T_2', 'figure'),
     Output('mini_line_T_box_2', 'figure')],
    [Input('chart_T_2', 'value'),
     Input('chart_T_type_2', 'value'),
     Input('chart_T_sort_2', 'value')]
)

# update chart according to drop down menu
def update_chart_select(chart, chart_T_type, chart_T_sort):
    '''update chart'''
    datatest, len_data, datatest_make, datatest_make_T, datatest_index, col_list, constancy = Get_data()
    if not chart or not chart_T_sort or not chart_T_type:
        raise PreventUpdate
    else:
        if chart_T_sort == 'asc':
            datatest_make_T_sort = datatest_make_T.sort_values(by=chart, ascending=True, inplace=False)
        elif chart_T_sort == 'desc':
            datatest_make_T_sort = datatest_make_T.sort_values(by=chart, ascending=False, inplace=False)
        return [update_chart_T(datatest_make_T_sort, chart, chart_T_type),
                update_chart_T_box(len_data[len_data['name'] == chart])]


def update_chart_T(df, chart, chart_T_type):
    '''update chart'''
    if chart_T_type == 'Line':
        fig = px.line(df, y=chart, x=df.index, color_discrete_sequence=["yellow"])
        fig.update_xaxes(visible=True, fixedrange=True, showgrid=False, title='')
        fig.update_yaxes(visible=False, fixedrange=True)
    elif chart_T_type == 'Bar':
        fig = px.bar(df, x=chart, y=df.index, orientation='h', barmode="group", color=df.index,
                     color_discrete_sequence=["red", "orange", "blue", "yellow"])
        fig.update_xaxes(visible=False, fixedrange=True)
        fig.update_yaxes(visible=True, fixedrange=True, title='')
    fig.update_layout(
        annotations=[],  # remove facet/subplot labels
        overwrite=True,
        showlegend=False,  # strip down the rest of the plot
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="#7F9BB4",
        height=250,
        bargap=0.4,
        # width=450,
        # margin=dict(t=10,l=10,b=10,r=10)
    )
    return fig


def update_chart_T_box(len_data):
    '''update chart'''
    fig = px.box(len_data, x='len', y='name', color_discrete_sequence=["yellow"])
    fig.update_xaxes(visible=False)
    fig.update_yaxes(visible=True, fixedrange=True, title='')
    fig.update_layout(
        annotations=[],  # remove facet/subplot labels
        overwrite=True,
        showlegend=True,  # strip down the rest of the plot
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="#7F9BB4",
        height=250,
        # width=450,
        # margin=dict(t=10,l=10,b=10,r=10)
    )
    return fig
