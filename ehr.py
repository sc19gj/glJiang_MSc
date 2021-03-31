# -*- coding: utf-8 -*-
import dash
import os
import pandas as pd
from function import data_analyse, distributions

#------------------------------
'''
set app name is ehr
'''
ehr = dash.Dash(__name__)
#-----

#------------------------------
#------get data from 'testdata.csv' in the project folder-----
#------------------------------
def Get_data():
#    datatest = pd.read_csv(os.getcwd() + r'\testdata.csv' ) #Using in Windows OS: reading dataset
    datatest = pd.read_csv(os.getcwd() + '/testdata.csv' )  #Using in Mac OS: reading dataset

    len_data, datatest_make = data_analyse(datatest)
    datatest_make_T = pd.DataFrame(datatest_make.values.T, index=datatest_make.columns, columns=datatest_make.index)

    datatest_index = datatest_make.columns.values
    # year_list = datatest['Payment_Year'].dropna().unique().tolist()
    col_list = datatest_make.index.values
    constancy = distributions(datatest_make)
    return datatest, len_data, datatest_make, datatest_make_T, datatest_index, col_list, constancy