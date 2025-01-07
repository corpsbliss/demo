import requests

# Jenkins details
jenkins_url = "http://your-jenkins-server"
username = "your-username"
password = "your-password"

# Crumb URL
crumb_url = f"{jenkins_url}/crumbIssuer/api/json"

# Get CSRF crumb
crumb_response = requests.get(crumb_url, auth=(username, password))

if crumb_response.status_code == 200:
    crumb_data = crumb_response.json()
    crumb_field = crumb_data["crumbRequestField"]
    crumb_value = crumb_data["crumb"]
    print("CSRF Crumb fetched successfully.")
else:
    print(f"Failed to fetch crumb. Status code: {crumb_response.status_code}")
    print(crumb_response.text)
    exit()