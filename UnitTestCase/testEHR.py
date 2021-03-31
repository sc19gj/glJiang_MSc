import os
import sys
import pandas as pd
import json
import jsonpath
import requests
import pytest
from UnitTestCase.Tools import Tools
from ehr import Get_data
import function

# datatest, len_data, datatest_make, datatest_make_T, datatest_index, col_list, constancy =   Get_data()
datatest_index = ['distinct' 'num_rows' 'null_values' 'uniqueness']
col_list = ['Provider Name' 'NPI' 'Medicaid_EP_Hospital_Type' 'Specialty'
                 'Business_Street_Address' 'Business_City' 'Business_County'
                 'Business_ZIP_Code' 'Business_State_Territory' 'Program_Year'
                 'Payment_Year' 'Payment_Year_Number' 'Payment_Criteria__Medicaid_Only'
                 'Payee_Name' 'Payee_NPI' 'Disbursement_Amount' 'Total_Payments'
                 'Longitude' 'Latitude']
column_index =['Provider Name, NPI, Medicaid_EP_Hospital_Type, Specialty, Business_Street_Address, Business_City, Business_County, Business_ZIP_Code, Business_State_Territory, Program_Year, Payment_Year, Payment_Year_Number, Payment_Criteria__Medicaid_Only, Payee_Name, Payee_NPI, Disbursement_Amount, Total_Payments, Longitude, Latitude']
class TestEHR:
    url = 'http://127.0.0.1:8050/'
    upload_file = '_dash-update-component'
    upload_url = url + upload_file
    def setup(self):
        pass
    def tearDown(self):
        pass
    def upload_correct_test_data(self, path):

        upload_data = Tools.read_file(path)
        upload_url = TestEHR.upload_url
        response = Tools.post_method(upload_url, upload_data)
        response_dict = json.loads(response )
        up_page = jsonpath.jsonpath(response_dict,"$..props.children")[0]
        print('up_page=', up_page)
        return up_page
    def upload_error_test_data(self, path):
        upload_data = Tools.read_file(path)
        response = Tools.post_method(TestEHR.upload_url, upload_data)
        response_dict = json.loads(response )
        up_page = jsonpath.jsonpath(response_dict, "$..props.children")[0]

    def test_upload_data_correct(self):
        correct_path= os.getcwd() + '/correct_data.json'
        up_page = self.upload_correct_test_data(correct_path)
        assert up_page == 'Your Upload File is SCCUESS'
        return up_page
    def test_datatest(self):
        assert datatest_index== ['distinct' 'num_rows' 'null_values' 'uniqueness']
    def test_col_list(self):
        assert col_list == ['Provider Name' 'NPI' 'Medicaid_EP_Hospital_Type' 'Specialty'
 'Business_Street_Address' 'Business_City' 'Business_County'
 'Business_ZIP_Code' 'Business_State_Territory' 'Program_Year'
 'Payment_Year' 'Payment_Year_Number' 'Payment_Criteria__Medicaid_Only'
 'Payee_Name' 'Payee_NPI' 'Disbursement_Amount' 'Total_Payments'
 'Longitude' 'Latitude']
    def test_column_index(self):
        assert column_index == ['Provider Name, NPI, Medicaid_EP_Hospital_Type, Specialty, Business_Street_Address, Business_City, Business_County, Business_ZIP_Code, Business_State_Territory, Program_Year, Payment_Year, Payment_Year_Number, Payment_Criteria__Medicaid_Only, Payee_Name, Payee_NPI, Disbursement_Amount, Total_Payments, Longitude, Latitude']
if __name__ == '__main__':
    ehr = TestEHR()
    pytest.main(['-s','-W','ignore:Module already imported:pytest.PytestAssertRewriteWarning', 'testEHR.py' ])
