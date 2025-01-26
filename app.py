from flask import Flask, request, render_template
from flask_cors import CORS
import requests

# Initialize the Flask app
app = Flask(__name__)

# Enable CORS for all routes
CORS(app)

# Azure service configuration
azure_endpoint = "https://chatbotruby.cognitiveservices.azure.com/language/:query-knowledgebases?projectName=Ruby&api-version=2021-10-01&deploymentName=production"
subscription_key = "69h1lSNG0RNUp48aHD5u4aSJp1Z47IESya7oDsk9z3WggyQ6HPMEJQQJ99BAACHYHv6XJ3w3AAAaACOGkXLC"

# Route to serve the HTML file
@app.route('/')
def index():
    return render_template('index.html')  # Serve the HTML file from the 'templates' folder

@app.route('/ask-bot', methods=['POST'])
def ask_bot():
    data = request.json
    question = data['question']

    headers = {
        "Ocp-Apim-Subscription-Key": subscription_key,
        "Content-Type": "application/json"
    }

    payload = {
        "top": 3,
        "question": question,
        "includeUnstructuredSources": True,
    }

    response = requests.post(azure_endpoint, headers=headers, json=payload)
    
    # Parse the response
    azure_response = response.json()
    
    # Extract only the first answer
    if "answers" in azure_response and len(azure_response["answers"]) > 0:
        answer = azure_response["answers"][0].get("answer", "No answer found.")
    else:
        answer = "No answer found."
    
    # Return only the answer as plain text
    return answer

if __name__ == '__main__':
    app.run(debug=True)
