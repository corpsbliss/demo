import requests

def get_commits_with_changes(owner, repo, token):
    """
    Fetches a list of commits with their modified file paths and commit messages.

    :param owner: Repository owner (e.g., 'octocat')
    :param repo: Repository name (e.g., 'Hello-World')
    :param token: Personal access token for authentication
    """
    commits_url = f"https://api.github.com/repos/{owner}/{repo}/commits"
    headers = {"Authorization": f"Bearer {token}"}
    page = 1

    while True:
        # Get paginated commit data
        response = requests.get(commits_url, headers=headers, params={"page": page, "per_page": 10})
        if response.status_code != 200:
            print(f"Failed to fetch commits: {response.status_code} - {response.text}")
            break

        commits = response.json()
        if not commits:  # Stop if no more commits are returned
            break

        for commit in commits:
            commit_id = commit.get("sha")
            commit_message = commit["commit"]["message"]
            commit_details_url = f"https://api.github.com/repos/{owner}/{repo}/commits/{commit_id}"

            # Fetch detailed commit data to get file paths
            details_response = requests.get(commit_details_url, headers=headers)
            if details_response.status_code != 200:
                print(f"Failed to fetch details for commit {commit_id}: {details_response.status_code}")
                continue

            details = details_response.json()
            files = details.get("files", [])
            file_paths = [file["filename"] for file in files]

            # Print commit ID, message, and modified file paths
            print(f"Commit ID: {commit_id}")
            print(f"Message: {commit_message}")
            print("Modified Files:")
            for path in file_paths:
                print(f" - {path}")
            print("-" * 40)

        page += 1


if __name__ == "__main__":
    # Replace these with your repository details and token
    GITHUB_OWNER = "octocat"  # Repository owner
    GITHUB_REPO = "Hello-World"  # Repository name
    GITHUB_TOKEN = "your_personal_access_token"  # Personal Access Token

    get_commits_with_changes(GITHUB_OWNER, GITHUB_REPO, GITHUB_TOKEN)