<div align="center">

# check_pr - GitHub Pull Request Tracker

> 🚀 A simple Python tool to check all Pull Requests created by a GitHub user across all their repositories.

[![Python](https://img.shields.io/badge/Python-3.6%2B-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![No Dependencies](https://img.shields.io/badge/Dependencies-None-success.svg)]()

</div>

---

## 📋 Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Example Output](#example-output)
- [How It Works](#how-it-works)
- [Limitations](#limitations)
- [Contributing](#contributing)
- [License](#license)

---

<a name="features"></a>
## ✨ Features

<table>
<tr>
<td>✅ <b>Zero Dependencies</b></td>
<td>Uses only Python standard library</td>
</tr>
<tr>
<td>✅ <b>No API Token Required</b></td>
<td>Works without authentication</td>
</tr>
<tr>
<td>✅ <b>Comprehensive Statistics</b></td>
<td>Shows merged, pending, and closed PRs</td>
</tr>
<tr>
<td>✅ <b>All Repositories</b></td>
<td>Scans across all user's repositories</td>
</tr>
<tr>
<td>✅ <b>Detailed Reports</b></td>
<td>Optional detailed PR list with links</td>
</tr>
<tr>
<td>✅ <b>Easy to Use</b></td>
<td>Simple command-line interface</td>
</tr>
</table>

---

<a name="prerequisites"></a>
## 📦 Prerequisites

<div align="left">

| Requirement | Description |
|------------|-------------|
| 🐍 Python | Version 3.6 or higher |
| 🌐 Internet | Active connection |
| 👤 GitHub Username | Valid username to check |

</div>

**That's it! No additional packages needed.**

---

<a name="installation"></a>
## 🔧 Installation

### Method 1: Clone the Repository

```bash
# Clone this repository
git clone https://github.com/Chintanpatel24/check_pr.git

# Navigate to the directory
cd check_pr

# Run the script
python check_pr.py

```
## Method 2: Download Directly
1. Download total_pr_checker.py from this repository
2. Save it to your desired location
3. Run it with Python

```bash
python check_pr.py

```
## Method 3: Quick Download (Using wget or curl)

1. Using wget:

```bash

# Download the script
wget https://raw.githubusercontent.com/yourusername/check_pr/main/check_pr.py

# Run it
python check_pr.py

```

2. Using curl:

```bash

# Download the script
curl -O https://raw.githubusercontent.com/yourusername/check_pr/main/check_pr.py

# Run it
python check_pr.py

```

3. One-Line Install & Run:

```bash

# Download and run in one command
curl -O https://raw.githubusercontent.com/yourusername/check_pr/main/check_pr.py && python check_pr.py

```

---

## 🔑 Optional: Setup GitHub Token

- For higher API limits (5000 requests/hour instead of 60):

Step 1: Create a Personal Access Token at GitHub Settings

Step 2: Create a .env file in the same directory:

```bash
GITHUB_TOKEN=your_token_here
```

Step 3: The script will automatically detect and use it

---

<a name="usage"></a>
## 🚀 Usage
- Starting the Tool
 
```bash

python check_pr.py

```

- Main Menu
```
text

======================================================================
  GITHUB TOTAL PR CHECKER
  Check all PRs by a user across all their repositories
======================================================================

Select a method:
1. Check all repositories owned by a user (Method 1)
2. Check a specific repository (Method 2)
3. Check multiple specific repositories (Method 3)
4. Show help
5. Exit

Enter your choice (1-5):

```

## Method 1: Check All Repositories
Best for: Getting complete PR statistics across all user's repos
```
text

Enter your choice (1-5): 1
👤 Enter GitHub username: Chintanpatel24
```

The script will:

✅ Fetch all repositories owned by the user

✅ Scan each repository for PRs

✅ Display total statistics

✅ Optionally show detailed list or export

## Method 2: Check Single Repository
Best for: Checking PRs in one specific repository
```
text

Enter your choice (1-5): 2

👤 Enter GitHub username: gaearon
🏢 Enter repository owner: facebook
📁 Enter repository name: react
```
The script will:

✅ Check only the specified repository

✅ Show PRs created by the user in that repo

✅ Display statistics

## Method 3: Check Multiple Specific Repositories
Best for: Checking PRs in selected repositories only
```
text

Enter your choice (1-5): 3

👤 Enter GitHub username: gaearon

📁 Enter repositories to check (one per line, format: owner/repo)
   Example: facebook/react
   Enter 'done' when finished:

Repository: facebook/react
Repository: reduxjs/redux
Repository: facebook/create-react-app
Repository: done
```
The script will:

✅ Check only the repositories you specified

✅ Show combined statistics

✅ Display detailed list if requested

- Export Options
After scanning, you can:
```
text

What would you like to do?
1. Show detailed PR list
2. Export to JSON
3. Export to CSV
4. All of the above
5. Exit

Enter your choice (1-5):
```
---

