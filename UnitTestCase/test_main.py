import pytest
import sys
import os
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)
import ehr
import function
from UnitTestCase.Tools import Tools
from UnitTestCase.testEHR import TestEHR
from UnitTestCase.testRows import TestRow
from UnitTestCase.testRowData import TestRowData

datatest_index = ['distinct' 'num_rows' 'null_values' 'uniqueness']
col_list = ['Provider Name' 'NPI' 'Medicaid_EP_Hospital_Type' 'Specialty'
                 'Business_Street_Address' 'Business_City' 'Business_County'
                 'Business_ZIP_Code' 'Business_State_Territory' 'Program_Year'
                 'Payment_Year' 'Payment_Year_Number' 'Payment_Criteria__Medicaid_Only'
                 'Payee_Name' 'Payee_NPI' 'Disbursement_Amount' 'Total_Payments'
                 'Longitude' 'Latitude']
column_index =['Provider Name, NPI, Medicaid_EP_Hospital_Type, Specialty, Business_Street_Address, Business_City, Business_County, Business_ZIP_Code, Business_State_Territory, Program_Year, Payment_Year, Payment_Year_Number, Payment_Criteria__Medicaid_Only, Payee_Name, Payee_NPI, Disbursement_Amount, Total_Payments, Longitude, Latitude']

print(sys.getdefaultencoding())
class testMain:

    # Unit Test Case: Used to test whether the output result of the specified method in the EHR, Function file is correct
    @pytest.mark.run(order=1)
    def test_datatest(self):
        datatest, len_data, datatest_make, datatest_make_T, datatest_index, col_list, constancy = TestEHR.get_ehr_response()

        assert datatest_index== ['distinct' 'num_rows' 'null_values' 'uniqueness']

    @pytest.mark.run(order=2)
    def test_col_list(self):
        datatest, len_data, datatest_make, datatest_make_T, datatest_index, col_list, constancy = TestEHR.get_ehr_response()


        assert col_list == ['Provider Name' 'NPI' 'Medicaid_EP_Hospital_Type' 'Specialty'
                            'Business_Street_Address' 'Business_City' 'Business_County'
                            'Business_ZIP_Code' 'Business_State_Territory' 'Program_Year'
                            'Payment_Year' 'Payment_Year_Number' 'Payment_Criteria__Medicaid_Only'
                            'Payee_Name' 'Payee_NPI' 'Disbursement_Amount' 'Total_Payments'
                            'Longitude' 'Latitude']

    @pytest.mark.run(order=3)
    def test_column_index(self):
        datatest, len_data, datatest_make, datatest_make_T, datatest_index, col_list, constancy = TestEHR.get_ehr_response()

        assert column_index == [
            'Provider Name, NPI, Medicaid_EP_Hospital_Type, Specialty, Business_Street_Address, Business_City, Business_County, Business_ZIP_Code, Business_State_Territory, Program_Year, Payment_Year, Payment_Year_Number, Payment_Criteria__Medicaid_Only, Payee_Name, Payee_NPI, Disbursement_Amount, Total_Payments, Longitude, Latitude']


    @pytest.mark.run(order = 4)
    def test_distributions(self):
        constancy = TestEHR.get_distributions_response()
        assert  constancy == [0.05263157894736842, 0.3684210526315789, 0.3684210526315789, 0.3684210526315789]


    # Integration test case: Verify that the uploaded file result returns SUCCESS, if it returns, the test passes, otherwise the test fails
    @pytest.mark.run(order=5)
    def test_upload_data_correct(self):
        correct_path= os.getcwd() + '/correct_data.json'
        up_page = TestEHR.upload_correct_test_data(correct_path)
        assert up_page == 'Your Upload File is SCCUESS'

        return up_page

    #Gets whether the value in the first drop-down list on the page is the same as the column value in the CSV file
    @pytest.mark.run(order=6)
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

    # Gets whether the value in the drop-down list under the specified column value on the page is the same as the column value in the CSV file
    @pytest.mark.run(order=7)
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

    # Select whether the value in the drop-down list on the left is the same as the equivalent of the uniqueness, distinct_value, and total_num returned in the drop-down list on the right
    @pytest.mark.run(order=8)
    def test_distinct_value_uniqueness(self):
        path = os.getcwd() + '/row3_NPI_post_data.json'
        total_num, distinct_value, uniqueness = TestRowData.get_column_page_data(path)
        path2 = os.getcwd() + '/row3_NPI2_post_data.json'
        total_num2, distinct_value2, uniqueness2 = TestRowData.get_column_page_data2(path2)
        assert uniqueness == uniqueness2
        assert distinct_value == distinct_value2
        assert total_num == total_num2



if __name__ == '__main__':
    pytest.main(['-s','-W','ignore:Module already imported:pytest.PytestAssertRewriteWarning', 'test_main.py'])
