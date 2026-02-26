#!/usr/bin/env python3

import urllib.request
import urllib.error
import json
import time
import sys
import os
import threading
from datetime import datetime, timedelta

# Check and import matplotlib
try:
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches
    import matplotlib.dates as mdates
    from matplotlib.patches import FancyBboxPatch
    import numpy as np
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False
    print("⚠️  matplotlib not found. Install it with: pip install matplotlib numpy")
    print("   Continuing without graph generation...\n")

# -------------------------
# Safe Formatting Helper
# -------------------------

def safe_str(value, default='N/A'):
    """Safely convert value to string, handling None"""
    if value is None:
        return default
    return str(value)

def safe_int(value, default=0):
    """Safely convert value to int, handling None"""
    if value is None:
        return default
    try:
        return int(value)
    except (ValueError, TypeError):
        return default

# -------------------------
# Cross-Platform Utilities
# -------------------------

def get_home_directory():
    """Get home directory cross-platform"""
    return os.path.expanduser("~")

def get_desktop_path():
    """Get desktop path cross-platform"""
    home = get_home_directory()
    return os.path.join(home, "Desktop")

def get_documents_path():
    """Get documents path cross-platform"""
    home = get_home_directory()
    return os.path.join(home, "Documents")

def clear_screen():
    """Clear screen cross-platform"""
    os.system('cls' if sys.platform == 'win32' else 'clear')

def get_os_name():
    """Get friendly OS name"""
    if sys.platform == "win32":
        return "Windows"
    elif sys.platform == "darwin":
        return "macOS"
    else:
        return "Linux"

# -------------------------
# Animation Utilities
# -------------------------

class LoadingSpinner:
    """Animated loading spinner"""
    def __init__(self, message="Loading"):
        self.message = message
        self.running = False
        self.thread = None
        self.spinner_chars = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
    
    def spin(self):
        i = 0
        while self.running:
            sys.stdout.write(f"\r   {self.spinner_chars[i % len(self.spinner_chars)]} {self.message}")
            sys.stdout.flush()
            time.sleep(0.1)
            i += 1
    
    def start(self):
        self.running = True
        self.thread = threading.Thread(target=self.spin)
        self.thread.start()
    
    def stop(self, final_message=None):
        self.running = False
        if self.thread:
            self.thread.join()
        if final_message:
            sys.stdout.write(f"\r   ✅ {final_message}\n")
        else:
            sys.stdout.write(f"\r   ✅ {self.message} - Done!\n")
        sys.stdout.flush()


