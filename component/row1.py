import os
import dash
# import chardet
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
# it is html page showing visualisations in row1(Filtering Pgae)
def Row1(datatest_index):
    datatest, len_data, datatest_make, datatest_make_T, datatest_index, col_list, constancy = Get_data()
    datatest_make_index = datatest.columns.values
    row1 = dbc.Row(
        [
            dbc.Col(
                [
                    dbc.Row(
                        [
                            dbc.Col(
                                [
                                    dcc.Dropdown(
                                        id='select_list',
                                        options=[{'label': i, 'value':i} for i in datatest_make_index],
                                        className="text-dark"
                                    )
                                ],
                                width=6
                            )
                        ],
                        className="mt-3"
                    ),
                    dbc.Row(
                        [
                            dbc.Col(
                                [
                                    dcc.Dropdown(
                                        id='year_list',
                                        # labelStyle={'marginLeft':'10px'},
                                        style={'display':'none'},
                                        className="text-dark"
                                    )
                                ],
                                width=4
                            )
                        ],
                        className="mt-2"
                    ),                    
                    dbc.Row(
                        [
                            dcc.RadioItems(
                                id='sort_data',
                                options=[{'label': i, 'value': i} for i in datatest_index],
                                value='distinct',
                                labelStyle={'marginLeft':'10px'}
                            )
                        ],
                        className="mt-2"
                    ),
                    dbc.Row(
                        [
                            dcc.RadioItems(
                                id='sort_type',
                                options=[{'label': i, 'value': i} for i in ['asc', 'desc']],
                                value='asc',
                                labelStyle={'marginLeft':'10px'}
                            )
                        ]
                    )
                ]
            ),
            
        ],
        className="text-white"
    )
    return row1

'''
callback
'''

@ehr.callback(
    Output('year_list', 'options'),
    Output('year_list', 'value'),
    Output('year_list', 'style'),
    [Input('select_list', 'value')]
)



# update drop down mune
def update_select_list(select):
    datatest, len_data, datatest_make, datatest_make_T, datatest_index, col_list, constancy = Get_data()
    if select:
        sel_list = datatest[select].dropna().unique().tolist()
        sel_list.sort()
        year_list = [{'label': i, 'value':i} for i in sel_list]
        year_list_value = sel_list[0]
        year_list_style = {}
        return year_list, year_list_value, year_list_style
    else:
        raise PreventUpdate

#-----
@ehr.callback(
    [Output('fig1', 'figure'),
    Output('fig2', 'figure'),
    Output('fig3', 'figure'),
    Output('fig4', 'figure'),
    Output('fig5', 'figure')],
    [Input('sort_type', 'value'),
    Input('sort_data', 'value'),
    Input('year_list', 'value'),
    Input('select_list', 'value')]
    )


def update_chart_select(sort_type, sort_data, year, sel_value):
    '''update chart Row2'''

    datatest, len_data, datatest_make, datatest_make_T, datatest_index, col_list, constancy = Get_data()
    if sel_value and year:
        len_data, datatest_make = data_analyse(datatest[datatest[sel_value] == year])
        print('sort_data=', sort_data)
        print('year=', year)
        if sort_type == 'asc':
            datatest_make_sort = datatest_make.sort_values(by=sort_data, ascending = True,inplace = False)
        elif sort_type == 'desc':
            datatest_make_sort = datatest_make.sort_values(by=sort_data, ascending = False,inplace = False)
        return [update_chart(1, datatest_make_sort), update_chart(2, datatest_make_sort), update_chart(3, datatest_make_sort), update_chart(4, datatest_make_sort), update_chart_box(len_data)]
    else:
        raise PreventUpdate
    


def update_chart(type, df):
    '''update fig1, fig2, fig3, fig4, fig5 chart'''
    if type == 1:
        this_tag = ['distinct', 'distinct']
    elif type == 2:
        this_tag = ['num_rows', 'num-rows']
    elif type == 3:
        this_tag = ['null_values', 'null values']
    elif type == 4:
        this_tag = ['uniqueness', 'uniqueness']
    fig = px.bar(df,x=this_tag[0],orientation = 'h',barmode='group', color=this_tag[0])
    if type == 1:
        fig.update_yaxes(visible=True, fixedrange=True, title='')
    else:
        fig.update_yaxes(visible=False, fixedrange=True)
    fig.update_xaxes(visible=False, fixedrange=True)
    fig.add_annotation(
        x=0.5, y=1, xanchor='left', yanchor='bottom', xref='paper', yref='paper', showarrow=False, text=this_tag[1]
    )
    fig.update_layout(
        coloraxis_showscale=False,    
        overwrite=True,                            # strip down the rest of the plot
        showlegend=True,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="#7F9BB4",
        bargap=0.4
        # height=500,
        # width=600
        # margin=dict(t=10,l=10,b=10,r=10)
    )
    return fig

#----------generate box plot----
def update_chart_box(len_data):
    fig = px.box(len_data, x='len', y='name', color="name")
    fig.update_xaxes(visible=False, fixedrange=True)
    fig.update_yaxes(visible=True, fixedrange=True, title='')
    fig.update_layout(overwrite=True)
    fig.add_annotation(
        x=0.5, y=1, xanchor='left', yanchor='bottom', xref='paper', yref='paper', showarrow=False, text='value length'
    )
    fig.update_layout(                                  # strip down the rest of the plot
        showlegend=True,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="#7F9BB4",
        # height=600,
        # width=800
        # margin=dict(t=10,l=10,b=10,r=10)
    )
    return fig

# ----last version used, and may be useful in next version---
def update_chart6(constancy_type):
    datatest, len_data, datatest_make, datatest_make_T, datatest_index, col_list, constancy = Get_data()
    if constancy_type == 'Bar':
        fig_constancy = px.bar(y=constancy, x=datatest_make.columns.values)
    elif constancy_type == 'Line':
        fig_constancy = px.line(y=constancy, x=datatest_make.columns.values)
    fig_constancy.update_xaxes(visible=True, fixedrange=True, title='', showgrid=False)
    fig_constancy.update_yaxes(visible=False, fixedrange=True)
    fig_constancy.update_layout()
    fig_constancy.add_annotation(
        x=0.5, y=1, xanchor='left', yanchor='bottom', xref='paper', yref='paper', showarrow=False, text='distributions-constancy'
    )
    fig_constancy.update_layout(      
        overwrite=True,                            # strip down the rest of the plot
        showlegend=True,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="#7F9BB4",
        height=300,
        # width=500,
        # margin=dict(t=10,l=10,b=10,r=10)
    )
    return fig_constancy