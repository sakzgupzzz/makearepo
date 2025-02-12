import subprocess
import sys
import requests
import getpass  # For secure token input

# Ensure required dependencies are installed
def install_dependencies():
    try:
        import requests  # Check if requests is installed
    except ImportError:
        print("📦 'requests' module not found. Installing now...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "requests"])

# Install dependencies before proceeding
install_dependencies()

def get_user_inputs():
    """Prompts the user for required GitHub inputs."""
    print("\n📢 This script will create a GitHub repository.")
    print("\n❗ You DO NOT need to enter a username because the Personal Access Token (PAT) handles authentication.")
    print("\n👉 To generate a Personal Access Token (PAT):")
    print("   1️⃣ Go to https://github.com/settings/tokens")
    print("   2️⃣ Click 'Generate new token (classic)'")
    print("   3️⃣ Select the 'repo' scope for full repository access")
    print("   4️⃣ Copy the token and paste it below (it won’t be displayed for security)\n")

    github_token = getpass.getpass("🔑 Enter your GitHub Personal Access Token (PAT): ")

    repo_name = input("📂 Enter the repository name: ").strip()
    description = input("📝 Enter a short description for the repository: ").strip()

    while True:
        privacy_choice = input("🔒 Make the repository private? (yes/no): ").strip().lower()
        if privacy_choice in ["yes", "y", "no", "n"]:
            is_private = privacy_choice in ["yes", "y"]
            break
        print("❌ Invalid choice. Please type 'yes' or 'no'.")

    return github_token, repo_name, description, is_private

def create_github_repo(github_token, repo_name, description, is_private):
    """Creates a new GitHub repository using the provided credentials."""
    url = "https://api.github.com/user/repos"
    headers = {
        "Authorization": f"token {github_token}",
        "Accept": "application/vnd.github.v3+json"
    }
    payload = {
        "name": repo_name,
        "description": description,
        "private": is_private
    }
    
    response = requests.post(url, json=payload, headers=headers)
    
    if response.status_code == 201:
        print(f"\n✅ Repository '{repo_name}' created successfully!")
        print(f"🔗 URL: {response.json()['html_url']}\n")
    else:
        print(f"\n❌ Failed to create repository: {response.json()}\n")

if __name__ == "__main__":
    github_token, repo_name, description, is_private = get_user_inputs()
    create_github_repo(github_token, repo_name, description, is_private)
