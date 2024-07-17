from flask import Flask, render_template
from flask_cors import CORS
import requests
import json
import markdown
from flask import request

app = Flask(__name__)
CORS(app)

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
    
# Models
GRANITE_CHAT = "ibm/granite-13b-chat-v2"
GRANITE_INSTRUCT = "ibm/granite-13b-instruct-v2"
LLAMA_3_INSTRUCT = "meta-llama/llama-3-70b-instruct"
LLAMA_2_CHAT = "meta-llama/llama-2-70b-chat"
MIXTRAL_INSTRUCT = "mistralai/mixtral-8x7b-instruct-v01"

# Model parameters
MAX_NEW_TOKENS = 2500
MIN_NEW_TOKENS = 200
REPETITION_PENALTY = 1

# API_KEY=os.environ.get("API_KEY")
API_KEY='BGthpi04Zy0luvLxtPhGvYqspGYSpU1Ae_sjOXF2MShX'
API_URL_ENDPOINT = "https://us-south.ml.cloud.ibm.com/ml/v1/text/generation?version=2024-06-01"
INSTRUCTION = """You are a security AI assistant. You will take the JSON data about an employee and generate a human readable summary of the data."""

@app.route("/")
def index():
    return render_template("risk-event.html")

@app.route("/workday/api/get_user_context")
def summarise():
    token = get_iam_token()
    user_context_data = get_user_context()
    user_context_data_string = json.dumps(user_context_data)
    headers = {"Authorization": f'Bearer {token}', 
                       "content-type":"application/json"}
    data = {
	  "model_id": MIXTRAL_INSTRUCT,
    #   "input": (INSTRUCTION+ "<|start_header_id|>user<|end_header_id|>"+jsondata["input"]+"<|eot_id|><|start_header_id|>assistant<|end_header_id|>"),
      "input": (INSTRUCTION+user_context_data_string),
      "project_id": "fc373787-aaaa-4622-93df-65e71b0a579f",
      	"parameters": {
		"decoding_method": "greedy",
		"max_new_tokens": MAX_NEW_TOKENS,
		"repetition_penalty": REPETITION_PENALTY,
        "stop_sequences": [],
	    },
    }
    r = requests.post(url=API_URL_ENDPOINT, json=data, headers=headers)
    jsondata = r.json()
    summary = jsondata["results"][0]["generated_text"]
    # summary = json.dumps(jsondata["results"][0]["generated_text"])
    # print(summary)
    email = user_context_data["manager"]["email"]
    print(email)
    dict = {"summary": summary, "email": email}
    return json.dumps(dict)

def get_iam_token():
    url = 'https://iam.cloud.ibm.com/identity/token'
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    data = f'grant_type=urn:ibm:params:oauth:grant-type:apikey&apikey={API_KEY}'
    r = requests.post(url=url, data=data, headers=headers)
    token = r.json()
    token = token["access_token"]
    return token

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
