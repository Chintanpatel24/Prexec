#!/usr/bin/env python3
"""
check_pr - GitHub Pull Request Tracker
A simple Python tool to check all Pull Requests created by a GitHub user across all their repositories.

Author: Your Name
License: MIT
Version: 1.0.0
"""

import urllib.request
import urllib.error
import json
import time
import sys
import os

# ANSI color codes for better output
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'

def print_header():
    """Print the application header"""
    print("\n" + "="*70)
    print("  GITHUB TOTAL PR CHECKER")
    print("  Check all PRs by a user across all their repositories")
    print("="*70 + "\n")

def get_github_token():
    """Try to get GitHub token from environment or .env file"""
    # Check environment variable
    token = os.getenv('GITHUB_TOKEN')
    
    # Check .env file
    if not token and os.path.exists('.env'):
        try:
            with open('.env', 'r') as f:
                for line in f:
                    if line.startswith('GITHUB_TOKEN='):
                        token = line.strip().split('=', 1)[1]
                        break
        except:
            pass
    
    return token

def make_api_request(url, token=None):
    """Make a request to GitHub API with optional authentication"""
    req = urllib.request.Request(url)
    
    # Add token if available
    if token:
        req.add_header('Authorization', f'token {token}')
    
    # Add User-Agent (required by GitHub)
    req.add_header('User-Agent', 'check_pr-script')
    
    try:
        with urllib.request.urlopen(req) as response:
            data = response.read()
            return json.loads(data), None
    except urllib.error.HTTPError as e:
        error_data = json.loads(e.read())
        return None, error_data.get('message', 'Unknown error')
    except Exception as e:
        return None, str(e)

def get_user_repos(username, token=None):
    """Get all repositories owned by a user"""
    repos = []
    page = 1
    
    print(f"\n🔍 Fetching repositories for @{username}...", end="", flush=True)
    
    while True:
        url = f"https://api.github.com/users/{username}/repos?per_page=100&page={page}&sort=updated"
        data, error = make_api_request(url, token)
        
        if error:
            print(f"\n❌ Error: {error}")
            return None
        
        if not data:
            break
        
        for repo in data:
            repos.append({
                'name': repo['name'],
                'full_name': repo['full_name'],
                'owner': repo['owner']['login'],
                'private': repo['private'],
                'fork': repo['fork']
            })
        
        print(".", end="", flush=True)
        page += 1
    
    print(f" Found {len(repos)} repositories!\n")
    return repos

def get_prs_in_repo(username, repo_full_name, token=None):
    """Get all PRs by user in a specific repository"""
    merged = 0
    pending = 0
    closed = 0
    pr_details = []
    
    page = 1
    
    while True:
        url = f"https://api.github.com/repos/{repo_full_name}/pulls?state=all&per_page=100&page={page}"
        data, error = make_api_request(url, token)
        
        if error:
            # Repo might be private or deleted, skip it
            break
        
        if not data:
            break
        
        for pr in data:
            if pr['user']['login'].lower() == username.lower():
                pr_info = {
                    'number': pr['number'],
                    'title': pr['title'],
                    'url': pr['html_url'],
                    'repo': repo_full_name,
                    'created_at': pr['created_at'][:10],
                    'state': pr['state']
                }
                
                if pr.get('merged_at'):
                    merged += 1
                    pr_info['status'] = 'merged'
                    pr_info['merged_at'] = pr['merged_at'][:10]
                elif pr['state'] == 'open':
                    pending += 1
                    pr_info['status'] = 'pending'
                else:
                    closed += 1
                    pr_info['status'] = 'closed'
                    if pr.get('closed_at'):
                        pr_info['closed_at'] = pr['closed_at'][:10]
                
                pr_details.append(pr_info)
        
        page += 1
    
    return merged, pending, closed, pr_details

def display_summary(username, total_merged, total_pending, total_closed):
    """Display the summary statistics"""
    total_prs = total_merged + total_pending + total_closed
    
    print("\n" + "="*70)
    print(f"📊 TOTAL PR STATISTICS FOR @{username}")
    print("="*70)
    print(f"\n📈 Summary Across All Repositories:")
    print(f"   Total PRs Created: {total_prs}")
    print(f"   ✅ Merged (Accepted): {total_merged}")
    print(f"   ⏳ Pending (Open): {total_pending}")
    print(f"   ❌ Closed (Not Merged): {total_closed}")
    print("\n" + "="*70)
    
    return total_prs

