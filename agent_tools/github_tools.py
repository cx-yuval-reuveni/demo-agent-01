import os
from github import Github

def fetch_repo_data(repo_url):
    """
    Fetches data from a GitHub repository given its URL.
    
    Args:
        repo_url (str): The URL of the GitHub repository.
        
    Returns:
        dict: A dictionary containing repository information.
    """
    g = Github()
    repo_name = repo_url.split('/')[-1]
    repo = g.get_repo(repo_name)
    
    return {
        "name": repo.name,
        "description": repo.description,
        "url": repo.html_url,
        "language": repo.language,
        "stars": repo.stargazers_count,
        "forks": repo.forks_count,
        "issues": repo.open_issues_count,
    }

def generate_readme_content(repo_data):
    """
    Generates README content based on the repository data.
    
    Args:
        repo_data (dict): A dictionary containing repository information.
        
    Returns:
        str: A formatted README string.
    """
    readme_content = f"# {repo_data['name']}\n\n"
    readme_content += f"## Description\n{repo_data['description']}\n\n"
    readme_content += f"## Repository Information\n"
    readme_content += f"- URL: {repo_data['url']}\n"
    readme_content += f"- Language: {repo_data['language']}\n"
    readme_content += f"- Stars: {repo_data['stars']}\n"
    readme_content += f"- Forks: {repo_data['forks']}\n"
    readme_content += f"- Open Issues: {repo_data['issues']}\n"
    
    return readme_content

def save_readme_to_file(content, file_path):
    """
    Saves the generated README content to a file.
    
    Args:
        content (str): The README content to save.
        file_path (str): The path where the README file will be saved.
    """
    # Sanitize the file path
    safe_directory = os.path.abspath(os.getcwd())
    resolved_path = os.path.abspath(file_path)

    if not resolved_path.startswith(safe_directory):
        raise ValueError("File path is outside the allowed directory.")

    with open(resolved_path, 'w') as f:
        f.write(content)