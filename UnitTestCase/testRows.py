import os
import sys
import pytest
import traceback
import json
import jsonpath
import pandas as pd
from UnitTestCase.Tools import Tools
from UnitTestCase.testRowData import TestRowData

class TestRow:
    url = 'http://127.0.0.1:8050/'
    upload_file = '_dash-update-component'
    upload_url = url + upload_file
    def setup(self):
        """This is where we initialize the resource """
        pass
    def tearDown(self):
        """Do the release of resources here """
        pass
    def get_columns_list(self):
        path = os.getcwd() + '/../testdata.csv'
        df = pd.read_csv(path , encoding="gbk")
        all_columns = df.columns.values
        column_list = list(all_columns)
        return column_list
    def get_row1_post_data(self, path):
        json_data = Tools.read_file(path)
        return json_data
    def get_row1_page_content(self, path):
        post_data = self.get_row1_post_data(path)
        response = Tools.post_method( TestRow.upload_url,   post_data)
        response = json.loads(response)
        options = jsonpath.jsonpath(response, '$..options')[0]
        columns_list = []
        for label in options:
            columns_list.append(label.get("label"))
        return columns_list

    def test_column_names(self):
        file_columns_names = self.get_columns_list()
        print('file_columns_names=', file_columns_names)
        path = os.getcwd() + '/row1PostData.json'
        interface_columns_names = self.get_row1_page_content(path)
        print('interface_columns_names=', interface_columns_names)
        length = len(interface_columns_names)
        assert file_columns_names == interface_columns_names
        total_num = self.count_total_num()
        assert  total_num == length
    def get_column_datas(self, column_name):
        try:
            path = os.getcwd() + '/../testdata.csv'
            df = pd.read_csv(path, encoding='utf-8')
            column_values = df[column_name]
            print('column_values=', column_values)
            uniqure_column_values = column_values.unique()
            column_values_list = column_values.values.tolist()
            print('column_values_list=', column_values_list)
            return column_values_list
        except Exception as e:
            print(e)
    def get_column_data_by_json(self, path):
        json_data = Tools.read_file(path)
        return json_data
    def get_column_page_data(self, path):
        post_data = self.get_column_data_by_json(path)
        response = Tools.post_method(TestRow.upload_url, post_data)
        response = json.loads(response)
        options = jsonpath.jsonpath(response, '$..options')[0]
        columns_list_page = []
        for label in options:
            columns_list_page.append(label.get("label"))
        return columns_list_page

    def test_column_values(self):
        column_name = 'Provider Name'
        file_columns_values = self.get_column_datas(column_name)
        path = os.getcwd() + '/providerName_column_values.json'
        interface_columns_values = self.get_column_page_data(path)
        length = len(file_columns_values)
        file_columns_values_set = set(file_columns_values)
        file_columns_values = list(file_columns_values_set)
        file_columns_values = file_columns_values[1:]
        file_columns_values.sort()
        interface_columns_values.sort()
        assert interface_columns_values == file_columns_values
        path = os.getcwd() + '/row3_NPI_post_data.json'
        total_num, distinct_value, uniqueness = TestRowData.get_column_page_data(path)
        assert  length == total_num
    def get_distinct_labels(self, path):
        distinct_labels_json = Tools.read_file(path)
        return distinct_labels_json
    def get_distinct_labels_page_response(self):
        path = os.getcwd() + '/distinct_labels_asc.json'
        post_data = self.get_column_data_by_json(path)
        response = Tools.post_method(TestRow.upload_url, post_data)
        response = json.loads(response)
        options = jsonpath.jsonpath(response, '$..y')[0]
        return options

    def get_num_rows_x_num(self):
        path = os.getcwd() + '/distinct_labels_asc.json'
        post_data = self.get_column_data_by_json(path)
        response = Tools.post_method(TestRow.upload_url, post_data)
        response = json.loads(response)
        x_value = jsonpath.jsonpath(response, '$..fig2.figure.data[0]')[0]
        num_rows_x_value = x_value.get("x")
        return num_rows_x_value

    def get_null_value_x_num(self):
        path = os.getcwd() + '/distinct_labels_asc.json'
        post_data = self.get_column_data_by_json(path)
        response = Tools.post_method(TestRow.upload_url, post_data)
        response = json.loads(response)
        x_value = jsonpath.jsonpath(response, '$..fig3.figure.data[0]')[0]
        null_value_x_value = x_value.get("x")
        return null_value_x_value

    def count_total_num(self):
        null_value_x_value = self.get_null_value_x_num()
        num_rows_x_value = self.get_num_rows_x_num()
        total_num  = 0
        for i in range  ( len(null_value_x_value)):
            total_num+= null_value_x_value[i] + num_rows_x_value[i]
        return total_num

    def get_distinct_labels_desc(self, path):
        distinct_labels_json = Tools.read_file(path)
        return distinct_labels_json

    def get_distinct_labels_desc_page_content(self):
        path = os.getcwd() + '/distinct_labels_desc.json'
        post_data = self.get_column_data_by_json(path)
        response = Tools.post_method(TestRow.upload_url, post_data)
        response = json.loads(response)
        options = jsonpath.jsonpath(response, '$..y')[0]


if __name__ == '__main__':
    test = TestRow()
    pytest.main(['-s', 'testRows.py'])
