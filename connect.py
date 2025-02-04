import requests
from requests.auth import HTTPBasicAuth

# Replace with your Jira Server details
JIRA_URL = "https://your-jira-server.com"
USERNAME = "your-email@example.com"
PASSWORD = "your-password"

# Jira API endpoint for testing connection
TEST_ENDPOINT = f"{JIRA_URL}/rest/api/2/myself"

# Send GET request to Jira API with basic authentication
response = requests.get(TEST_ENDPOINT, auth=HTTPBasicAuth(USERNAME, PASSWORD))

# Check response
if response.status_code == 200:
    print("Jira connection successful!")
    print("User details:", response.json())
else:
    print(f"Failed to connect to Jira. Status Code: {response.status_code}")
    print("Response:", response.text)