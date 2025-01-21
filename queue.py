import jenkins
import time
from requests.exceptions import RequestException

# Jenkins server details
JENKINS_URL = 'http://your-jenkins-url'
USERNAME = 'your-username'
PASSWORD = 'your-password'

# Initialize Jenkins server connection
server = jenkins.Jenkins(JENKINS_URL, username=USERNAME, password=PASSWORD)

def get_build_number_from_queue(queue_id, max_retries=5, retry_interval=5):
    """
    Waits for the build number from the queue.
    Handles disconnection and retries in case of errors.
    """
    retries = 0
    while retries < max_retries:
        try:
            # Get the queue item details
            queue_item = server.get_queue_item(queue_id)

            # Check if the queue item has an executable assigned
            if 'executable' in queue_item:
                build_number = queue_item['executable']['number']
                print(f"Build number: {build_number}")
                return build_number

            # If not yet assigned, wait and retry
            print("Build not yet assigned. Retrying...")
            time.sleep(retry_interval)

        except jenkins.JenkinsException as e:
            print(f"JenkinsException occurred: {e}. Retrying...")
        except RequestException as e:
            print(f"RequestException occurred: {e}. Retrying...")

        # Increment retry counter
        retries += 1

    # If max retries are exceeded, raise an exception
    raise Exception(f"Failed to get build number from queue {queue_id} after {max_retries} retries.")

# Example usage
try:
    queue_id = 1234  # Replace with the actual queue ID
    build_number = get_build_number_from_queue(queue_id)
    print(f"Build started with number: {build_number}")
except Exception as e:
    print(f"Error: {e}")