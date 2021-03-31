{"output":"..mini_line_T_2.figure...mini_line_T_box_2.figure..","outputs":[{"id":"mini_line_T_2","property":"figure"},{"id":"mini_line_T_box_2","property":"figure"}],"inputs":[{"id":"chart_T_2","property":"value","value":"Medicaid_EP_Hospital_Type"},{"id":"chart_T_type_2","property":"value","value":"Bar"},{"id":"chart_T_sort_2","property":"value","value":"asc"}],"changedPropIds":["chart_T_2.value"]}# -*- coding: utf-8 -*-
import os
import sys
import pytest
import json
import jsonpath
import pandas as pd
from UnitTestCase.Tools import Tools
from UnitTestCase.testEHR import TestEHR

class TestRowData:
    url = 'http://127.0.0.1:8050/'
    upload_file = '_dash-update-component'
    upload_url = url + upload_file
    @classmethod
    def get_column_data_by_json(cls, path):
        json_data = Tools.read_file(path)

        return json_data

    @classmethod
    def get_column_page_data(cls, path):
        post_data = cls.get_column_data_by_json(path)
        response = Tools.post_method(TestRowData.upload_url, post_data)
        response = json.loads(response)
        null_values = jsonpath.jsonpath(response, '$..mini_line_T..data')[0][0]["x"][0]
        distinct_value = jsonpath.jsonpath(response, '$..mini_line_T..data')[0][1]["x"][0]
        num_rows = jsonpath.jsonpath(response, '$..mini_line_T..data')[0][2]["x"][0]
        uniqueness = jsonpath.jsonpath(response, '$..mini_line_T..data')[0][3]["x"][0]
        total_num = int(null_values + num_rows)

        return total_num, distinct_value, uniqueness



if __name__ == '__main__':
    row3 = TestRowData()
    pytest.main(['-s', 'testRowData.py'])