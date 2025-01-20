import requests
import re
import time

# Define constants
URL = "https://example.com"  # Replace with the target webpage URL
STATIC_PART = "https://staticpart.com/"  # Replace with the static part of the URL you're looking for
CHECK_INTERVAL = 600  # Check every 10 minutes (600 seconds)

def check_webpage():
    try:
        # Fetch the webpage
        response = requests.get(URL)
        response.raise_for_status()  # Raise an error if the request failed
        content = response.text

        # Search for the URL with the static part
        pattern = re.compile(rf"{re.escape(STATIC_PART)}[\w/-]+")
        match = pattern.search(content)

        if match:
            print(f"URL found: {match.group(0)}")
        else:
            print("URL not found.")

    except requests.RequestException as e:
        print(f"Error fetching webpage: {e}")

# Main loop
if __name__ == "__main__":
    while True:
        print("Checking webpage...")
        check_webpage()
        print(f"Waiting for {CHECK_INTERVAL // 60} minutes...\n")
        time.sleep(CHECK_INTERVAL)