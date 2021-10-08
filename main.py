from flask import Flask, jsonify, request
import sqlite3
from datetime import datetime, date

"""
Flask RestAPI app to sum two numbers and response the result contains two endpoints:
/calculator -> get two numbers in request body json and make the sum
/health -> check the health of the API -> response ok message status code 200 and save the ping time to sqlite DB
"""

"""
example for input values:
{
   "num1": 3,
   "num2": 43
}
"""


health_status = True
app = Flask(__name__)


## save the ping datetime to local sqlite db with status code
def saveToDB(statusCode):
    try:
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        with sqlite3.connect("pingDB.db") as con:
            cur = con.cursor()
            cur.execute("insert into pingDB values (?,?)", (dt_string, statusCode))
            con.commit()

    except Exception as err:
        print(err)


def validateInput(input1, input2):
    validate = False
    if type(input1) == int or type(input1) == float:
        if type(input2) == int or type(input2) == float:
            validate = True
        else:
            validate = False
    else:
        validate = False
    return validate


## calculator end point get json data from request body
## calculate the sum of two numbers from the json and resoonse json with the result

@app.route("/calculator", methods=["POST"])

def calculator():


    invalidNumber = {'result': {'error': 'invalid input'}}
    request_data = request.get_json() #get json from body

    num1 = request_data['num1'] #first number to calculate
    num2 = request_data['num2']  # second number to calculate

    input = validateInput(num1, num2)

    if input == True:

        result = {'result': {'sum': num1 + num2}}  ## input cpntains two valid values

    else:
        return invalidNumber

    return result




## make health check and return json with 'ok response and status code 200'
@app.route('/health', methods=["GET"])
def health():
    if health_status:
        resp = jsonify(health="ok")
        resp.status_code = 200
        saveToDB(200)

    return resp


if __name__ == '__main__':
    app.run(debug=True)