def display_detailed_prs(all_prs):
    """Display detailed PR information"""
    # Group by status
    merged_prs = [pr for pr in all_prs if pr['status'] == 'merged']
    pending_prs = [pr for pr in all_prs if pr['status'] == 'pending']
    closed_prs = [pr for pr in all_prs if pr['status'] == 'closed']
    
    # Display merged PRs
    if merged_prs:
        print("\n" + "="*70)
        print(f"✅ MERGED PRs ({len(merged_prs)}):")
        print("="*70)
        for i, pr in enumerate(merged_prs, 1):
            print(f"\n  [{i}] PR #{pr['number']} in {pr['repo']}")
            print(f"      Title: {pr['title']}")
            print(f"      Created: {pr['created_at']} | Merged: {pr.get('merged_at', 'N/A')}")
            print(f"      Link: {pr['url']}")
    
    # Display pending PRs
    if pending_prs:
        print("\n" + "="*70)
        print(f"⏳ PENDING PRs ({len(pending_prs)}):")
        print("="*70)
        for i, pr in enumerate(pending_prs, 1):
            print(f"\n  [{i}] PR #{pr['number']} in {pr['repo']}")
            print(f"      Title: {pr['title']}")
            print(f"      Created: {pr['created_at']}")
            print(f"      Link: {pr['url']}")
    
    # Display closed PRs
    if closed_prs:
        print("\n" + "="*70)
        print(f"❌ CLOSED PRs ({len(closed_prs)}):")
        print("="*70)
        for i, pr in enumerate(closed_prs, 1):
            print(f"\n  [{i}] PR #{pr['number']} in {pr['repo']}")
            print(f"      Title: {pr['title']}")
            print(f"      Created: {pr['created_at']} | Closed: {pr.get('closed_at', 'N/A')}")
            print(f"      Link: {pr['url']}")

def export_to_json(username, all_prs, total_merged, total_pending, total_closed):
    """Export results to JSON file"""
    filename = f"{username}_pr_stats.json"
    
    data = {
        'username': username,
        'total_prs': len(all_prs),
        'merged': total_merged,
        'pending': total_pending,
        'closed': total_closed,
        'pull_requests': all_prs
    }
    
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"\n📄 Results exported to: {filename}")
    except Exception as e:
        print(f"\n❌ Error exporting to JSON: {e}")

def export_to_csv(username, all_prs):
    """Export results to CSV file"""
    filename = f"{username}_pr_stats.csv"
    
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            # Write header
            f.write("Repository,PR Number,Title,Status,Created Date,Merged/Closed Date,URL\n")
            
            # Write data
            for pr in all_prs:
                repo = pr['repo']
                number = pr['number']
                title = pr['title'].replace(',', ';').replace('\n', ' ')
                status = pr['status']
                created = pr['created_at']
                date = pr.get('merged_at', pr.get('closed_at', 'N/A'))
                url = pr['url']
                
                f.write(f'"{repo}",{number},"{title}",{status},{created},{date},{url}\n')
        
        print(f"📄 Results exported to: {filename}")
    except Exception as e:
        print(f"\n❌ Error exporting to CSV: {e}")

def check_all_prs(username, token=None):
    """Check all PRs across all user's repositories"""
    
    # Get user's repositories
    repos = get_user_repos(username, token)
    
    if not repos:
        return
    
    # Track totals
    total_merged = 0
    total_pending = 0
    total_closed = 0
    all_prs = []
    
    print(f"🔍 Checking PRs in {len(repos)} repositories...\n")
    
    # Check each repository
    for i, repo in enumerate(repos, 1):
        print(f"[{i}/{len(repos)}] Checking {repo['full_name']}...", end="", flush=True)
        
        merged, pending, closed, pr_details = get_prs_in_repo(username, repo['full_name'], token)
        
        total_merged += merged
        total_pending += pending
        total_closed += closed
        all_prs.extend(pr_details)
        
        total_in_repo = merged + pending + closed
        if total_in_repo > 0:
            print(f" ✅ Found {total_in_repo} PRs")
        else:
            print(f" (no PRs)")
        
        # Small delay to avoid rate limiting
        time.sleep(0.1)
    
    # Display results
    total_prs = display_summary(username, total_merged, total_pending, total_closed)
    
    if total_prs == 0:
        print("\nNo PRs found in any repository.")
        return
    
    # Ask if user wants details
    print("\nWhat would you like to do?")
    print("1. Show detailed PR list")
    print("2. Export to JSON")
    print("3. Export to CSV")
    print("4. All of the above")
    print("5. Exit")
    
    choice = input("\nEnter your choice (1-5): ").strip()
    
    if choice == '1' or choice == '4':
        display_detailed_prs(all_prs)
    
    if choice == '2' or choice == '4':
        export_to_json(username, all_prs, total_merged, total_pending, total_closed)
    
    if choice == '3' or choice == '4':
        export_to_csv(username, all_prs)

def check_single_repo(username, repo_owner, repo_name, token=None):
    """Check PRs in a single repository (Method 2)"""
    print(f"\n🔍 Checking PRs by @{username} in {repo_owner}/{repo_name}...\n")
    
    repo_full_name = f"{repo_owner}/{repo_name}"
    merged, pending, closed, pr_details = get_prs_in_repo(username, repo_full_name, token)
    
    total_prs = merged + pending + closed
    
    print("\n" + "="*70)
    print(f"📊 PR STATISTICS FOR @{username} in {repo_full_name}")
    print("="*70)
    print(f"\n📈 Summary:")
    print(f"   Total PRs: {total_prs}")
    print(f"   ✅ Merged: {merged}")
    print(f"   ⏳ Pending: {pending}")
    print(f"   ❌ Closed: {closed}")
    print("\n" + "="*70)
    
    if total_prs == 0:
        print("\nNo PRs found in this repository.")
        return
    
    show_details = input("\nShow detailed PR list? (y/n): ").lower()
    if show_details == 'y':
        display_detailed_prs(pr_details)

