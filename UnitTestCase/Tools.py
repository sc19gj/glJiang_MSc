import requests
import json
url = 'http://127.0.0.1:8050/'
upload_file = '_dash-update-component'
upload_url = url + upload_file
class Tools:
    @classmethod
    def post_method(cls, url, data):
        header = {"Content-Type": "application/json"}
        response = requests.post(url=url, headers=header, json=data)
        print('response=', response.text)

        return response.text
    @classmethod
    def post_method2(cls, url, data):
        header = {"Content-Type": "application/json"}
        response = requests.post(url=url, headers=header, json=data)
        print('response=', response.text)

        return response
    @classmethod
    def read_file(cls, path):
        # json.load reads the file and turns the contents of the file into Python objects

        with open( path, 'r') as f:
            s1 = json.load(f)
            return s1


if __name__ == '__main__':
    t = Tools()
    t.read_file('C:/Users/Martin/Desktop/1616489534572_testing/testing/UnitTestCase/row1PostData.json')