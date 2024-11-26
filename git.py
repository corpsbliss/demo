import requests

def get_commits(owner, repo, token):
    """
    Fetches the list of all commits in a GitHub repository.

    :param owner: Repository owner (e.g., 'octocat')
    :param repo: Repository name (e.g., 'Hello-World')
    :param token: Personal access token for authentication
    :return: List of commits
    """
    url = f"https://api.github.com/repos/{owner}/{repo}/commits"
    headers = {"Authorization": f"Bearer {token}"}
    commits = []
    page = 1

    while True:
        # Paginate through results
        response = requests.get(url, headers=headers, params={"page": page, "per_page": 100})
        if response.status_code != 200:
            print(f"Failed to fetch commits: {response.status_code} - {response.text}")
            break

        data = response.json()
        if not data:  # Stop if no more commits are returned
            break

        commits.extend(data)
        page += 1

    return commits


if __name__ == "__main__":
    # Replace these with your repository details and token
    GITHUB_OWNER = "octocat"  # Repository owner
    GITHUB_REPO = "Hello-World"  # Repository name
    GITHUB_TOKEN = "your_personal_access_token"  # Personal Access Token

    commits = get_commits(GITHUB_OWNER, GITHUB_REPO, GITHUB_TOKEN)
    
    print(f"Total commits found: {len(commits)}")
    for commit in commits:
        sha = commit.get("sha")
        message = commit["commit"]["message"]
        author = commit["commit"]["author"]["name"]
        date = commit["commit"]["author"]["date"]
        print(f"{sha}: {message} by {author} on {date}")