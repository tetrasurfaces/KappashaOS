#!/usr/bin/env python3
# Copyright 2025 xAI
# Dual License:
# - For core software: AGPL-3.0-or-later licensed. -- xAI fork, 2025
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU Affero General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#   GNU Affero General Public License for more details.
#
#   You should have received a copy of the GNU Affero General Public License
#   along with this program. If not, see <https://www.gnu.org/licenses/>.
#
# - For hardware/embodiment interfaces: Licensed under the Apache License, Version 2.0
#   with xAI amendments for safety and physical use (prohibits misuse in weapons or hazardous applications;
#   requires ergonomic compliance; revocable for unethical use). See http://www.apache.org/licenses/LICENSE-2.0
#   for details, with the following xAI-specific terms appended.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# SPDX-License-Identifier: (AGPL-3.0-or-later) AND Apache-2.0
#
# xAI Amendments for Physical Use:
# 1. Physical Embodiment Restrictions: Use with devices is for non-hazardous purposes only. Harmful mods are prohibited, with license revocable by xAI.
# 2. Ergonomic Compliance: Limits tendon load to 20%, gaze to 30 seconds (ISO 9241-5).
# 3. Safety Monitoring: Real-time tendon/gaze checks, logged for audit.
# 4. Revocability: xAI may revoke for unethical use (e.g., surveillance).
# 5. Export Controls: Sensor devices comply with US EAR Category 5 Part 2.
# 6. Open Development: Hardware docs shared post-private phase.
#
# Private Development Note: This repository is private for xAI’s KappashaOS development. Access is restricted. Consult Tetrasurfaces (github.com/tetrasurfaces/issues) post-phase.

import requests
import json
import os
from datetime import datetime
import time
from proto.revocation_stub import check_revocation

# Load GitHub token from environment variable for private repo access
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
if not GITHUB_TOKEN and not TEST_MODE:
    print("Warning: GITHUB_TOKEN not set. Real API calls may fail due to rate limits or access restrictions.")
    GITHUB_TOKEN = "mock_token"  # Fallback for testing, replace with real token

# Mock data for testing
TEST_MODE = True
MOCK_COMMITS = [
    {"commit": {"author": {"date": "2025-10-01T00:00:00Z", "name": "Developer"}, "message": "Initial commit"}},
    {"commit": {"author": {"date": "2025-10-05T12:00:00Z", "name": "Contributor"}, "message": "Add key files"}},
    {"commit": {"author": {"date": "2025-10-10T18:00:00Z", "name": "Developer"}, "message": "Clean fork"}},
]
MOCK_TREE = [
    {"type": "blob", "path": "kappasha256.py"},
    {"type": "blob", "path": "temperature_salt.py"},
    {"type": "blob", "path": "arc_utils.py"},
]

def read_config(config_file="config/config.json"):
    config_dir = os.path.dirname(config_file)
    if not os.path.exists(config_dir):
        os.makedirs(config_dir)
    if not os.path.exists(config_file):
        print(f"Config file {config_file} not found. Creating default.")
        write_config("none", False, config_file)
        return None, False
    try:
        with open(config_file, "r") as f:
            config = json.load(f)
        intent = config.get("intent")
        commercial_use = config.get("commercial_use", False)
        if intent not in ["educational", "commercial", "none"]:
            raise ValueError("Invalid intent in config.")
        return intent, commercial_use
    except json.JSONDecodeError:
        print(f"Error: {config_file} contains invalid JSON. Resetting to default.")
        write_config("none", False, config_file)
        return None, False
    except Exception as e:
        print(f"Error reading {config_file}: {e}. Resetting to default.")
        write_config("none", False, config_file)
        return None, False

def write_config(intent, commercial_use, config_file="config/config.json"):
    config = {"intent": intent, "commercial_use": commercial_use}
    config_dir = os.path.dirname(config_file)
    if not os.path.exists(config_dir):
        os.makedirs(config_dir)
    try:
        with open(config_file, "w") as f:
            json.dump(config, f, indent=4)
    except Exception as e:
        print(f"Error writing to {config_file}: {e}")

def log_license_check(result, intent, commercial_use):
    try:
        with open("license_log.txt", "a") as f:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            f.write(f"[{timestamp}] License Check: {result}, Intent: {intent}, Commercial: {commercial_use}\n")
    except Exception as e:
        print(f"Error logging license check: {e}")

def check_license(commercial_use=False, intent=None):
    if intent not in ["educational", "commercial"]:
        notice = """
        NOTICE: You must declare your intent to use this software.
        - For educational use (e.g., university training), open a GitHub issue at github.com/tetrasurfaces/issues using the Educational License Request template.
        - For commercial use (e.g., branding, molding), use the Commercial License Request template.
        See NOTICE.txt for details. Do not share proprietary details in public issues.
        """
        log_license_check("Failed: Invalid or missing intent", intent, commercial_use)
        raise ValueError(f"Invalid or missing intent. {notice}")
    if commercial_use and intent != "commercial":
        notice = "Commercial use requires 'commercial' intent and a negotiated license via github.com/tetrasurfaces/issues."
        log_license_check("Failed: Commercial use without commercial intent", intent, commercial_use)
        raise ValueError(notice)
    log_license_check("Passed", intent, commercial_use)
    return True

