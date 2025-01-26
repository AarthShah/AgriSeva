from flask import Flask, render_template, request, jsonify
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential

app = Flask(__name__, template_folder='.')

# Azure Text Analytics credentials
language_key = 'EhrvRaDEqtQpb39URQsEFpsTUwlkK2HODcsvYYKRooEKKnDxOzghJQQJ99BAAC1i4TkXJ3w3AAAaACOGm4nE'
language_endpoint = 'https://aagrisevaproject.cognitiveservices.azure.com/'

# Authenticate Azure Text Analytics client
def authenticate_client():
    ta_credential = AzureKeyCredential(language_key)
    return TextAnalyticsClient(endpoint=language_endpoint, credential=ta_credential)

client = authenticate_client()

# Analyze feedback
def analyze_feedback(feedback):
    documents = [feedback]
    response = client.analyze_sentiment(documents=documents)
    sentiment = response[0].sentiment
    return sentiment

# Route for home page
@app.route('/')
def index():
    return render_template('index.html')

# Route for feedback analysis
@app.route('/analyze', methods=['POST'])
def analyze():
    feedback = request.form['feedback']
    sentiment = analyze_feedback(feedback)
    return jsonify({'sentiment': sentiment})

if __name__ == '__main__':
    app.run(debug=True)