def progress_bar(current, total, prefix="Progress", length=40):
    """Display animated progress bar"""
    if total == 0:
        total = 1
    percent = (current / total) * 100
    filled = int(length * current // total)
    bar = "█" * filled + "░" * (length - filled)
    sys.stdout.write(f"\r   {prefix}: [{bar}] {percent:.1f}% ({current}/{total})")
    sys.stdout.flush()


def show_scanning_animation(text, duration=1.0):
    """Show scanning dots animation"""
    end_time = time.time() + duration
    dots = 0
    while time.time() < end_time:
        sys.stdout.write(f"\r   🔍 {text}" + "." * dots + "   ")
        sys.stdout.flush()
        dots = (dots + 1) % 4
        time.sleep(0.3)
    sys.stdout.write(f"\r   ✅ {text} - Complete!     \n")
    sys.stdout.flush()


# -------------------------
# Header and UI
# -------------------------

def print_header():
    clear_screen()
    header = """
╔══════════════════════════════════════════════════════════════════════════════════╗
║                                                                                  ║
║    ██████╗ ██████╗      ██████╗██╗  ██╗███████╗ ██████╗██╗  ██╗███████╗██████╗   ║
║    ██╔══██╗██╔══██╗    ██╔════╝██║  ██║██╔════╝██╔════╝██║ ██╔╝██╔════╝██╔══██╗  ║
║    ██████╔╝██████╔╝    ██║     ███████║█████╗  ██║     █████╔╝ █████╗  ██████╔╝  ║
║    ██╔═══╝ ██╔══██╗    ██║     ██╔══██║██╔══╝  ██║     ██╔═██╗ ██╔══╝  ██╔══██╗  ║
║    ██║     ██║  ██║    ╚██████╗██║  ██║███████╗╚██████╗██║  ██╗███████╗██║  ██║  ║
║    ╚═╝     ╚═╝  ╚═╝     ╚═════╝╚═╝  ╚═╝╚══════╝ ╚═════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝  ║
║                                                                                  ║
║               !! GitHub Pull Request Analyzer & Visualizer !!                    ║
║                                                                                  ║
╠══════════════════════════════════════════════════════════════════════════════════╣
║                                                                                  ║
║          Analyze PRs    │     Generate Graphs    │     Export Reports            ║
║                                                                                  ║
╚══════════════════════════════════════════════════════════════════════════════════╝
"""
    print(header)
    print(f"   🖥️  Running on: {get_os_name()}")
    print(f"   📁 Home Directory: {get_home_directory()}")
    print(f"   📊 Matplotlib: {'✅ Available' if MATPLOTLIB_AVAILABLE else '❌ Not Available'}")
    print()


def show_system_info():
    """Display system information"""
    print("\n╔═══════════════════════════════════════════════════════════════════════════╗")
    print("║                           📋 SYSTEM INFORMATION                             ║")
    print("╠═════════════════════════════════════════════════════════════════════════════╣")
    print(f"║   Operating System  : {get_os_name():<53} ║")
    print(f"║   Python Version    : {sys.version.split()[0]:<53} ║")
    print(f"║   Home Directory    : {get_home_directory()[:53]:<53} ║")
    print(f"║   Current Directory : {os.getcwd()[:53]:<53} ║")
    print(f"║   Matplotlib        : {'Installed ✅' if MATPLOTLIB_AVAILABLE else 'Not Installed ❌':<53} ║")
    print("╚═════════════════════════════════════════════════════════════════════════════╝\n")


def show_main_menu():
    """Display main menu"""
    print("\n╔═══════════════════════════════════════════════════════════════════════════╗")
    print("║                              SELECT AN OPTION                               ║")
    print("╠═════════════════════════════════════════════════════════════════════════════╣")
    print("║                                                                             ║")
    print("║   [1] 🔍 Quick Scan       - Basic PR statistics                             ║")
    print("║   [2] 🔬 Deep Scan        - Detailed analysis with graphs                   ║")
    print("║   [3] ℹ️  System Info      - Show system information                        ║")
    print("║   [4] 🚪 Exit             - Close the application                           ║")
    print("║                                                                             ║")
    print("╚═════════════════════════════════════════════════════════════════════════════╝")


# -------------------------
# GitHub API Utilities
# -------------------------

def get_github_token():
    """Get GitHub token from environment or .env file"""
    token = os.getenv("GITHUB_TOKEN")
    if not token and os.path.exists(".env"):
        try:
            with open(".env") as f:
                for line in f:
                    if line.startswith("GITHUB_TOKEN="):
                        token = line.strip().split("=", 1)[1]
        except Exception:
            pass
    return token


def make_api_request(url, token=None):
    """Make API request"""
    req = urllib.request.Request(url)
    req.add_header("User-Agent", "pr-checker-script")
    if token:
        req.add_header("Authorization", f"token {token}")
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            return json.loads(response.read()), None
    except urllib.error.HTTPError as e:
        try:
            error_body = e.read()
            return None, json.loads(error_body).get("message", str(e))
        except Exception:
            return None, str(e)
    except urllib.error.URLError as e:
        return None, f"Connection error: {str(e.reason)}"
    except Exception as e:
        return None, str(e)


def check_rate_limit(token):
    """Check and display API rate limit"""
    print("\n╔═════════════════════════════════════════════════════════════════════════════╗")
    print("║                         🔄 CHECKING API RATE LIMIT                          ║")
    print("╚═════════════════════════════════════════════════════════════════════════════╝")
    
    spinner = LoadingSpinner("Connecting to GitHub API")
    spinner.start()
    
    data, error = make_api_request("https://api.github.com/rate_limit", token)
    time.sleep(0.5)
    
    spinner.stop("Connected to GitHub API")
    
    if data:
        rate_data = data.get("rate", {})
        remaining = safe_int(rate_data.get("remaining"), 0)
        limit = safe_int(rate_data.get("limit"), 60)
        reset_timestamp = rate_data.get("reset")
        
        if reset_timestamp:
            reset_time = datetime.fromtimestamp(reset_timestamp).strftime("%H:%M:%S")
        else:
            reset_time = "Unknown"
        
        if limit > 0:
            percent = (remaining / limit) * 100
        else:
            percent = 0
        
        bar_length = 30
        filled = int(bar_length * remaining // max(limit, 1))
        bar = "█" * filled + "░" * (bar_length - filled)
        
        if percent > 50:
            status = "🟢 Good"
        elif percent > 20:
            status = "🟡 Moderate"
        else:
            status = "🔴 Low"
        
        print(f"\n   API Rate Limit: [{bar}] {remaining}/{limit}")
        print(f"   Status: {status} | Resets at: {reset_time}")
        
        return remaining > 0
    else:
        print(f"   ⚠️  Could not check rate limit: {safe_str(error, 'Unknown error')}")
        return True


def verify_username(username, token):
    """Verify if GitHub username exists"""
    print(f"\n   🔍 Verifying username '@{username}'...")
    
    spinner = LoadingSpinner(f"Looking up @{username}")
    spinner.start()
    
    url = f"https://api.github.com/users/{username}"
    data, error = make_api_request(url, token)
    time.sleep(0.8)
    
    spinner.stop()
    
    if data:
        name = safe_str(data.get('name'), 'N/A')[:45]
        location = safe_str(data.get('location'), 'N/A')[:45]
        public_repos = safe_int(data.get('public_repos'), 0)
        followers = safe_int(data.get('followers'), 0)
        created_at = safe_str(data.get('created_at'), 'N/A')[:10]
        
        print("\n╔═════════════════════════════════════════════════════════════════════════════╗")
        print("║                              ✅ USER FOUND                                  ║")
        print("╠═════════════════════════════════════════════════════════════════════════════╣")
        print(f"║   👤 Name         : {name:<55} ║")
        print(f"║   📍 Location     : {location:<55} ║")
        print(f"║   📦 Public Repos : {public_repos:<55} ║")
        print(f"║   👥 Followers    : {followers:<55} ║")
        print(f"║   📅 Joined       : {created_at:<55} ║")
        print("╚═════════════════════════════════════════════════════════════════════════════╝")
        return True, data
    else:
        print(f"   ❌ User '@{username}' not found!")
        return False, None


# -------------------------
# PR Fetching Engine
# -------------------------

def fetch_all_prs_animated(username, token=None):
    """Fetch ALL PRs using Search API"""
    
    print("\n╔═════════════════════════════════════════════════════════════════════════════╗")
    print("║                            🔍 STARTING PR SCAN                              ║")
    print("╚═════════════════════════════════════════════════════════════════════════════╝")
    
    print("\n   ┌─ PHASE 1: INITIALIZATION")
    show_scanning_animation("Initializing scan engine", 0.8)
    print("   └─ ✓ Phase 1 Complete\n")
    
    print("   ┌─ PHASE 2: CONNECTING TO GITHUB")
    show_scanning_animation("Establishing secure connection", 0.6)
    print("   └─ ✓ Phase 2 Complete\n")
    
    print("   ┌─ PHASE 3: FETCHING PULL REQUESTS")
    
    page = 1
    all_prs = []
    
    url = f"https://api.github.com/search/issues?q=author:{username}+type:pr&per_page=100&page=1"
    data, error = make_api_request(url, token)
    
    if error:
        print(f"   │  ❌ Error: {safe_str(error, 'Unknown error')}")
        return []
    
    if not data:
        print(f"   │  ❌ No data received from API")
        return []
    
    total_count = safe_int(data.get("total_count"), 0)
    print(f"   │  📊 Total PRs to fetch: {total_count}")
    
    if total_count == 0:
        print("   │  ⚠️  No PRs found for this user")
        print("   └─ ✓ Phase 3 Complete\n")
        return []
    
    total_pages = (total_count + 99) // 100
    
    while True:
        progress_bar(page, total_pages, "Fetching PRs", 40)
        
        url = f"https://api.github.com/search/issues?q=author:{username}+type:pr&per_page=100&page={page}"
        data, error = make_api_request(url, token)
        
        if error or not data:
            break
        
        items = data.get("items", [])
        if not items:
            break
        
        all_prs.extend(items)
        time.sleep(0.2)
        
        if len(items) < 100:
            break
        
        page += 1
    
    print(f"\n   │  ✅ Successfully fetched {len(all_prs)} PRs")
    print("   └─ ✓ Phase 3 Complete\n")
    
    if len(all_prs) > 0:
        print("   ┌─ PHASE 4: PROCESSING DATA")
        for i in range(len(all_prs)):
            progress_bar(i + 1, len(all_prs), "Processing PRs", 40)
            time.sleep(0.01)
        print(f"\n   └─ ✓ Phase 4 Complete\n")
    
    print("╔═════════════════════════════════════════════════════════════════════════════╗")
    print(f"║            ✅ SCAN COMPLETE - {len(all_prs)} PULL REQUESTS FOUND                        ║")
    print("╚═════════════════════════════════════════════════════════════════════════════╝")
    
    return all_prs


# -------------------------
# PR Type Detection Engine
# -------------------------

# PR Type Keywords
PR_TYPE_PATTERNS = {
    "🐛 Bug Fix": {
        "keywords": ["fix", "bug", "issue", "error", "crash", "broken", "patch", "hotfix", 
                     "resolve", "solving", "repair", "correct", "debug", "fault", "defect"],
        "title_weight": 2,
        "body_weight": 1
    },
    "✨ Feature": {
        "keywords": ["feature", "add", "new", "implement", "create", "introduce", "support",
                     "enable", "allow", "capability", "functionality", "enhancement"],
        "title_weight": 2,
        "body_weight": 1
    },
    "📚 Documentation": {
        "keywords": ["doc", "readme", "documentation", "comment", "guide", "tutorial",
                     "wiki", "changelog", "license", "contributing", "api doc", "jsdoc",
                     "docstring", "typo in doc", "update readme"],
        "title_weight": 2,
        "body_weight": 1
    },
    "♻️ Refactor": {
        "keywords": ["refactor", "restructure", "reorganize", "cleanup", "clean up",
                     "improve code", "code quality", "simplify", "optimize code",
                     "better structure", "rewrite", "modernize"],
        "title_weight": 2,
        "body_weight": 1
    },
    "📦 Dependency": {
        "keywords": ["dependency", "dependencies", "package", "npm", "pip", "yarn",
                     "update package", "upgrade", "bump", "version bump", "security update",
                     "dependabot", "renovate", "greenkeeper", "snyk"],
        "title_weight": 2,
        "body_weight": 1
    },
    "🧪 Test": {
        "keywords": ["test", "testing", "spec", "unit test", "integration test", "e2e",
                     "coverage", "jest", "pytest", "mocha", "cypress", "selenium",
                     "test case", "test suite", "tdd", "bdd"],
        "title_weight": 2,
        "body_weight": 1
    },
    "⚡ Performance": {
        "keywords": ["performance", "optimize", "speed", "faster", "efficient", "memory",
                     "cache", "lazy load", "async", "parallel", "benchmark", "profiling",
                     "reduce load", "improve speed"],
        "title_weight": 2,
        "body_weight": 1
    },
    "🎨 Style/Lint": {
        "keywords": ["style", "lint", "format", "prettier", "eslint", "formatting",
                     "code style", "indentation", "whitespace", "semicolon", "trailing",
                     "black", "flake8", "pylint", "rubocop"],
        "title_weight": 2,
        "body_weight": 1
    },
    "🌐 Translation": {
        "keywords": ["translation", "translate", "i18n", "l10n", "locale", "language",
                     "internationalization", "localization", "multilingual", "lang"],
        "title_weight": 2,
        "body_weight": 1
    },
    "🔧 Config": {
        "keywords": ["config", "configuration", "settings", "env", "environment",
                     "ci/cd", "workflow", "github action", "travis", "jenkins", "docker",
                     "kubernetes", "yaml", "json config"],
        "title_weight": 2,
        "body_weight": 1
    },
    "🔒 Security": {
        "keywords": ["security", "vulnerability", "cve", "xss", "csrf", "injection",
                     "auth", "authentication", "authorization", "encrypt", "ssl", "https",
                     "sanitize", "escape", "secure"],
        "title_weight": 2,
        "body_weight": 1
    },
    "🗑️ Deprecation": {
        "keywords": ["deprecate", "remove", "delete", "drop support", "end of life",
                     "obsolete", "legacy", "cleanup old", "remove unused"],
        "title_weight": 2,
        "body_weight": 1
    }
}

# Tool Detection Patterns
TOOL_PATTERNS = {
    "🖥️ GitHub Web": {
        "patterns": [],  # Default if no specific tool detected
        "body_hints": ["<!-- -->", "## description", "## changes", "### checklist"],
        "is_default": True
    },
    "💻 GitHub CLI (gh)": {
        "patterns": ["created via gh cli", "gh pr create", "via github cli", 
                     "github.com/cli/cli"],
        "body_hints": []
    },
    "🔧 Git CLI + API": {
        "patterns": [],
        "body_hints": [],
        "empty_body": True  # Short or empty body often indicates API/CLI
    },
    "🤖 Dependabot": {
        "patterns": ["dependabot", "dependabot[bot]", "dependabot-preview"],
        "body_hints": ["bumps", "from ", " to ", "release notes", "changelog", "commits"]
    },
    "🔄 Renovate Bot": {
        "patterns": ["renovate", "renovate[bot]", "renovatebot"],
        "body_hints": ["this pr contains", "renovate", "datasource", "package update"]
    },
    "🛡️ Snyk Bot": {
        "patterns": ["snyk", "snyk-bot", "snyk[bot]"],
        "body_hints": ["snyk", "vulnerability", "security upgrade"]
    },
    "📦 Greenkeeper": {
        "patterns": ["greenkeeper", "greenkeeper[bot]"],
        "body_hints": ["greenkeeper", "update", "version"]
    },
    "🖼️ ImgBot": {
        "patterns": ["imgbot", "imgbot[bot]"],
        "body_hints": ["image", "optimize", "compression", "imgbot"]
    },
    "👥 All Contributors": {
        "patterns": ["allcontributors", "all-contributors"],
        "body_hints": ["add", "contributor", "all-contributors"]
    },
    "🚀 Release Bot": {
        "patterns": ["release-bot", "semantic-release", "release-please"],
        "body_hints": ["release", "version", "changelog"]
    },
    "⚙️ GitHub Actions": {
        "patterns": ["github-actions", "github-actions[bot]"],
        "body_hints": ["automated", "workflow", "action"]
    },
    "🖱️ GitHub Desktop": {
        "patterns": ["github desktop"],
        "body_hints": []
    },
    "💜 VS Code": {
        "patterns": ["vscode", "vs code"],
        "body_hints": ["vscode", "visual studio code"]
    },
    "🧠 JetBrains IDE": {
        "patterns": ["intellij", "pycharm", "webstorm", "phpstorm", "idea"],
        "body_hints": ["jetbrains", "intellij"]
    },
    "🐙 GitKraken": {
        "patterns": ["gitkraken"],
        "body_hints": ["gitkraken"]
    },
    "🌳 Sourcetree": {
        "patterns": ["sourcetree"],
        "body_hints": ["sourcetree"]
    },
    "☁️ GitHub Codespaces": {
        "patterns": ["codespaces", "codespace"],
        "body_hints": ["codespace", "github.dev"]
    },
    "🌐 GitPod": {
        "patterns": ["gitpod"],
        "body_hints": ["gitpod"]
    }
}


def detect_pr_type(pr):
    """Detect the type/category of PR based on content analysis"""
    
    title = safe_str(pr.get("title"), "").lower()
    body = safe_str(pr.get("body"), "").lower()
    
    scores = {}
    
    for pr_type, config in PR_TYPE_PATTERNS.items():
        score = 0
        keywords = config["keywords"]
        title_weight = config["title_weight"]
        body_weight = config["body_weight"]
        
        for keyword in keywords:
            if keyword in title:
                score += title_weight
            if keyword in body:
                score += body_weight
        
        if score > 0:
            scores[pr_type] = score
    
    if scores:
        return max(scores, key=scores.get)
    
    return "📝 General"


def detect_pr_tool(pr):
    """Detect which tool was used to create the PR"""
    
    body = safe_str(pr.get("body"), "").lower()
    user_data = pr.get("user") or {}
    user = safe_str(user_data.get("login"), "").lower()
    
    # Check for bot accounts first
    for tool_name, config in TOOL_PATTERNS.items():
        if config.get("is_default"):
            continue
            
        patterns = config.get("patterns", [])
        body_hints = config.get("body_hints", [])
        
        # Check user login
        for pattern in patterns:
            if pattern in user:
                return tool_name
        
        # Check body content
        for pattern in patterns:
            if pattern in body:
                return tool_name
        
        for hint in body_hints:
            if hint in body:
                return tool_name
    
    # Check for empty/minimal body (likely API/CLI)
    if len(body.strip()) < 20:
        return "🔧 Git CLI + API"
    
    # Default to web interface
    return "🖥️ GitHub Web"


def categorize_prs_animated(prs):
    """Categorize all PRs by type and tool"""
    print("\n   ┌─ CATEGORIZING PR TYPES & TOOLS")
    
    type_categories = {}
    tool_categories = {}
    total_prs = len(prs)
    
    for i, pr in enumerate(prs):
        progress_bar(i + 1, total_prs, "Analyzing PRs", 40)
        
        # Detect PR type
        pr_type = detect_pr_type(pr)
        if pr_type not in type_categories:
            type_categories[pr_type] = []
        type_categories[pr_type].append(pr)
        
        # Detect tool used
        tool = detect_pr_tool(pr)
        if tool not in tool_categories:
            tool_categories[tool] = []
        tool_categories[tool].append(pr)
        
        # Store in PR for later use
        pr["_detected_type"] = pr_type
        pr["_detected_tool"] = tool
        
        time.sleep(0.005)
    
    print(f"\n   │  ✅ Categorized into {len(type_categories)} types and {len(tool_categories)} tools")
    print("   └─ ✓ Categorization Complete\n")
    
    return type_categories, tool_categories


# -------------------------
# Analytics Engine
# -------------------------

def analyze_prs_animated(prs, username):
    """Analyze PRs with animated progress"""
    
    print("\n╔═════════════════════════════════════════════════════════════════════════════╗")
    print("║                           📊 ANALYZING PR DATA                              ║")
    print("╚═════════════════════════════════════════════════════════════════════════════╝")
    
    merged = pending = closed = draft = stale = 0
    repo_counter = {}
    yearly = {}
    monthly = {}
    daily = {}
    detailed = []
    pr_dates = []
    
    total_prs = len(prs)
    
    print("\n   ┌─ ANALYSIS IN PROGRESS")
    
    for i, pr in enumerate(prs):
        progress_bar(i + 1, total_prs, "Analyzing", 40)
        
        repo_url = safe_str(pr.get("repository_url"), "")
        if repo_url:
            parts = repo_url.split("/")
            if len(parts) >= 2:
                repo = parts[-2] + "/" + parts[-1]
            else:
                repo = "unknown/unknown"
        else:
            repo = "unknown/unknown"
        
        repo_counter[repo] = repo_counter.get(repo, 0) + 1
        
        created_at = safe_str(pr.get("created_at"), "1970-01-01T00:00:00Z")
        created_year = created_at[:4]
        created_month = created_at[:7]
        created_day = created_at[:10]
        
        yearly[created_year] = yearly.get(created_year, 0) + 1
        monthly[created_month] = monthly.get(created_month, 0) + 1
        daily[created_day] = daily.get(created_day, 0) + 1
        
        state = safe_str(pr.get("state"), "unknown")
        
        if pr.get("draft"):
            draft += 1
        
        # Track PR dates and states for productivity graph
        try:
            pr_date = datetime.strptime(created_at[:19], "%Y-%m-%dT%H:%M:%S")
            pr_data = pr.get("pull_request") or {}
            is_merged = pr_data.get("merged_at") is not None
            pr_dates.append({
                "date": pr_date,
                "state": state,
                "merged": is_merged
            })
        except:
            pass
        
        if state == "open":
            pending += 1
            try:
                created_date = datetime.strptime(created_at[:10], "%Y-%m-%d")
                if (datetime.now() - created_date).days > 180:
                    stale += 1
            except ValueError:
                pass
        elif state == "closed":
            pr_data = pr.get("pull_request") or {}
            if pr_data.get("merged_at"):
                merged += 1
            else:
                closed += 1
        
        detailed.append({
            "repo": repo,
            "number": safe_int(pr.get("number"), 0),
            "title": safe_str(pr.get("title"), "No title"),
            "status": state,
            "url": safe_str(pr.get("html_url"), ""),
            "created_at": created_at[:10]
        })
        
        time.sleep(0.008)
    
    print(f"\n   │  ✅ Analysis complete")
    print("   └─ ✓ Done\n")
    
    total = merged + pending + closed
    acceptance = round((merged / total) * 100, 2) if total > 0 else 0
    
    if repo_counter:
        top_repo = max(repo_counter, key=repo_counter.get)
    else:
        top_repo = "No repositories"
    
    # Sort PR dates
    pr_dates.sort(key=lambda x: x["date"])
    
    return {
        "merged": merged,
        "pending": pending,
        "closed": closed,
        "draft": draft,
        "stale": stale,
        "acceptance": acceptance,
        "top_repo": top_repo,
        "yearly": yearly,
        "monthly": monthly,
        "daily": daily,
        "repo_counter": repo_counter,
        "total": total,
        "details": detailed,
        "pr_dates": pr_dates
    }


# -------------------------
# Productivity Score Calculator
# -------------------------

def calculate_productivity_scores(pr_dates, acceptance_rate):
    """Calculate productivity scores over time for the profit/loss chart"""
    
    if not pr_dates or len(pr_dates) < 2:
        return [], []
    
    scores = []
    dates = []
    base_score = 50  # Start at 50%
    current_score = base_score
    
    # Calculate average time between PRs
    time_diffs = []
    for i in range(1, len(pr_dates)):
        diff = (pr_dates[i]["date"] - pr_dates[i-1]["date"]).total_seconds() / 3600  # Hours
        time_diffs.append(diff)
    
    if not time_diffs:
        return [], []
    
    avg_time_diff = sum(time_diffs) / len(time_diffs)
    
    # First PR
    dates.append(pr_dates[0]["date"])
    scores.append(current_score)
    
    for i in range(1, len(pr_dates)):
        pr = pr_dates[i]
        prev_pr = pr_dates[i-1]
        
        # Time between PRs in hours
        time_diff = (pr["date"] - prev_pr["date"]).total_seconds() / 3600
        
        # Calculate score change based on multiple factors
        score_change = 0
        
        # Factor 1: Time between PRs
        # If faster than average, score goes up; if slower, score goes down
        if time_diff < avg_time_diff:
            # Faster than average - productivity increase
            speed_factor = (avg_time_diff - time_diff) / max(avg_time_diff, 1)
            score_change += min(speed_factor * 15, 10)
        else:
            # Slower than average - productivity decrease
            speed_factor = (time_diff - avg_time_diff) / max(avg_time_diff, 1)
            score_change -= min(speed_factor * 10, 15)
        
        # Factor 2: PR was merged (positive) or just closed (negative)
        if pr["merged"]:
            score_change += 5
        elif pr["state"] == "closed":
            score_change -= 3
        
        # Factor 3: Consistency bonus (if maintaining pace)
        if i >= 2:
            prev_diff = (pr_dates[i-1]["date"] - pr_dates[i-2]["date"]).total_seconds() / 3600
            if abs(time_diff - prev_diff) < avg_time_diff * 0.3:  # Within 30% of previous pace
                score_change += 2
        
        # Apply score change with smoothing
        current_score = current_score + score_change
        
        # Keep score bounded between 0 and 100
        current_score = max(5, min(95, current_score))
        
        dates.append(pr["date"])
        scores.append(current_score)
    
    # Apply acceptance rate influence to all scores
    acceptance_multiplier = acceptance_rate / 100 if acceptance_rate > 0 else 0.5
    scores = [s * (0.5 + 0.5 * acceptance_multiplier) for s in scores]
    
    return dates, scores


# -------------------------
# Matplotlib Graph Engine
# -------------------------

def generate_graphs(username, stats, type_counts, tool_counts, save_path):
    """Generate matplotlib graphs and save them"""
    
    if not MATPLOTLIB_AVAILABLE:
        print("   ⚠️  Cannot generate graphs - matplotlib not installed")
        return None
    
    print("\n╔═════════════════════════════════════════════════════════════════════════════╗")
    print("║                            📈 GENERATING GRAPHS                             ║")
    print("╚═════════════════════════════════════════════════════════════════════════════╝\n")
    
    try:
        plt.style.use('dark_background')
    except:
        pass
    
    fig = plt.figure(figsize=(24, 18), facecolor='#1a1a2e')
    fig.suptitle(f"GitHub PR Analysis Report for @{username}", fontsize=22, fontweight='bold', 
                 y=0.98, color='white')
    
    # Graph 1: Productivity/Brain Power Chart (Profit-Loss Style)
    print("   ┌─ Creating Graph 1/6: Productivity Chart (Profit-Loss Style)...")
    ax1 = fig.add_subplot(2, 3, 1, facecolor='#16213e')
    
    pr_dates = stats.get("pr_dates", [])
    dates, scores = calculate_productivity_scores(pr_dates, stats["acceptance"])
    
    if dates and scores:
        # Create gradient fill effect
        for i in range(len(dates) - 1):
            color = '#00ff88' if scores[i+1] >= scores[i] else '#ff4444'
            ax1.fill_between([dates[i], dates[i+1]], [50, 50], [scores[i], scores[i+1]], 
                           alpha=0.3, color=color)
            ax1.plot([dates[i], dates[i+1]], [scores[i], scores[i+1]], 
                    color=color, linewidth=2)
        
        # Add markers at each point
        for i, (d, s) in enumerate(zip(dates, scores)):
            color = '#00ff88' if s >= 50 else '#ff4444'
            ax1.scatter([d], [s], color=color, s=30, zorder=5)
        
        # Add baseline
        ax1.axhline(y=50, color='white', linestyle='--', alpha=0.5, linewidth=1)
        ax1.fill_between(dates, 0, 50, alpha=0.1, color='#ff4444')
        ax1.fill_between(dates, 50, 100, alpha=0.1, color='#00ff88')
        
        ax1.set_ylim(0, 100)
        ax1.set_ylabel('Productivity Score', fontsize=10, color='white')
        ax1.set_xlabel('Time', fontsize=10, color='white')
        ax1.tick_params(colors='white')
        
        # Add annotations
        ax1.text(0.02, 0.95, '📈 HIGH PRODUCTIVITY', transform=ax1.transAxes, 
                fontsize=8, color='#00ff88', verticalalignment='top')
        ax1.text(0.02, 0.05, '📉 LOW PRODUCTIVITY', transform=ax1.transAxes, 
                fontsize=8, color='#ff4444', verticalalignment='bottom')
    else:
        ax1.text(0.5, 0.5, 'Insufficient Data', ha='center', va='center', 
                fontsize=14, color='white')
    
    ax1.set_title('🧠 Brain Power / Productivity Index', fontweight='bold', fontsize=12, color='white')
    ax1.grid(True, alpha=0.2)
    print("   │  ✅ Graph 1 created")
    
    # Graph 2: PR Types Distribution (Horizontal Bar)
    print("   ├─ Creating Graph 2/6: PR Types Distribution...")
    ax2 = fig.add_subplot(2, 3, 2, facecolor='#16213e')
    
    if type_counts:
        types = list(type_counts.keys())
        counts = list(type_counts.values())
        colors = plt.cm.Set3([i/max(len(types), 1) for i in range(len(types))])
        
        bars = ax2.barh(types, counts, color=colors, edgecolor='white', linewidth=0.5)
        ax2.set_xlabel('Number of PRs', fontsize=10, color='white')
        ax2.tick_params(colors='white')
        
        for bar, count in zip(bars, counts):
            width = bar.get_width()
            ax2.annotate(f'{count}', xy=(width, bar.get_y() + bar.get_height()/2),
                        xytext=(3, 0), textcoords="offset points", ha='left', va='center', 
                        fontsize=9, color='white')
    
    ax2.set_title('📋 PR Types Distribution', fontweight='bold', fontsize=12, color='white')
    print("   │  ✅ Graph 2 created")
    
    # Graph 3: Tools Used (Pie Chart)
    print("   ├─ Creating Graph 3/6: Tools Used...")
    ax3 = fig.add_subplot(2, 3, 3, facecolor='#16213e')
    
    if tool_counts:
        tools = list(tool_counts.keys())
        counts = list(tool_counts.values())
        colors = plt.cm.Pastel1([i/max(len(tools), 1) for i in range(len(tools))])
        
        wedges, texts, autotexts = ax3.pie(counts, labels=tools, colors=colors,
                                            autopct='%1.1f%%', startangle=90,
                                            textprops={'fontsize': 8, 'color': 'white'})
        for autotext in autotexts:
            autotext.set_color('black')
            autotext.set_fontsize(8)
    
    ax3.set_title('🛠️ Tools Used to Create PRs', fontweight='bold', fontsize=12, color='white')
    print("   │  ✅ Graph 3 created")
    
    # Graph 4: Monthly Trend with Area Fill
    print("   ├─ Creating Graph 4/6: Monthly Trend Analysis...")
    ax4 = fig.add_subplot(2, 3, 4, facecolor='#16213e')
    
    if stats['monthly']:
        months = sorted(stats['monthly'].keys())[-24:]
        counts = [stats['monthly'][m] for m in months]
        
        ax4.fill_between(range(len(months)), counts, alpha=0.4, color='#00d4ff')
        ax4.plot(range(len(months)), counts, color='#00d4ff', linewidth=2, marker='o', markersize=4)
        ax4.set_xlabel('Month', fontsize=10, color='white')
        ax4.set_ylabel('PRs', fontsize=10, color='white')
        ax4.tick_params(colors='white')
        ax4.set_xticks(range(0, len(months), 4))
        ax4.set_xticklabels([months[i][2:] for i in range(0, len(months), 4)], rotation=45)
        ax4.grid(True, alpha=0.2)
    
    ax4.set_title('📅 Monthly PR Trend', fontweight='bold', fontsize=12, color='white')
    print("   │  ✅ Graph 4 created")
    
    # Graph 5: PR Status (Donut Chart)
    print("   ├─ Creating Graph 5/6: PR Status Distribution...")
    ax5 = fig.add_subplot(2, 3, 5, facecolor='#16213e')
    
    status_labels = ['Merged', 'Pending', 'Closed']
    status_values = [stats['merged'], stats['pending'], stats['closed']]
    status_colors = ['#00ff88', '#ffcc00', '#ff4444']
    
    if sum(status_values) > 0:
        wedges, texts, autotexts = ax5.pie(status_values, labels=status_labels, 
                                            colors=status_colors, autopct='%1.1f%%',
                                            startangle=90, pctdistance=0.75,
                                            textprops={'fontsize': 10, 'color': 'white'})
        
        # Create donut effect
        centre_circle = plt.Circle((0, 0), 0.50, fc='#16213e')
        ax5.add_artist(centre_circle)
        
        # Add center text
        ax5.text(0, 0, f'{stats["total"]}\nTotal', ha='center', va='center', 
                fontsize=14, fontweight='bold', color='white')
    
    ax5.set_title('📊 PR Status Distribution', fontweight='bold', fontsize=12, color='white')
    print("   │  ✅ Graph 5 created")
    
    # Graph 6: Summary Stats
    print("   └─ Creating Graph 6/6: Summary Statistics...")
    ax6 = fig.add_subplot(2, 3, 6, facecolor='#16213e')
    ax6.axis('off')
    
    top_repo_display = safe_str(stats.get('top_repo'), 'No repositories')[:30]
    
    summary_text = f"""
    ╔══════════════════════════════════════════╗
    ║         📊 SUMMARY STATISTICS            ║
    ╠══════════════════════════════════════════╣
    ║                                          ║
    ║   Total PRs          : {stats['total']:>6}             ║
    ║   ───────────────────────────────────    ║
    ║   ✅ Merged           : {stats['merged']:>6}             ║
    ║   ⏳ Pending          : {stats['pending']:>6}             ║
    ║   ❌ Closed           : {stats['closed']:>6}             ║
    ║   📝 Draft            : {stats['draft']:>6}             ║
    ║   ⚠️  Stale            : {stats['stale']:>6}             ║
    ║   ───────────────────────────────────    ║
    ║   📈 Acceptance Rate : {stats['acceptance']:>5}%             ║
    ║                                          ║
    ║   🏆 Top Repository:                     ║
    ║      {top_repo_display:<34}  ║
    ║                                          ║
    ╚══════════════════════════════════════════╝
    """
    
    ax6.text(0.5, 0.5, summary_text, transform=ax6.transAxes, fontsize=11,
             verticalalignment='center', horizontalalignment='center',
             fontfamily='monospace', color='white',
             bbox=dict(boxstyle='round', facecolor='#16213e', edgecolor='#00d4ff', linewidth=2))
    print("      ✅ Graph 6 created\n")
    
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    
    graph_filename = os.path.join(save_path, "your-graph-by-cp.png")
    
    print("   💾 Saving graph...")
    for i in range(0, 101, 10):
        progress_bar(i, 100, "Saving", 40)
        time.sleep(0.05)
    
    plt.savefig(graph_filename, dpi=150, bbox_inches='tight', facecolor='#1a1a2e', edgecolor='none')
    plt.close()
    
    print(f"\n   ✅ Graph saved: {graph_filename}")
    
    return graph_filename


# -------------------------
# ASCII Graph Engine
# -------------------------

def create_ascii_bar(value, max_value, width=30, fill_char="█", empty_char="░"):
    """Create a single ASCII bar"""
    if max_value == 0:
        return empty_char * width
    filled = int((value / max_value) * width)
    return fill_char * filled + empty_char * (width - filled)


def print_ascii_flow_chart(stats):
    """Print ASCII flow chart of PR lifecycle"""
    total = stats['total']
    merged = stats['merged']
    pending = stats['pending']
    closed = stats['closed']
    acceptance = stats['acceptance']
    
    print("""
╔═════════════════════════════════════════════════════════════════════════════╗
║                          📊 PR LIFECYCLE FLOW CHART                         ║
╠═════════════════════════════════════════════════════════════════════════════╣
║                                                                             ║
║                              ┌───────────────┐                              ║
║                              │   TOTAL PRs   │                              ║""")
    print(f"║                              │     {total:^5}     │                              ║")
    print("""║                              └───────┬───────┘                              ║
║                                      │                                      ║
║                   ┌──────────────────┼──────────────────┐                   ║
║                   │                  │                  │                   ║
║                   ▼                  ▼                  ▼                   ║
║            ┌────────────┐     ┌────────────┐     ┌────────────┐             ║
║            │ ✅ MERGED  │     │ ⏳ PENDING │     │ ❌ CLOSED  │             ║""")
    print(f"║            │    {merged:^5}   │     │    {pending:^5}   │     │    {closed:^5}   │             ║")
    print("""║            └────────────┘     └────────────┘     └────────────┘             ║
║                                                                             ║
║                          ┌─────────────────────┐                            ║
║                          │  📈 ACCEPTANCE RATE │                            ║""")
    print(f"║                          │       {acceptance:^6}%       │                            ║")
    print("""║                          └─────────────────────┘                            ║
║                                                                             ║
╚═════════════════════════════════════════════════════════════════════════════╝
""")


def print_type_distribution_chart(type_data):
    """Print PR type distribution as ASCII chart"""
    if not type_data:
        return
    
    total = sum(type_data.values())
    max_count = max(type_data.values()) if type_data else 1
    
    print("""
╔═════════════════════════════════════════════════════════════════════════════╗
║                          📋 PR TYPE DISTRIBUTION                            ║
╠═════════════════════════════════════════════════════════════════════════════╣
║  PR Types Detected:                                                         ║
║  • 🐛 Bug Fix       - Resolving reported issues and defects                 ║
║  • ✨ Feature       - New functionality or capabilities                     ║
║  • 📚 Documentation - Improving README, guides, comments                    ║
║  • ♻️ Refactor      - Improving code structure                              ║
║  • 📦 Dependency    - Updating libraries and packages                       ║
║  • 🧪 Test          - Adding or improving test coverage                     ║
║  • ⚡ Performance   - Making code faster or more efficient                  ║
║  • 🎨 Style/Lint    - Formatting and code standards                         ║
║  • 🌐 Translation   - Adding or updating language translations              ║
╠═════════════════════════════════════════════════════════════════════════════╣""")
    
    for pr_type, count in sorted(type_data.items(), key=lambda x: -x[1]):
        percentage = (count / total * 100) if total > 0 else 0
        bar = create_ascii_bar(count, max_count, width=25, fill_char="█", empty_char="░")
        display_type = pr_type[:18] if len(pr_type) > 18 else pr_type
        print(f"║  {display_type:<18} │ {bar} │ {count:>4} ({percentage:>5.1f}%)     ║")
    
    print(f"╠═════════════════════════════════════════════════════════════════════════════╣")
    print(f"║  {'TOTAL':<18} │ {' '*25} │ {total:>4} (100.0%)     ║")
    print(f"╚═════════════════════════════════════════════════════════════════════════════╝")


def print_tool_distribution_chart(tool_data):
    """Print tool distribution as ASCII chart"""
    if not tool_data:
        return
    
    total = sum(tool_data.values())
    max_count = max(tool_data.values()) if tool_data else 1
    
    print("""
╔═════════════════════════════════════════════════════════════════════════════╗
║                        🛠️ TOOLS USED TO CREATE PRs                          ║
╠═════════════════════════════════════════════════════════════════════════════╣
║  Tools Detected:                                                            ║
║  • 🖥️ GitHub Web     - Browser-based PR creation                            ║
║  • 💻 GitHub CLI     - gh pr create command                                 ║
║  • 🔧 Git CLI + API  - Standard Git + API calls                             ║
║  • 🤖 Dependabot     - Automated dependency updates                         ║
║  • 🔄 Renovate Bot   - Package update automation                            ║
║  • 💜 VS Code        - VS Code GitHub Extension                             ║
║  • 🧠 JetBrains IDE  - IntelliJ, PyCharm, WebStorm                          ║
║  • ⚙️ GitHub Actions - Automated workflows                                  ║
╠═════════════════════════════════════════════════════════════════════════════╣""")
    
    for tool, count in sorted(tool_data.items(), key=lambda x: -x[1]):
        percentage = (count / total * 100) if total > 0 else 0
        bar = create_ascii_bar(count, max_count, width=25, fill_char="▓", empty_char="░")
        display_tool = tool[:18] if len(tool) > 18 else tool
        print(f"║  {display_tool:<18} │ {bar} │ {count:>4} ({percentage:>5.1f}%)     ║")
    
    print(f"╠═════════════════════════════════════════════════════════════════════════════╣")
    print(f"║  {'TOTAL':<18} │ {' '*25} │ {total:>4} (100.0%)     ║")
    print(f"╚═════════════════════════════════════════════════════════════════════════════╝")


def print_productivity_ascii_chart(stats):
    """Print ASCII productivity/brain power chart"""
    
    pr_dates = stats.get("pr_dates", [])
    dates, scores = calculate_productivity_scores(pr_dates, stats["acceptance"])
    
    if not scores or len(scores) < 2:
        print("""
╔═════════════════════════════════════════════════════════════════════════════╗
║                       🧠 PRODUCTIVITY / BRAIN POWER INDEX                   ║
╠═════════════════════════════════════════════════════════════════════════════╣
║                                                                             ║
║   ⚠️  Insufficient data to generate productivity chart                      ║
║      Need at least 2 PRs with different dates                               ║
║                                                                             ║
╚═════════════════════════════════════════════════════════════════════════════╝
""")
        return
    
    print("""
╔═════════════════════════════════════════════════════════════════════════════╗
║                       🧠 PRODUCTIVITY / BRAIN POWER INDEX                   ║
╠═════════════════════════════════════════════════════════════════════════════╣
║                                                                             ║
║   This chart shows your coding productivity over time based on:             ║
║   • Time between PRs (faster = higher productivity)                         ║
║   • PR acceptance rate (merged PRs boost score)                             ║
║   • Consistency of contributions                                            ║
║                                                                             ║
║   📈 Above 50% = High Productivity (Profit Zone)                            ║
║   📉 Below 50% = Low Productivity (Loss Zone)                               ║
║                                                                             ║
╠═════════════════════════════════════════════════════════════════════════════╣""")
    
    # Create ASCII chart
    chart_height = 10
    chart_width = 60
    
    # Normalize scores to chart
    min_score = min(scores)
    max_score = max(scores)
    score_range = max_score - min_score if max_score != min_score else 1
    
    # Sample scores if too many
    if len(scores) > chart_width:
        step = len(scores) // chart_width
        sampled_scores = [scores[i] for i in range(0, len(scores), step)][:chart_width]
    else:
        sampled_scores = scores
    
    # Build chart rows
    for row in range(chart_height, -1, -1):
        threshold = row * 10  # 0, 10, 20, ... 100
        
        if row == 5:
            line = "║  50% ┤"
        elif row == 10:
            line = "║ 100% ┤"
        elif row == 0:
            line = "║   0% ┤"
        else:
            line = "║      │"
        
        for score in sampled_scores:
            normalized = ((score - min_score) / score_range) * 100 if score_range > 0 else 50
            
            if normalized >= threshold and normalized < threshold + 10:
                if score >= 50:
                    line += "█"
                else:
                    line += "▓"
            elif normalized >= threshold + 10:
                if threshold >= 50:
                    line += "│"
                else:
                    line += "│"
            else:
                line += " "
        
        line = line.ljust(72) + "║"
        print(line)
    
    print("║      └" + "─" * len(sampled_scores) + " " * (65 - len(sampled_scores)) + "║")
    print("║       " + "└─── Time ───►" + " " * 52 + "║")
    print("║                                                                             ║")
    
    # Calculate overall trend
    if len(scores) >= 2:
        start_avg = sum(scores[:len(scores)//3]) / max(len(scores)//3, 1)
        end_avg = sum(scores[-len(scores)//3:]) / max(len(scores)//3, 1)
        
        if end_avg > start_avg + 5:
            trend = "📈 IMPROVING - Your productivity is on an upward trend!"
        elif end_avg < start_avg - 5:
            trend = "📉 DECLINING - Consider more frequent contributions"
        else:
            trend = "📊 STABLE - Maintaining consistent productivity"
        
        print(f"║   Trend: {trend:<64} ║")
    
    avg_score = sum(scores) / len(scores)
    print(f"║   Average Score: {avg_score:.1f}%                                                      ║")
    print("║                                                                             ║")
    print("╚═════════════════════════════════════════════════════════════════════════════╝")


def print_yearly_ascii_chart(yearly_data):
    """Print yearly contribution as ASCII timeline"""
    if not yearly_data:
        return
    
    max_prs = max(yearly_data.values()) if yearly_data else 1
    total = sum(yearly_data.values())
    
    print("""
╔═════════════════════════════════════════════════════════════════════════════╗
║                       📅 YEARLY CONTRIBUTION TIMELINE                       ║
╠═════════════════════════════════════════════════════════════════════════════╣""")
    
    for year in sorted(yearly_data.keys()):
        count = yearly_data[year]
        bar = create_ascii_bar(count, max_prs, width=40, fill_char="▓", empty_char="░")
        percentage = (count / total * 100) if total > 0 else 0
        print(f"║   {year} │ {bar} │ {count:>4} PRs ({percentage:>5.1f}%)  ║")
    
    print(f"╠═════════════════════════════════════════════════════════════════════════════╣")
    print(f"║   TOTAL: {total:>4} PRs                                                          ║")
    print(f"╚═════════════════════════════════════════════════════════════════════════════╝")


def print_repo_distribution_chart(repo_data, top_n=5):
    """Print top repositories contribution"""
    if not repo_data:
        return
    
    top_repos = dict(sorted(repo_data.items(), key=lambda x: -x[1])[:top_n])
    max_count = max(top_repos.values()) if top_repos else 1
    
    print(f"""
╔═════════════════════════════════════════════════════════════════════════════╗
║                     🏆 TOP {top_n} CONTRIBUTED REPOSITORIES                       ║
╠═════════════════════════════════════════════════════════════════════════════╣""")
    
    medals = ["🥇", "🥈", "🥉", "4️⃣", "5️⃣"]
    
    for i, (repo, count) in enumerate(top_repos.items()):
        display_repo = repo if len(repo) <= 30 else repo[:27] + "..."
        bar = create_ascii_bar(count, max_count, width=25, fill_char="▓", empty_char="░")
        medal = medals[i] if i < 5 else f"{i+1}."
        print(f"║  {medal} {display_repo:<30} │ {bar} │ {count:>4} PRs ║")
    
    print(f"╚═════════════════════════════════════════════════════════════════════════════╝")


def print_activity_heatmap(monthly_data):
    """Print monthly activity as heatmap-style visualization"""
    if not monthly_data:
        return
    
    max_count = max(monthly_data.values()) if monthly_data else 1
    
    print("""
╔═════════════════════════════════════════════════════════════════════════════╗
║                         📆 MONTHLY ACTIVITY HEATMAP                         ║
╠═════════════════════════════════════════════════════════════════════════════╣""")
    
    years = {}
    for month, count in monthly_data.items():
        year = month[:4]
        if year not in years:
            years[year] = {}
        years[year][month[5:7]] = count
    
    print("║       │ Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec │ Total   ║")
    print("║  ─────┼─────────────────────────────────────────────────┼───────  ║")
    
    for year in sorted(years.keys()):
        row = f"║  {year} │ "
        year_total = 0
        for m in ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]:
            count = years[year].get(m, 0)
            year_total += count
            if count == 0:
                row += " ·  "
            elif count < max_count * 0.25:
                row += " ░  "
            elif count < max_count * 0.5:
                row += " ▒  "
            elif count < max_count * 0.75:
                row += " ▓  "
            else:
                row += " █  "
        row += f"│  {year_total:>4}   ║"
        print(row)
    
    print("║  ─────┴─────────────────────────────────────────────────┴───────  ║")
    print("║  Legend: · = 0  ░ = Low  ▒ = Medium  ▓ = High  █ = Peak           ║")
    print(f"╚═════════════════════════════════════════════════════════════════════════════╝")


def print_detailed_breakdown(type_categories, tool_categories):
    """Print detailed breakdown of PRs by type and tool"""
    
    print("""
╔═════════════════════════════════════════════════════════════════════════════╗
║                       📋 DETAILED PR BREAKDOWN BY TYPE                      ║
╚═════════════════════════════════════════════════════════════════════════════╝""")
    
    for pr_type, pr_list in sorted(type_categories.items(), key=lambda x: -len(x[1])):
        print(f"\n┌─── {pr_type} ({len(pr_list)} PRs) ───────────────────────────────────────────────")
        print("│")
        
        for pr in pr_list[:5]:
            repo_url = safe_str(pr.get("repository_url"), "")
            repo = repo_url.split("/")[-1] if repo_url else "unknown"
            if len(repo) > 15:
                repo = repo[:12] + "..."
            
            title = safe_str(pr.get("title"), "No title")
            if len(title) > 35:
                title = title[:32] + "..."
            
            state = safe_str(pr.get("state"), "unknown")
            pr_data = pr.get("pull_request") or {}
            tool = pr.get("_detected_tool", "Unknown")
            
            if state == "open":
                state_emoji = "⏳"
            elif pr_data.get("merged_at"):
                state_emoji = "✅"
            else:
                state_emoji = "❌"
            
            pr_number = safe_int(pr.get("number"), 0)
            print(f"│  {state_emoji} #{pr_number:<5} [{repo:<15}] {title}")
        
        if len(pr_list) > 5:
            print(f"│")
            print(f"│  📌 ... and {len(pr_list) - 5} more PRs of this type")
        
        print(f"│")
        print(f"└───────────────────────────────────────────────────────────────────────────")


# -------------------------
# Detailed Scan Feature
# -------------------------

def perform_detailed_scan(prs, username, stats):
    """Perform detailed analysis with visualizations"""
    
    print("\n╔═════════════════════════════════════════════════════════════════════════════╗")
    print(f"║              🔬 DETAILED PR ANALYSIS FOR @{username.upper():<32} ║")
    print("╚═════════════════════════════════════════════════════════════════════════════╝")
    
    type_categories, tool_categories = categorize_prs_animated(prs)
    type_counts = {k: len(v) for k, v in type_categories.items()}
    tool_counts = {k: len(v) for k, v in tool_categories.items()}
    
    time.sleep(0.3)
    print_ascii_flow_chart(stats)
    
    time.sleep(0.3)
    print_productivity_ascii_chart(stats)
    
    time.sleep(0.3)
    print_type_distribution_chart(type_counts)
    
    time.sleep(0.3)
    print_tool_distribution_chart(tool_counts)
    
    time.sleep(0.3)
    print_yearly_ascii_chart(stats['yearly'])
    
    time.sleep(0.3)
    print_activity_heatmap(stats['monthly'])
    
    time.sleep(0.3)
    print_repo_distribution_chart(stats['repo_counter'], top_n=5)
    
    time.sleep(0.3)
    print_detailed_breakdown(type_categories, tool_categories)
    
    return type_categories, tool_categories, type_counts, tool_counts


# -------------------------
# Export Engine
# -------------------------

def show_saving_progress(message="Saving your report"):
    """Show animated saving progress"""
    print(f"\n   💾 {message}...")
    for i in range(0, 101, 5):
        bar = "█" * (i // 5) + "░" * (20 - i // 5)
        sys.stdout.write(f"\r   [{bar}] {i}%")
        sys.stdout.flush()
        time.sleep(0.03)
    print()


def export_markdown(username, stats, type_counts, tool_counts, type_categories, filename, graph_path=None):
    """Export full report as Markdown"""
    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"# 📊 GitHub PR Report for @{username}\n\n")
        f.write(f"**Generated on:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"**Operating System:** {get_os_name()}\n\n")
        f.write("---\n\n")
        
        f.write("## 📈 Summary\n\n")
        f.write(f"| Metric | Value |\n")
        f.write(f"|--------|-------|\n")
        f.write(f"| Total PRs | {stats['total']} |\n")
        f.write(f"| ✅ Merged | {stats['merged']} |\n")
        f.write(f"| ⏳ Pending | {stats['pending']} |\n")
        f.write(f"| ❌ Closed | {stats['closed']} |\n")
        f.write(f"| 📝 Draft | {stats['draft']} |\n")
        f.write(f"| ⚠️ Stale (>180d open) | {stats['stale']} |\n")
        f.write(f"| 📈 Acceptance Rate | {stats['acceptance']}% |\n")
        f.write(f"| 🏆 Top Repo | {safe_str(stats['top_repo'], 'N/A')} |\n\n")
        
        if graph_path:
            f.write("## 📊 Visual Analysis\n\n")
            f.write(f"![PR Analysis Graph]({os.path.basename(graph_path)})\n\n")
        
        # PR Types
        if type_counts:
            f.write("## 📋 PR Types Distribution\n\n")
            f.write("| Type | Count | Percentage |\n")
            f.write("|------|-------|------------|\n")
            total = sum(type_counts.values())
            for pr_type, count in sorted(type_counts.items(), key=lambda x: -x[1]):
                pct = (count / total * 100) if total > 0 else 0
                f.write(f"| {pr_type} | {count} | {pct:.1f}% |\n")
            f.write("\n")
        
        # Tools Used
        if tool_counts:
            f.write("## 🛠️ Tools Used to Create PRs\n\n")
            f.write("| Tool | Count | Percentage |\n")
            f.write("|------|-------|------------|\n")
            total = sum(tool_counts.values())
            for tool, count in sorted(tool_counts.items(), key=lambda x: -x[1]):
                pct = (count / total * 100) if total > 0 else 0
                f.write(f"| {tool} | {count} | {pct:.1f}% |\n")
            f.write("\n")
        
        # Yearly
        if stats['yearly']:
            f.write("## 📅 Yearly Contributions\n\n")
            f.write("```\n")
            max_prs = max(stats['yearly'].values()) if stats['yearly'] else 1
            for year, count in sorted(stats['yearly'].items()):
                bar_len = int((count / max_prs) * 30) if max_prs > 0 else 0
                bar = "█" * bar_len + "░" * (30 - bar_len)
                f.write(f"{year} │ {bar} │ {count} PRs\n")
            f.write("```\n\n")
        
        # Top Repos
        if stats['repo_counter']:
            f.write("## 🏆 Top Contributed Repositories\n\n")
            top_repos = sorted(stats['repo_counter'].items(), key=lambda x: -x[1])[:10]
            f.write("| # | Repository | PRs |\n")
            f.write("|---|------------|-----|\n")
            for i, (repo, count) in enumerate(top_repos, 1):
                f.write(f"| {i} | {repo} | {count} |\n")
            f.write("\n")
        
        f.write("---\n")
        f.write("\n*Report generated by GitHub PR Checker* 🚀\n")


# -------------------------
# Display Stats
# -------------------------

def display_stats(stats, username):
    """Display PR statistics in a formatted table"""
    
    top_repo_display = safe_str(stats.get('top_repo'), 'No repositories')
    if len(top_repo_display) > 50:
        top_repo_display = top_repo_display[:47] + "..."
    
    print("\n╔═════════════════════════════════════════════════════════════════════════════╗")
    print(f"║                    📊 PR STATISTICS FOR @{username.upper():<33} ║")
    print("╠═════════════════════════════════════════════════════════════════════════════╣")
    print(f"║                                                                             ║")
    print(f"║   Total PRs           : {stats['total']:>6}                                           ║")
    print(f"║   ─────────────────────────────────────────────────────────────────────     ║")
    print(f"║   ✅ Merged            : {stats['merged']:>6}                                           ║")
    print(f"║   ⏳ Pending           : {stats['pending']:>6}                                           ║")
    print(f"║   ❌ Closed            : {stats['closed']:>6}                                           ║")
    print(f"║   📝 Draft             : {stats['draft']:>6}                                           ║")
    print(f"║   ⚠️  Stale (>180d)     : {stats['stale']:>6}                                           ║")
    print(f"║   ─────────────────────────────────────────────────────────────────────     ║")
    print(f"║   📈 Acceptance Rate   : {stats['acceptance']:>6}%                                          ║")
    print(f"║   🏆 Top Repository    : {top_repo_display:<50} ║")
    print(f"║                                                                             ║")
    print("╚═════════════════════════════════════════════════════════════════════════════╝")
    
    if stats["yearly"]:
        print("\n╔═════════════════════════════════════════════════════════════════════════════╗")
        print("║                          📅 YEARLY CONTRIBUTIONS                            ║")
        print("╠═════════════════════════════════════════════════════════════════════════════╣")
        max_yearly = max(stats["yearly"].values()) if stats["yearly"] else 1
        for year, count in sorted(stats["yearly"].items()):
            bar = create_ascii_bar(count, max_yearly, width=40)
            print(f"║   {year} │ {bar} │ {count:>4} PRs           ║")
        print("╚═════════════════════════════════════════════════════════════════════════════╝")


# -------------------------
# Scan Handler
# -------------------------

def run_scan(scan_type, token):
    """Run a PR scan (quick or deep)"""
    
    print("\n╔═════════════════════════════════════════════════════════════════════════════╗")
    print("║                         ENTER GITHUB USERNAME                               ║")
    print("╚═════════════════════════════════════════════════════════════════════════════╝")
    
    username = input("\n   👤 GitHub Username: ").strip()
    
    if not username:
        print("\n   ❌ Username cannot be empty!")
        return
    
    valid, user_data = verify_username(username, token)
    if not valid:
        return
    
    prs = fetch_all_prs_animated(username, token)
    
    if not prs:
        print(f"\n   ❌ No PRs found for @{username}")
        return
    
    stats = analyze_prs_animated(prs, username)
    display_stats(stats, username)
    
    type_categories = {}
    tool_categories = {}
    type_counts = {}
    tool_counts = {}
    graph_path = None
    
    if scan_type == "deep":
        print("\n   🔬 Running DETAILED SCAN with ASCII visualizations...")
        type_categories, tool_categories, type_counts, tool_counts = perform_detailed_scan(prs, username, stats)
    else:
        type_categories, tool_categories = categorize_prs_animated(prs)
        type_counts = {k: len(v) for k, v in type_categories.items()}
        tool_counts = {k: len(v) for k, v in tool_categories.items()}
    
    # Ask for graph generation
    if MATPLOTLIB_AVAILABLE:
        graph_choice = input("\n   📊 Generate matplotlib graph (your-graph-by-cp.png)? (y/n): ").strip().lower()
        
        if graph_choice in ['y', 'yes']:
            print("\n   📁 Where would you like to save the graph?")
            print(f"      [1] Current Directory: {os.getcwd()}")
            print(f"      [2] Desktop: {get_desktop_path()}")
            print(f"      [3] Documents: {get_documents_path()}")
            print(f"      [4] Custom path")
            
            loc_choice = input("\n   Enter choice (1-4): ").strip()
            
            if loc_choice == "2":
                save_path = get_desktop_path()
            elif loc_choice == "3":
                save_path = get_documents_path()
            elif loc_choice == "4":
                save_path = input("   Enter custom path: ").strip()
            else:
                save_path = os.getcwd()
            
            if not os.path.exists(save_path):
                try:
                    os.makedirs(save_path)
                except Exception as e:
                    print(f"   ⚠️  Could not create directory: {e}")
                    save_path = os.getcwd()
            
            graph_path = generate_graphs(username, stats, type_counts, tool_counts, save_path)
    
    # Ask to save report
    save_choice = input("\n   💾 Save complete report as Markdown? (y/n): ").strip().lower()
    
    if save_choice in ['y', 'yes']:
        print("\n   📁 Where would you like to save the report?")
        print(f"      [1] Current Directory: {os.getcwd()}")
        print(f"      [2] Desktop: {get_desktop_path()}")
        print(f"      [3] Documents: {get_documents_path()}")
        print(f"      [4] Custom path")
        
        loc_choice = input("\n   Enter choice (1-4): ").strip()
        
        if loc_choice == "2":
            save_path = get_desktop_path()
        elif loc_choice == "3":
            save_path = get_documents_path()
        elif loc_choice == "4":
            save_path = input("   Enter custom path: ").strip()
        else:
            save_path = os.getcwd()
        
        if not os.path.exists(save_path):
            try:
                os.makedirs(save_path)
            except Exception as e:
                print(f"   ⚠️  Could not create directory: {e}")
                save_path = os.getcwd()
        
        default_name = f"{username}_pr_report.md"
        print(f"\n   📝 Enter filename (press Enter for default: '{default_name}')")
        filename = input("      Filename: ").strip()
        
        if not filename:
            filename = default_name
        
        if not filename.endswith('.md'):
            filename += '.md'
        
        full_path = os.path.join(save_path, filename)
        
        show_saving_progress("Generating report")
        
        try:
            export_markdown(username, stats, type_counts, tool_counts, type_categories, full_path, graph_path)
            
            print("\n╔═════════════════════════════════════════════════════════════════════════════╗")
            print("║                       ✅ REPORT SAVED SUCCESSFULLY                          ║")
            print("╠═════════════════════════════════════════════════════════════════════════════╣")
            print("║                                                                             ║")
            print("║   🎉 Your report has been saved successfully!                               ║")
            print("║                                                                             ║")
            
            display_filename = filename if len(filename) <= 55 else filename[:52] + "..."
            display_path = save_path if len(save_path) <= 55 else save_path[:52] + "..."
            
            print(f"║   📄 Report : {display_filename:<60} ║")
            print(f"║   📁 Path   : {display_path:<60} ║")
            
            if graph_path:
                print(f"║   📊 Graph  : your-graph-by-cp.png                                          ║")
            
            print("║                                                                             ║")
            print("╚═════════════════════════════════════════════════════════════════════════════╝")
            
        except Exception as e:
            print(f"\n   ❌ Error saving report: {e}")
    else:
        print("\n   📌 Report not saved.")
    
    print("\n   ✨ Scan completed successfully!")
    input("\n   Press Enter to return to main menu...")


# -------------------------
# Main Application Loop
# -------------------------

def main():
    """Main application with loop"""
    
    token = get_github_token()
    
    while True:
        print_header()
        
        if token:
            print("   🔑 GitHub Token: Found ✅")
        else:
            print("   🔑 GitHub Token: Not found (limited to 60 requests/hour)")
            print("       Set GITHUB_TOKEN environment variable for higher limits")
        
        if not check_rate_limit(token):
            print("\n   ❌ API rate limit exceeded. Please try again later.")
            input("\n   Press Enter to continue...")
            continue
        
        show_main_menu()
        
        choice = input("\n   Enter your choice (1-4): ").strip()
        
        if choice == "1":
            run_scan("quick", token)
        
        elif choice == "2":
            run_scan("deep", token)
        
        elif choice == "3":
            show_system_info()
            input("\n   Press Enter to return to main menu...")
        
        elif choice == "4":
            print("\n╔═════════════════════════════════════════════════════════════════════════════╗")
            print("║                                                                             ║")
            print("║              👋 Thank you for using GitHub PR Checker!                      ║")
            print("║                                                                             ║")
            print("║              ⭐ Star us on GitHub if you found this helpful!                ║")
            print("║                                                                             ║")
            print("╚═════════════════════════════════════════════════════════════════════════════╝")
            print("\n   Goodbye! 👋\n")
            break
        
        else:
            print("\n   ❌ Invalid choice. Please enter 1, 2, 3, or 4.")
            input("\n   Press Enter to continue...")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n   ⚠️  Interrupted by user.")
        print("   👋 Goodbye!\n")
    except Exception as e:
        print(f"\n\n   ❌ An error occurred: {e}")
        import traceback
        print("\n   Debug info:")
        traceback.print_exc()
        print("\n   Please check your internet connection and try again.\n")