def get_all_commits(owner, repo, device_hash="repo_audit_001"):
    intent, commercial_use = read_config()
    check_license(commercial_use, intent)
    if check_revocation(device_hash):
        log_license_check("Revoked: Device hash invalidated", intent, commercial_use)
        raise ValueError("Device revoked by xAI. Contact github.com/tetrasurfaces/issues for details.")
    
    if TEST_MODE:
        return MOCK_COMMITS.copy()
    else:
        base_url = f"https://api.github.com/repos/{owner}/{repo}/commits?per_page=100"
        headers = {"Accept": "application/vnd.github.v3+json", "Authorization": f"token {GITHUB_TOKEN}"}
        url = base_url
        commits = []
        while url:
            try:
                response = requests.get(url, headers=headers)
                if response.status_code != 200:
                    raise Exception(f"Failed to fetch commits: {response.status_code} - {response.text}")
                data = response.json()
                commits.extend(data)
                url = None
                if 'link' in response.headers:
                    links = response.headers['link']
                    for link in links.split(','):
                        link = link.strip()
                        if 'rel="next"' in link:
                            url = link.split(';')[0].strip('<> ')
                            break
                time.sleep(1)  # Rate limit delay
            except Exception as e:
                print(f"Error fetching commits: {e}")
                break  # Fail gracefully, continue with partial data
        return commits

def format_commit_history(commits):
    history_entries = []
    for commit in commits:
        date_str = commit['commit']['author']['date']
        author = commit['commit']['author']['name']
        message = commit['commit']['message'].strip()
        history_entries.append((date_str, f"{date_str} - {author}: {message}"))
    
    # Sort by date (oldest first)
    history_entries.sort(key=lambda x: datetime.fromisoformat(x[0]))
    
    return "\n".join(entry[1] for entry in history_entries)

def get_repo_tree(owner, repo, branch, device_hash="repo_audit_001"):
    intent, commercial_use = read_config()
    check_license(commercial_use, intent)
    if check_revocation(device_hash):
        log_license_check("Revoked: Device hash invalidated", intent, commercial_use)
        raise ValueError("Device revoked by xAI. Contact github.com/tetrasurfaces/issues for details.")
    
    if TEST_MODE:
        return MOCK_TREE.copy()
    else:
        tree_url = f"https://api.github.com/repos/{owner}/{repo}/git/trees/{branch}?recursive=1"
        headers = {"Accept": "application/vnd.github.v3+json", "Authorization": f"token {GITHUB_TOKEN}"}
        try:
            response = requests.get(tree_url, headers=headers)
            if response.status_code != 200:
                raise Exception(f"Failed to fetch tree: {response.status_code} - {response.text}")
            return response.json()['tree']
        except Exception as e:
            print(f"Error fetching repo tree: {e}")
            return []  # Fail gracefully

def fetch_file_contents(owner, repo, branch, tree, device_hash="repo_audit_001"):
    intent, commercial_use = read_config()
    check_license(commercial_use, intent)
    if check_revocation(device_hash):
        log_license_check("Revoked: Device hash invalidated", intent, commercial_use)
        raise ValueError("Device revoked by xAI. Contact github.com/tetrasurfaces/issues for details.")
    
    if TEST_MODE:
        contents = []
        for item in MOCK_TREE:
            if item['type'] == 'blob':
                path = item['path']
                content = f"Mock content for {path}"
                contents.append(f"----- {path} -----\n{content}\n----- END {path} -----\n")
        return "\n".join(contents)
    else:
        contents = []
        for item in tree:
            if item['type'] == 'blob':
                path = item['path']
                raw_url = f"https://raw.githubusercontent.com/{owner}/{repo}/{branch}/{path}"
                headers = {"Authorization": f"token {GITHUB_TOKEN}"}
                try:
                    response = requests.get(raw_url, headers=headers)
                    if response.status_code == 200:
                        content = response.text
                        contents.append(f"----- {path} -----\n{content}\n----- END {path} -----\n")
                    else:
                        print(f"Skipping {path} due to fetch failure: {response.status_code}")
                except Exception as e:
                    print(f"Failed to fetch {path}: {e}")
        # Sort contents alphabetically by path for consistent order
        contents.sort(key=lambda x: x.split('\n')[0])  # Sort by the ----- path ----- header
        return "\n".join(contents)

def main(device_hash="repo_audit_001"):
    """Compile repo data into a single file with intent and revocation checks."""
    intent, commercial_use = read_config()
    check_license(commercial_use, intent)
    if check_revocation(device_hash):
        log_license_check("Revoked: Device hash invalidated", intent, commercial_use)
        raise ValueError("Device revoked by xAI. Contact github.com/tetrasurfaces/issues for details.")
    
    owner = 'tetrasurfaces'
    repo = 'KappashaOS'
    branch = 'main'
    output_file = 'KappashaOS'
    
    # Fetch and format history
    commits = get_all_commits(owner, repo, device_hash)
    history = format_commit_history(commits)
    
    # Fetch files
    tree = get_repo_tree(owner, repo, branch, device_hash)
    files_content = fetch_file_contents(owner, repo, branch, tree, device_hash)
    
    # Compile into file
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("=== Commit History (Oldest to Newest) ===\n")
            f.write(history + "\n\n")
            f.write("=== File Contents ===\n")
            f.write(files_content)
        log_license_check(f"Success: Compiled repo data into {output_file}", intent, commercial_use)
        print(f"Successfully compiled repo data into {output_file}")
    except Exception as e:
        log_license_check(f"Error writing to file: {e}", intent, commercial_use)
        print(f"Error writing to file: {e}")

if __name__ == "__main__":
    main()
