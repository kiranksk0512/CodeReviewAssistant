import json
import re

# Load JSON data from file
with open("data/json/pull_request_data.json", "r") as file:
    data = json.load(file)

# Function to retrieve description based on diff_file
def get_description_by_diff_file(data, diff_file):
    diff_file = "raw/"+diff_file
    for key in data.keys():
        value = data.get(key)
        if (value.get("prs") != []):
            for prs in value.get("prs"):
                if (prs.get("diff_file") == diff_file):
                    return extract_jira_ids(prs.get("pr_data").get("title"))
    return None

def extract_jira_ids(text):
    # Define the pattern to match JIRA IDs
    pattern = r'\b[A-Z]+-[0-9]+\b'

    # Use findall to extract all occurrences of the pattern
    jira_ids = re.findall(pattern, text)

    return jira_ids

# Example usage
# diff_file = "raw/2f84d3ff7ac27b61e97c85aae14d44ee254e2490_pr_6364_diff.txt"
# description = get_description_by_diff_file(data, diff_file)
# linked_jiras = extract_jira_ids(description)
# print(linked_jiras)

