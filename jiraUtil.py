import requests
from requests.auth import HTTPBasicAuth
import json
import csv


JIRA_INSTANCE = "https://jiraisa.atlassian.net"
TOKEN = "<pasteTokenHere>"

JIRA_ISSUE_URL = '{}/rest/api/2/issue/{}'
JIRA_COMMITS_URL = '{}/rest/dev-status/latest/issue/detail?issueId={}&applicationType=bitbucket&dataType=repository'

class JiraEntry:
    def __init__(self, key=None, description="", summary="", commits=[], parent=None, children=None, status=None):
        self.key = key
        self.description = description
        self.summary = summary
        self.commits = commits
        self.parent = parent
        self.children = children
        self.status = status


class JiraService:
    def __init__(self):
        self.headers = {
            'Authorization': f"Basic {TOKEN}",
            "Accept": "application/json"
        }

    def get(self, keys):
        jiras = []
        for k in keys:
            print(f"retrieving jira - {k}")
            jira = self.jira(k, False, None)
            jiras.append(jira)
        return jiras

    def jira(self, jira, summary, parent_entry):

        url = JIRA_ISSUE_URL.format(JIRA_INSTANCE, jira)
        response_raw = requests.get(url, headers=self.headers)
        jira_entry = JiraEntry()
        if response_raw.status_code == 200:
            try:
                response = json.loads(response_raw.text)
                # print(response)
                jira_id = response.get("id")
                key = response.get("key")
                jira_summary = response["fields"]["summary"]
                jira_status = response["fields"]["status"]["name"]
                commits = []
                sub_tasks = []
                parent = None
                if not summary:
                    commits = self.commits(jira_id)
                description = response["fields"]["description"]
                
                if "parent" in response["fields"].keys():
                    parent_jira = response["fields"].get("parent")
                    if parent_jira is not None:
                        if parent_entry is None:
                            parent = self.jira(parent_jira["key"], True, None)

                if parent_entry is not None:
                    parent = parent_entry

                if "subtasks" in response["fields"].keys():
                    for s in response["fields"]["subtasks"]:
                        sub_tasks.append(self.jira(s["key"], True, jira_entry))

                jira_entry.key = key
                jira_entry.summary = jira_summary
                jira_entry.description = description
                jira_entry.commit = commits
                jira_entry.parent = parent
                jira_entry.children = sub_tasks
                jira_entry.status = jira_status
                return jira_entry
            except (json.JSONDecodeError, KeyError) as e:
                print(f"Error parsing JSON response: {e}")
                return None
        else:
            print(f"Error retrieving issue: {response_raw.status_code}")
            return None

    def commits(self, id):
        url = JIRA_COMMITS_URL.format(JIRA_INSTANCE, id)
        response_raw = requests.get(url, headers=self.headers)
        response = json.loads(response_raw.text)
        commits = []
        if "detail" in response.keys():
            for d in response["detail"]:
                for r in d["repositories"]:
                    for c in r["commits"]:
                        commits.append(c["id"])
        return commits
