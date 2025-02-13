import subprocess
import sys
import getpass
import os

# Ensure required dependencies are installed
def install_dependencies():
    try:
        import requests  # Check if requests is installed
    except ImportError:
        print("📦 'requests' module not found. Installing now...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "requests"])

# Install dependencies before proceeding
install_dependencies()
import requests 


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
    github_username = input("👤 Enter your GitHub username: ").strip()
    repo_name = input("📂 Enter the repository name: ").strip()
    description = input("📝 Enter a short description for the repository: ").strip()

    while True:
        privacy_choice = input("🔒 Make the repository private? (yes/no): ").strip().lower()
        if privacy_choice in ["yes", "y", "no", "n"]:
            is_private = privacy_choice in ["yes", "y"]
            break
        print("❌ Invalid choice. Please type 'yes' or 'no'.")

    return github_token, github_username, repo_name, description, is_private

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
        repo_url = response.json()['html_url']
        print(f"\n✅ Repository '{repo_name}' created successfully!")
        print(f"🔗 URL: {repo_url}\n")
        return repo_url
    else:
        print(f"\n❌ Failed to create repository: {response.json()}\n")
        return None

def clone_repository(repo_url, github_username, repo_name):
    """Clones the newly created GitHub repository to a local directory."""
    while True:
        clone_choice = input("⬇️  Would you like to clone this repository locally? (yes/no): ").strip().lower()
        if clone_choice in ["yes", "y", "no", "n"]:
            break
        print("❌ Invalid choice. Please type 'yes' or 'no'.")

    if clone_choice in ["yes", "y"]:
        local_path = input("📁 Enter the local directory where you want to clone the repo: ").strip()

        # Ensure the directory exists
        if not os.path.isdir(local_path):
            print(f"⚠️ Directory '{local_path}' does not exist. Creating it now...")
            os.makedirs(local_path)

        # Full clone path
        repo_local_path = os.path.join(local_path, repo_name)

        # Check if the directory is empty or doesn't exist
        if os.path.exists(repo_local_path):
            print(f"❌ Error: Directory '{repo_local_path}' already exists. Choose a different path or delete the existing folder.")
            return
        
        # Clone the repository
        print(f"🔄 Cloning repository into '{repo_local_path}'...")
        clone_command = f"git clone {repo_url}.git {repo_local_path}"
        
        result = subprocess.run(clone_command, shell=True, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"\n✅ Repository successfully cloned into: {repo_local_path}\n")
        else:
            print(f"\n❌ Failed to clone repository. Error:\n{result.stderr}")

if __name__ == "__main__":
    github_token, github_username, repo_name, description, is_private = get_user_inputs()
    repo_url = create_github_repo(github_token, repo_name, description, is_private)
    
    if repo_url:
        clone_repository(repo_url, github_username, repo_name)