def check_multiple_repos(username, token=None):
    """Check PRs in multiple specific repositories (Method 3)"""
    print("\n📁 Enter repositories to check (one per line, format: owner/repo)")
    print("   Example: facebook/react")
    print("   Enter 'done' when finished:\n")
    
    repos = []
    while True:
        repo = input("Repository: ").strip()
        if repo.lower() == 'done':
            break
        if '/' in repo:
            repos.append(repo)
        else:
            print("   Invalid format! Use: owner/repo")
    
    if not repos:
        print("\n❌ No repositories entered!")
        return
    
    total_merged = 0
    total_pending = 0
    total_closed = 0
    all_prs = []
    
    print(f"\n🔍 Checking {len(repos)} repositories...\n")
    
    for i, repo in enumerate(repos, 1):
        print(f"[{i}/{len(repos)}] Checking {repo}...", end="", flush=True)
        
        merged, pending, closed, pr_details = get_prs_in_repo(username, repo, token)
        
        total_merged += merged
        total_pending += pending
        total_closed += closed
        all_prs.extend(pr_details)
        
        total_in_repo = merged + pending + closed
        if total_in_repo > 0:
            print(f" ✅ Found {total_in_repo} PRs")
        else:
            print(f" (no PRs)")
    
    # Display results
    total_prs = display_summary(username, total_merged, total_pending, total_closed)
    
    if total_prs > 0:
        show_details = input("\nShow detailed PR list? (y/n): ").lower()
        if show_details == 'y':
            display_detailed_prs(all_prs)

def show_help():
    """Display help information"""
    help_text = """
╔══════════════════════════════════════════════════════════════════════╗
║                     check_pr - HELP & USAGE                          ║
╚══════════════════════════════════════════════════════════════════════╝

DESCRIPTION:
    A tool to check Pull Requests created by a GitHub user

METHODS:
    
    Method 1: Check all user's repositories
        - Scans ALL repositories owned by the user
        - Most comprehensive option
    
    Method 2: Check a single repository
        - Check PRs in one specific repository
        - Faster for targeted searches
    
    Method 3: Check multiple specific repositories
        - Choose exactly which repositories to check
        - Flexible option for multiple repos

USAGE:
    
    python check_pr.py              # Interactive mode
    python check_pr.py --help       # Show this help

GITHUB TOKEN (Optional):
    
    To avoid rate limits, create a .env file:
    
        GITHUB_TOKEN=your_token_here
    
    Or set environment variable:
    
        export GITHUB_TOKEN=your_token_here

RATE LIMITS:
    
    Without token: 60 requests/hour
    With token: 5000 requests/hour

EXAMPLES:
    
    1. Check all repos for user "torvalds":
       - Select Method 1
       - Enter username: torvalds
    
    2. Check PRs in facebook/react by user "gaearon":
       - Select Method 2
       - Enter username: gaearon
       - Enter owner: facebook
       - Enter repo: react
    
    3. Check multiple repos:
       - Select Method 3
       - Enter username
       - Enter repos one by one

For more information, visit:
    https://github.com/Chintanpatel24/c-pr

    """
    print(help_text)

def main():
    """Main function"""
    # Check for help flag
    if len(sys.argv) > 1 and sys.argv[1] in ['--help', '-h', 'help']:
        show_help()
        return
    
    # Print header
    print_header()
    
    # Get GitHub token if available
    token = get_github_token()
    if token:
        print("🔑 GitHub token detected - using authenticated requests\n")
    else:
        print("ℹ️  No GitHub token found - using unauthenticated requests")
        print("   (Limited to 60 requests/hour. Create .env file with GITHUB_TOKEN for 5000/hour)\n")
    
    # Choose method
    print("Select a method:")
    print("1. Check all repositories owned by a user (Method 1)")
    print("2. Check a specific repository (Method 2)")
    print("3. Check multiple specific repositories (Method 3)")
    print("4. Show help")
    print("5. Exit")
    
    method = input("\nEnter your choice (1-5): ").strip()
    
    if method == '4':
        show_help()
        return
    elif method == '5':
        print("\n👋 Goodbye!\n")
        return
    
    # Get username
    username = input("\n👤 Enter GitHub username: ").strip()
    
    if not username:
        print("\n❌ Username is required!")
        return
    
    # Execute based on method
    if method == '1':
        check_all_prs(username, token)
    elif method == '2':
        repo_owner = input("🏢 Enter repository owner: ").strip()
        repo_name = input("📁 Enter repository name: ").strip()
        if repo_owner and repo_name:
            check_single_repo(username, repo_owner, repo_name, token)
        else:
            print("\n❌ Repository owner and name are required!")
    elif method == '3':
        check_multiple_repos(username, token)
    else:
        print("\n❌ Invalid choice!")
        return
    
    print("\n✨ Done!\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Process interrupted by user. Goodbye!\n")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ An unexpected error occurred: {e}\n")
        sys.exit(1)
