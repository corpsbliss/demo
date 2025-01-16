import time
import jenkins
import requests

# Jenkins server configuration
JENKINS_URL = "http://your-jenkins-server"
USERNAME = "your-username"
PASSWORD = "your-password"
JOB_NAME = "your-job-name"

# Function to wait for the build to complete
def wait_for_build(jenkins_server, job_name, build_number, max_retries=5):
    retry_count = 0
    backoff_time = 2  # Start with 2 seconds

    while retry_count < max_retries:
        try:
            # Check the build status
            build_info = jenkins_server.get_build_info(job_name, build_number)
            if build_info['building']:
                print("Build in progress, waiting...")
                time.sleep(10)  # Poll every 10 seconds
            else:
                print("Build completed!")
                return build_info
        except (jenkins.JenkinsException, requests.exceptions.RequestException) as e:
            print(f"Connection issue: {e}")
            retry_count += 1
            print(f"Retrying in {backoff_time} seconds...")
            time.sleep(backoff_time)
            backoff_time *= 2  # Exponential backoff

    raise Exception("Max retries reached. Unable to connect to Jenkins server.")

def main():
    try:
        # Connect to Jenkins
        server = jenkins.Jenkins(JENKINS_URL, username=USERNAME, password=PASSWORD)
        print("Connected to Jenkins.")

        # Trigger the build
        build_number = server.get_job_info(JOB_NAME)['nextBuildNumber']
        server.build_job(JOB_NAME)
        print(f"Triggered build #{build_number} for job {JOB_NAME}.")

        # Wait for the build to complete
        build_info = wait_for_build(server, JOB_NAME, build_number)
        print("Build result:", build_info['result'])
    except Exception as e:
        print("An error occurred:", e)

if __name__ == "__main__":
    main()