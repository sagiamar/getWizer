from flask import Flask, jsonify, request
import sqlite3
from datetime import datetime, date

"""
Flask RestAPI app to sum two numbers and response the result contains two endpoints:
/calculator -> get two numbers in request body json and make the sum
/health -> check the health of the API -> response ok message status code 200 and save the ping time to sqlite DB
"""

health_status = True
app = Flask(__name__)




## save the ping datetime to local sqlite db with status code
def saveToDB(statusCode):
    try:
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        with sqlite3.connect("ping.db") as con:
            cur = con.cursor()
            print(date)
            cur.execute("insert into ping values (?,?)", (dt_string, statusCode))
            con.commit()

    except Exception as err:
        print(err)



## calculator end point get json data from request body
## calculate the sum of two numbers from the json and resoonse json with the result

@app.route("/calculator", methods=["GET", "POST"])

def calculator():

    try:
        invalidNumber = {"error": 'not valid number'}
        request_data = request.get_json() #get json from body
        print(request_data)

        num1 = request_data['num1'] #first number to calculate
        if type(num1) == int or type(num1) == float:
            num2 = request_data['num2']  # second number to calculate
            if type(num2) == int or type(num2) == float:
                try:
                    result = num1 + num2
                except Exception as err:
                    print(err)
            else:
                result = invalidNumber
        else:
            result = invalidNumber

    except Exception as err:
        print(err)

    return {"sum": result}



## make health check and return json with 'ok response and status code 200'
@app.route('/health')
def health():
    if health_status:
        resp = jsonify(health="ok")
        resp.status_code = 200
        saveToDB(200)

    return resp


if __name__ == '__main__':
    app.run(debug=True)


