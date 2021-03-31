import pytest
import sys
import os
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)

import Tools
from testEHR import TestEHR
from testRows import TestRow
from testRowData import TestRowData
datatest_index = ['distinct' 'num_rows' 'null_values' 'uniqueness']
col_list = ['Provider Name' 'NPI' 'Medicaid_EP_Hospital_Type' 'Specialty'
                 'Business_Street_Address' 'Business_City' 'Business_County'
                 'Business_ZIP_Code' 'Business_State_Territory' 'Program_Year'
                 'Payment_Year' 'Payment_Year_Number' 'Payment_Criteria__Medicaid_Only'
                 'Payee_Name' 'Payee_NPI' 'Disbursement_Amount' 'Total_Payments'
                 'Longitude' 'Latitude']
column_index =['Provider Name, NPI, Medicaid_EP_Hospital_Type, Specialty, Business_Street_Address, Business_City, Business_County, Business_ZIP_Code, Business_State_Territory, Program_Year, Payment_Year, Payment_Year_Number, Payment_Criteria__Medicaid_Only, Payee_Name, Payee_NPI, Disbursement_Amount, Total_Payments, Longitude, Latitude']

class testSystem:

    @pytest.mark.run(order=1)
    def test_upload_data_correct(self):
        correct_path= os.getcwd() + '/correct_data.json'
        up_page = TestEHR.upload_correct_test_data(correct_path)
        assert up_page == 'Your Upload File is SCCUESS'

        return up_page

    @pytest.mark.run(order=2)
    def test_column_names(self):
        file_columns_names = TestRow.get_columns_list()
        print('file_columns_names=', file_columns_names)
        path = os.getcwd() + '/row1PostData.json'
        interface_columns_names = TestRow.get_row1_page_content(path)
        print('interface_columns_names=', interface_columns_names)
        length = len(interface_columns_names)
        # print('length=', length)
        assert file_columns_names == interface_columns_names
        total_num = TestRow.count_total_num()

        assert  total_num == length

    @pytest.mark.run(order=3)
    def test_column_values(self):
        column_name = 'Provider Name'
        file_columns_values = TestRow.get_column_datas(column_name)
        path = os.getcwd() + '/providerName_column_values.json'
        interface_columns_values = TestRow.get_column_page_data(path)
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

    @pytest.mark.run(order=5)
    def test_distinct_value_uniqueness(self):
        path = os.getcwd() + '/row3_NPI_post_data.json'
        total_num, distinct_value, uniqueness = TestRowData.get_column_page_data(path)
        assert uniqueness == distinct_value

  
    @pytest.mark.run(order=7)
    def test_datatest(self):
        assert datatest_index== ['distinct' 'num_rows' 'null_values' 'uniqueness']

    @pytest.mark.run(order=8)
    def test_col_list(self):
        assert col_list == ['Provider Name' 'NPI' 'Medicaid_EP_Hospital_Type' 'Specialty'
 'Business_Street_Address' 'Business_City' 'Business_County'
 'Business_ZIP_Code' 'Business_State_Territory' 'Program_Year'
 'Payment_Year' 'Payment_Year_Number' 'Payment_Criteria__Medicaid_Only'
 'Payee_Name' 'Payee_NPI' 'Disbursement_Amount' 'Total_Payments'
 'Longitude' 'Latitude']

    @pytest.mark.run(order=9)
    def test_column_index(self):
        assert column_index == ['Provider Name, NPI, Medicaid_EP_Hospital_Type, Specialty, Business_Street_Address, Business_City, Business_County, Business_ZIP_Code, Business_State_Territory, Program_Year, Payment_Year, Payment_Year_Number, Payment_Criteria__Medicaid_Only, Payee_Name, Payee_NPI, Disbursement_Amount, Total_Payments, Longitude, Latitude']


if __name__ == '__main__':
    pytest.main(['-s', 'testSystem.py'])
    pytest.main(['-s','-W','ignore:Module already imported:pytest.PytestWarning', 'testRowData.py'])
    #
    pytest.main(['-s','-W','ignore:Module already imported:pytest.PytestWarning','testRows.py'])
    pytest.main(['-s','-W','ignore:Module already imported:pytest.PytestWarning','testFileType.py'])
