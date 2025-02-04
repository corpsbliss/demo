import requests
import base64

JIRA_URL = "https://your-domain.atlassian.net"
EMAIL = "your-email@example.com"
API_TOKEN = "your-api-token"

# Encode credentials manually
auth_string = f"{EMAIL}:{API_TOKEN}".encode("utf-8")
auth_header = base64.b64encode(auth_string).decode("utf-8")

# Set headers
headers = {
    "Authorization": f"Basic {auth_header}",
    "Accept": "application/json"
}

# Jira API endpoint for testing connection
TEST_ENDPOINT = f"{JIRA_URL}/rest/api/3/myself"

# Send GET request with headers
response = requests.get(TEST_ENDPOINT, headers=headers)

# Check response
if response.status_code == 200:
    print("✅ Jira connection successful!")
    print("User details:", response.json())
elif response.status_code == 401:
    print("❌ Error 401: Unauthorized - Check API token, email, and domain URL.")
else:
    print(f"❌ Failed to connect to Jira. Status Code: {response.status_code}")
    print("Response:", response.text)