import os
import sys
import pytest
import difflib
import json
import jsonpath
import pandas as pd

from Tools import Tools
class TestFileType:
    url = 'http://127.0.0.1:8050/'
    upload_file = '_dash-update-component'
    upload_url = url + upload_file

    def compare_json_files(self, file1Path, file2Path):
        json1 = Tools.read_file(file1Path)
        json2 = Tools.read_file(file2Path)

        # Read correct_data.json and error_data.json from correct_data.json
        # Json file containing the correct_data.json file containing the correct request parameter values.
        #Error_data. json contains content with request parameter values for the error file
        # Compare the contents of the two files, if there is a difference, the uploaded file content is wrong, then the program should report an error
        Flag = False
        for my_key in json1.keys():
            value_eval = json1[str(my_key)]
            value_test = json2[str(my_key)]
            diff = difflib.SequenceMatcher(None, value_eval, value_test).quick_ratio()
            if diff != None:
                """ Compare the contents of two files, if there is a difference, the uploaded file content is wrong, 
	then the program should report an error to compare the contents of two files whether there is a difference, 
	if there is a difference, the uploaded file is not correct"""
                Flag = True

                break
        print('Flag=', Flag)
        return Flag

    # @pytest.mark.run(order=10)
    def test_file_content_type(self):
        error_path = os.getcwd() + '/error_data.json'
        upload_url = TestFileType.upload_url
        upload_data = Tools.read_file(error_path)

        response = Tools.post_method(upload_url, upload_data)
        correct_path = os.getcwd() + '/correct_data.json'

        Flag = self.compare_json_files(correct_path, error_path)
        print('Flag=', Flag)
        assert Flag == False

if __name__ == '__main__':
    pytest.main(['-s', 'testFileType.py'])