import os
import numpy as np
import pandas as pd
import base64
import dash_core_components as dcc
import dash_html_components as html

#------------------------------
#------get data statistics-----
#--read profiling tasks results--
#------------------------------
def data_analyse(datatest):
    len_list = []
    for i in datatest.columns.values:
        for l in datatest[i]:
            list_res = []
            list_res.append(i)
            list_res.append(len(str(l)))
            len_list.append(list_res)   
    len_data = pd.DataFrame(len_list, columns=['name','len'])
    datatest_make = pd.DataFrame(index=datatest.columns.values)
    different_res = []
    row_len_res = []
    null_len_res = []
    unique_res = []
    for i in datatest.columns.values:
        row_len_temp = len(datatest[i]) - datatest[i].isnull().sum()
        different_res.append(len(datatest[i].value_counts()) / row_len_temp)
        row_len_res.append(row_len_temp)
        unique_res.append(np.sum((datatest[i].value_counts().values == 1) !=0))
    datatest_make['distinct'] = different_res
    datatest_make['num_rows'] = row_len_res
    datatest_make['null_values'] = datatest.isnull().sum(axis=0).values
    datatest_make['uniqueness'] = unique_res
    return len_data, datatest_make

#------get dataset constancy, is another profiling task----
# ----last version used, and may be useful in next version---
#------------------------------
def distributions(datatest_make):
    constancy = []
    length = len(datatest_make)
    for i in datatest_make.columns.values:
        res_list = datatest_make[i].value_counts().sort_values(ascending = False,inplace = False).values.tolist()
        if res_list:
            constancy.append(res_list[0]/length)
        else:
            constancy.append(0)
    return constancy

#------------------------------
#------upload file function----
#------------------------------
def up_file_func(content):
#    path=os.getcwd() + r'\testdata.csv'     # using in Windows OS: upload file path and file name
    path=os.getcwd() + '/testdata.csv'     # using in Mac OS: upload file path and file name

    content_type, content_string = content.split(',')
    decoded = base64.b64decode(content_string)

    if os.path.exists(path):
        os.remove(path)
    with open(path,'wb+')as destination:
        destination.write(decoded)

#------------------------------

def Attach():
    attach = html.Div(
        [
            html.Div(id="up_page"),
            html.Div(id="up_btn"),
            dcc.Upload(html.Div(id="upload_live"), id="upload_file"),
            dcc.Dropdown(id="upload_col"),
            html.Div(id="upload_col_row"),
            dcc.RadioItems(id="year_list"),
            dcc.Dropdown(id="select_list"),
            dcc.RadioItems(id="sort_data"),
            dcc.RadioItems(id="sort_type"),
            dcc.RadioItems(id="constancy_type"),
            dcc.Graph(id="fig1"),
            dcc.Graph(id="fig2"),
            dcc.Graph(id="fig3"),
            dcc.Graph(id="fig4"),
            dcc.Graph(id="fig5"),
            dcc.Graph(id="fig_constancy"),
            dcc.Dropdown(id="chart_T"),
            dcc.RadioItems(id="chart_T_type"),
            dcc.RadioItems(id="chart_T_sort"),
            dcc.Graph(id="mini_line_T"),
            dcc.Graph(id="mini_line_T_box"),
            dcc.Dropdown(id="chart1"),            
            dcc.RadioItems(id="chart_mini_type"),
            dcc.RadioItems(id="chart_mini_sort"),
            dcc.Graph(id="mini_line1"),
            dcc.Dropdown(id="chart_T_2"),
            dcc.RadioItems(id="chart_T_type_2"),
            dcc.RadioItems(id="chart_T_sort_2"),
            dcc.Graph(id="mini_line_T_2"),
            dcc.Graph(id="mini_line_T_box_2"),
        ],
        style={"display":"None"}
    ) 
    return attach