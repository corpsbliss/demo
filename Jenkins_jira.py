import time
import jenkins
import requests
from requests.auth import HTTPBasicAuth

# Jenkins server details
JENKINS_URL = 'http://54.152.54.80:8080'  # Replace with your Jenkins server URL
USERNAME = 'myuser'                       # Replace with your Jenkins username
PASSWORD = 'mypassword'                   # Replace with your Jenkins password or API token

# Jira server details
JIRA_URL = 'https://your-jira-instance.atlassian.net'  # Replace with your Jira URL
JIRA_USER = 'your-email@example.com'  # Replace with your Jira email (used for basic auth)
JIRA_API_TOKEN = 'your-jira-api-token'  # Replace with your Jira API token

# Jenkins Job Name
JOB_NAME = 'seret-image'                  # Replace with the name of your Jenkins job

# Polling interval (seconds)
POLL_INTERVAL = 60  # Poll every 60 seconds

# Jira transition ID for "Done" status
DONE_TRANSITION_ID = '31'  # Replace with the actual ID for transitioning a ticket to "Done"

# Cache to store processed ticket IDs
processed_tickets = set()

def poll_jira_for_new_tickets():
    """
    Poll Jira for new tickets that meet the condition, trigger Jenkins job, and update the ticket.
    """
    while True:
        print("Polling Jira for new tickets...")

        # Jira API endpoint for searching issues (can be customized with JQL)
        jql_query = 'project = "OPS" AND summary ~ "seret-image" AND status != "Done"'
        url = f"{JIRA_URL}/rest/api/2/search?jql={jql_query}"

        headers = {'Content-Type': 'application/json'}
        auth = HTTPBasicAuth(JIRA_USER, JIRA_API_TOKEN)

        try:
            response = requests.get(url, headers=headers, auth=auth)

            if response.status_code == 200:
                data = response.json()
                issues = data.get('issues', [])

                if issues:
                    print(f"Found {len(issues)} ticket(s) matching criteria.")
                    for issue in issues:
                        ticket_id = issue['key']
                        summary = issue['fields']['summary']
                        description = issue['fields']['description']

                        # Skip already processed tickets
                        if ticket_id in processed_tickets:
                            continue

                        print(f"Processing ticket: {ticket_id} - {summary}")

                        # Trigger Jenkins job
                        trigger_jenkins_job(ticket_id, description)

                        # Mark the ticket as processed
                        processed_tickets.add(ticket_id)
                else:
                    print("No new tickets found.")

            else:
                print(f"Failed to fetch Jira tickets. Status Code: {response.status_code}")
                print(response.text)

        except Exception as e:
            print(f"Error polling Jira: {e}")

        # Wait before polling again
        print(f"Waiting for {POLL_INTERVAL} seconds before polling again...\n")
        time.sleep(POLL_INTERVAL)

def trigger_jenkins_job(ticket_id, description):
    """
    Trigger Jenkins job for the given ticket.
    """
    try:
        # Create a Jenkins server connection
        server = jenkins.Jenkins(JENKINS_URL, username=USERNAME, password=PASSWORD)

        # Build parameters
        job_params = {
            'image_type': description  # Passing the Jira ticket description as the build parameter
        }

        print(f"Triggering Jenkins job '{JOB_NAME}' for ticket '{ticket_id}'...")

        # Trigger the job
        server.build_job(JOB_NAME, parameters=job_params)

        # Monitor job status
        monitor_jenkins_job(server, ticket_id)
    except jenkins.JenkinsException as e:
        print(f"Failed to connect to Jenkins: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def monitor_jenkins_job(server, ticket_id):
    """
    Monitor the Jenkins job status and update Jira ticket once the job is finished.
    """
    # Fetch the latest build number
    job_info = server.get_job_info(JOB_NAME)
    latest_build_number = job_info['lastBuild']['number']

    # Check the status of the latest build
    build_info = server.get_build_info(JOB_NAME, latest_build_number)

    if build_info['result'] == 'SUCCESS':
        build_status = 'SUCCESS'
    else:
        build_status = 'FAILURE'

    print(f"Build status for ticket {ticket_id}: {build_status}")

    # Comment on the Jira ticket
    comment_on_jira_ticket(ticket_id, build_status)

    # Change Jira ticket status to "Done"
    transition_jira_ticket_to_done(ticket_id)

def comment_on_jira_ticket(ticket_id, build_status):
    """
    Comment on the Jira ticket with the build status.
    """
    # Jira API endpoint for adding a comment to a ticket
    url = f"{JIRA_URL}/rest/api/2/issue/{ticket_id}/comment"

    # Prepare the comment text
    comment = f"Build status of Jenkins job '{JOB_NAME}': {build_status}."

    # Authentication and headers for Jira API
    headers = {
        'Content-Type': 'application/json'
    }
    auth = HTTPBasicAuth(JIRA_USER, JIRA_API_TOKEN)

    data = {
        'body': comment
    }

    try:
        # Make the request to Jira to add a comment
        response = requests.post(url, json=data, headers=headers, auth=auth)

        if response.status_code == 201:
            print(f"Comment added to Jira ticket {ticket_id} successfully!")
        else:
            print(f"Failed to add comment to Jira ticket. Status Code: {response.status_code}")
            print(response.text)

    except Exception as e:
        print(f"Error commenting on Jira ticket {ticket_id}: {e}")

def transition_jira_ticket_to_done(ticket_id):
    """
    Transition the Jira ticket to "Done" status.
    """
    # Jira API endpoint for transitioning an issue
    url = f"{JIRA_URL}/rest/api/2/issue/{ticket_id}/transitions"

    headers = {'Content-Type': 'application/json'}
    auth = HTTPBasicAuth(JIRA_USER, JIRA_API_TOKEN)

    data = {
        'transition': {
            'id': DONE_TRANSITION_ID  # The transition ID for "Done" status
        }
    }

    try:
        # Make the request to Jira to transition the ticket
        response = requests.post(url, json=data, headers=headers, auth=auth)

        if response.status_code == 204:
            print(f"Ticket {ticket_id} transitioned to 'Done' successfully!")
        else:
            print(f"Failed to transition ticket {ticket_id} to 'Done'. Status Code: {response.status_code}")
            print(response.text)

    except Exception as e:
        print(f"Error transitioning Jira ticket {ticket_id} to 'Done': {e}")

# Start the polling process
poll_jira_for_new_tickets()