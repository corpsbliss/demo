import requests

# GitHub Personal Access Token (required for authentication)
GITHUB_TOKEN = "your_github_token"

# GitHub Repository details
OWNER = "repository_owner"  # e.g., 'octocat'
REPO = "repository_name"    # e.g., 'Hello-World'
BRANCH = "main"             # Replace with your branch name

# API Endpoint to fetch the branch information
url = f"https://api.github.com/repos/{OWNER}/{REPO}/commits/{BRANCH}"

# Headers for the request
headers = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}

try:
    # Make a GET request to the GitHub API
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # Raise an error for bad responses

    # Parse the JSON response
    data = response.json()
    commit_id = data.get("sha")  # Get the commit ID (SHA hash)

    if commit_id:
        print(f"Latest Commit ID for branch '{BRANCH}': {commit_id}")
    else:
        print("Unable to fetch commit ID.")

except requests.exceptions.RequestException as e:
    print(f"Error fetching commit ID: {e}")