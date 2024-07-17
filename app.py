from flask import Flask

app = Flask(__name__)

@app.route("/workday/api/get_user_context")
def get_user_context():
    print("app is running")
    return {
        "fname": "John",
        "lname": "Doe",
        "email": "john.doe@ibm.com",
        "employeeId": "192844",
        "startDate": "2024-02-01",
        "isOnHoliday": "true",
        "holidayStartDate": "2024-06-20",
        "holidayEndDate": "2024-06-27",
        "manager": {
            "fname": "Thomas",
            "lname": "Watson",
            "email": "thomas.watson@ibm.com"
        }
    }

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
