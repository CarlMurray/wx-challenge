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
  "userId": "user_12345",
  "userName": "john_doe",
  "firstName": "John",
  "lastName": "Doe",
  "email": "john.doe@ibm.com",
  "phone": "+1-555-123-4567",
  "title": "Data Analyst",
  "department": {
    "departmentName": "Data Analytics",
    "manager": {
      "managerId": "user_67890",
      "managerName": "Thomas Watson",
      "managerTitle": "Director of Data Analytics",
      "managerEmail": "thomas.watson@ibm.com"
    }
  },
  "location": {
    "office": "New York Office",
    "address": {
      "street": "1234 5th Avenue",
      "city": "New York",
      "state": "NY",
      "postalCode": "10001",
      "country": "USA"
    }
  },
  "employment": {
    "employeeId": "emp_54321",
    "employmentType": "Full-time",
    "hireDate": "2020-05-01",
    "endDate": "null"
  },
  "accessDetails": {
    "roles": ["Data Analyst", "Sensitive Data Access"],
    "lastLogin": "2024-07-15T08:00:00Z",
    "failedLoginAttempts": 2,
    "activeSessions": 1
  },
  "projects": [
    {
      "projectId": "proj_1122",
      "projectName": "Customer Insights Analysis",
      "role": "Lead Data Analyst",
      "startDate": "2023-01-01",
      "endDate": "null"
    },
    {
      "projectId": "proj_3344",
      "projectName": "Marketing Data Cleanup",
      "role": "Data Analyst",
      "startDate": "2022-09-01",
      "endDate": "2023-01-01"
    }
  ],
  "training": [
    {
      "trainingId": "train_5678",
      "trainingName": "Data Privacy and Security",
      "completionDate": "2024-06-15"
    },
    {
      "trainingId": "train_91011",
      "trainingName": "Advanced SQL for Data Analysts",
      "completionDate": "2023-11-20"
    }
  ],

  "risk_event": {
    "risk_id": 24,
    "classification": "sql_injection",
    "classification_nls": "SQL Injection",
    "severity": 69,
    "severity_level": "HIGH",
    "pivot": {
      "type": "DB_USER",
      "id": "9.46.87.164;DATABASE6;CINDEE",
      "db_user": "CINDEE",
      "database": "DATABASE6",
      "server_ip": "9.46.87.164",
      "database_source_field": "DATABASE_NAME"
    },
    "short_observations": [
      {
        "type": "VIOLATION",
        "count": 3
      }
    ],
    "from_date": "2024-07-09T09:00:00Z",
    "to_date": "2024-07-09T19:00:00Z",
    "status": "OPENED",
    "description": "In the last day, there were 255 violations of the \"SQL Injection: Tautology\" policy rule.\n",
    "category_description": "SQL injection attacks attempt to use application vulnerabilities by concatenating user input with SQL queries. If successful, these attacks can run malicious SQL commands by using the legitimate application connection. There are various SQL injection techniques. Explore policy violations and exceptions to understand which techniques, suggesting an SQL injection, were identified.",
    "categorization_confidence": 0.7403198
  },
  "observations": [
    {
      "observation_id": 1,
      "lead_feature_id": 26,
      "time": "2024-07-09T09:00:00Z",
      "observation_description": "86 violations with severity 10 or higher",
      "observation_type": "VIOLATION"
    },
    {
      "observation_id": 2,
      "lead_feature_id": 46,
      "time": "2024-07-09T11:00:00Z",
      "observation_description": "86 violations with severity 10 or higher",
      "observation_type": "VIOLATION"
    },
    {
      "observation_id": 3,
      "lead_feature_id": 77,
      "time": "2024-07-09T18:00:00Z",
      "observation_description": "86 violations with severity 10 or higher",
      "observation_type": "VIOLATION"
    }
  ]
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
INSTRUCTION = """<|begin_of_text|><|start_header_id|>system<|end_header_id|>

Write a summary of the provided JSON data, which includes information about a risk event and the associated user from Workday. The summary should be easy to read and use bullet points to highlight key points. Based on the data and context from Workday, suggest possible explanations for the risk event. Make sure you are clear on what part of the data led you to those explanations and why you think those explanations are possible. 

Your output should include a high level overview of the most important data points but make sure to include important contextual information which would help a security analyst assess a threat, such as the employees experience, start date or holiday status. 

Your output must also include a "Possible explanations" section which provides possible explanations for the risk event, which have been inferred by the data provided and are based on the data. Also include a Recommended Next Steps section.<|eot_id|><|start_header_id|>assistant<|end_header_id|>

"""

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
	  "model_id": LLAMA_3_INSTRUCT,
    #   "input": (INSTRUCTION+ "<|start_header_id|>user<|end_header_id|>"+jsondata["input"]+"<|eot_id|><|start_header_id|>assistant<|end_header_id|>"), 
    #   "input": (INSTRUCTION+user_context_data_string),
        "input":INSTRUCTION + "<|start_header_id|>user<|end_header_id|>"+ user_context_data_string + "<|eot_id|><|start_header_id|>assistant<|end_header_id|>",
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
    email = user_context_data["department"]["manager"]["managerEmail"]
    print(email)
    dict = {"summary": summary, "email": email, "subject": "Security Event Summary from watsonx"}
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
