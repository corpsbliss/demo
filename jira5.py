import jenkins
import re
import time
import requests

# Jenkins and Jira configurations
JENKINS_URL = "http://your-jenkins-url"
JENKINS_USER = "your-jenkins-username"
JENKINS_API_TOKEN = "your-jenkins-api-token"

JIRA_URL = "http://your-jira-url"
JIRA_USER = "your-jira-username"
JIRA_API_TOKEN = "your-jira-api-token"

JENKINS_JOB_NAME = "download_snapshot"

# Initialize Jenkins server
server = jenkins.Jenkins(JENKINS_URL, username=JENKINS_USER, password=JENKINS_API_TOKEN)

# Function to trigger Jenkins job
def trigger_jenkins_job(parameters):
    next_build_number = server.get_job_info(JENKINS_JOB_NAME)['nextBuildNumber']
    server.build_job(JENKINS_JOB_NAME, parameters)
    print(f"Triggered Jenkins job: {JENKINS_JOB_NAME}, Build number: {next_build_number}")
    return next_build_number

# Function to wait for Jenkins job to complete
def wait_for_build_to_complete(build_number):
    while True:
        build_info = server.get_build_info(JENKINS_JOB_NAME, build_number)
        if build_info['building']:
            print(f"Build {build_number} is in progress...")
            time.sleep(5)
        else:
            print(f"Build {build_number} completed with result: {build_info['result']}")
            return build_info

# Function to get console output and extract image path
def get_final_image_path(build_number):
    console_output = server.get_build_console_output(JENKINS_JOB_NAME, build_number)
    match = re.search(r"Path of final image: (.+)", console_output)
    if match:
        return match.group(1)
    else:
        print("Final image path not found in console output.")
        return None

# Function to comment on Jira issue
def comment_on_jira(issue_key, comment):
    url = f"{JIRA_URL}/rest/api/2/issue/{issue_key}/comment"
    headers = {"Content-Type": "application/json"}
    payload = {"body": comment}
    response = requests.post(
        url,
        json=payload,
        auth=(JIRA_USER, JIRA_API_TOKEN),
        headers=headers,
    )
    if response.status_code == 201:
        print("Comment added to Jira issue successfully.")
    else:
        print("Failed to comment on Jira issue:", response.text)

# Main execution
def main(jira_issue_key, param1, param2, param3):
    # Trigger Jenkins job with parameters
    jenkins_parameters = {
        "PARAM1": param1,
        "PARAM2": param2,
        "PARAM3": param3,
    }
    build_number = trigger_jenkins_job(jenkins_parameters)

    # Wait for build to complete
    build_info = wait_for_build_to_complete(build_number)

    # Extract final image path
    final_image_path = get_final_image_path(build_number)
    if final_image_path:
        print(f"Final image path: {final_image_path}")

        # Comment the path in Jira
        comment = f"The final image is available at: {final_image_path}"
        comment_on_jira(jira_issue_key, comment)

if __name__ == "__main__":
    # Example inputs
    jira_issue_key = "PROJECT-123"  # Replace with the actual Jira issue key
    param1 = "value1"
    param2 = "value2"
    param3 = "value3"

    main(jira_issue_key, param1, param2, param3)