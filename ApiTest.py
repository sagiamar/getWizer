import requests
import unittest
import json

"""tests to check if the the api response usung unittest library"""


## create request to the api with valid input numbers
## the response here is the sum of two numbers
def validInput():
    url = "http://127.0.0.1:5000/calculator"

    payload = "{\n\"num1\": 3,\n\"num2\": 3\n}"
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    r = json.loads(response.text)
    result = r['result']['sum']

    return result


## create request to the api with invalid input numbers
## the response here is error message
def invalidInput():
    url = "http://127.0.0.1:5000/calculator"

    payload = "{\n\"num1\": \"3\",\n\"num2\": 43\n}"
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    r = json.loads(response.text)
    result = r['result']['error']

    return result


def apiHealthCheck():

    url = "http://127.0.0.1:5000/health"
    response = requests.request("GET", url)#, headers=headers, data=payload)
    result = json.loads(response.text)

    return result['health']



class apiTest(unittest.TestCase):
    def test1(self): ## check valid input
        chk = validInput()
        self.assertEqual(chk, 6)

    def test2(self): # check invalid input
        chk = invalidInput()
        self.assertEqual(chk, 'invalid input')

    def test3(self): # api health check
        chk = apiHealthCheck()
        self.assertEqual(chk, 'ok')


if __name__ == '__main__':
    unittest.main()
