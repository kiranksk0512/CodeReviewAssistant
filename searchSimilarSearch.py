import json
from generate_pr_data import get_description_by_diff_file
from langchain_community.embeddings.openai import OpenAIEmbeddings
from langchain_community.vectorstores.chroma import Chroma


def parse_git_diff(diff_text):
    file_changes = []
    current_file = None
    added_lines = []
    deleted_lines = []
    parent_jira_id = ""

    for line in diff_text.split('\n'):
        if line.startswith('diff --git'):
            print("startWith")
            if current_file is not None:
                print("currentFile Not NOne")
                # Check if the current file contains "DAO" or ".xml" in its name
                if 'DAO' not in current_file and '.xml' not in current_file:
                    print("DAO not in current file")
                    file_changes.append((current_file, added_lines, deleted_lines, parent_jira_id))
            print("outside")
            current_file = line.split(' ')[-1][2:]
            added_lines = []
            deleted_lines = []
            parent_jira_id = ""
        elif line.startswith('@@'):
            continue
        elif line.startswith('+'):
            if line[1:] != '':
                added_lines.append(line[1:])
        elif line.startswith('-'):
            if line[1:] != '':
                deleted_lines.append(line[1:])
        elif line.startswith("index "):
            parent_commit_id = line.split()[1].split("..")[0]
            parent_jira_id = parent_commit_id

    if current_file is not None:
        # Check if the last file contains "DAO" or ".xml" in its name
        if 'DAO' not in current_file and '.xml' not in current_file:
            file_changes.append((current_file, added_lines, deleted_lines, parent_jira_id))

    return file_changes


def generate_embedding(file_changes):
    diffDoc = {}
    embeddings = []

    for file_change in file_changes:
        file_name, added_lines, deleted_lines, parent_jira_id = file_change
        embedding = {
            'file_name': file_name,
            'added_lines': added_lines,
            'deleted_lines': deleted_lines,
            'parent_jira_id': parent_jira_id
        }
        embeddings.append(embedding)

    # vector = embedding_function.embed_query(generateMinifiedChangeList(embeddings))
    return generateMinifiedChangeList(embeddings)
    # print(f"Vector for 'apple': {vector}")
    # print(f"Vector length: {len(vector)}")
    # return vector
    # save_document_as_json(embeddings, "/data/diffs")


def generateMinifiedChangeList(embeddings):
    return json.dumps(embeddings).replace(" ", "").replace("[", "").replace("]", "").replace("'", "").replace('\"',
                                                                                                              "").replace(
        "\\t", "").replace("{", "").replace("}", "").replace(":", " ")


def extract_file_info(text):
    global jira_ids
    file_names = []
    added_files = []
    deleted_files = []
    diff_file_names = []

    # Split the text by comma to separate different pieces of information
    pieces = text.split(',')
    with open("data/json/pull_request_data.json", "r") as file:
        data = json.load(file)
    # Iterate over each piece of information
    added = False
    deleted = False
    for piece in pieces:
        # Extract file names
        if piece.startswith('file_name'):
            added = False
            deleted = False
            file_names.append(piece.split('file_name ')[-1])
        elif piece.startswith('added_lines') and added == False:
            added = True
            deleted = False
            added_files.append(piece.split('++')[-1])
        elif piece.startswith('deleted_lines') and deleted == False:
            added = False
            deleted = True
            deleted_files.append(piece.split('--')[-1])
        elif piece.startswith('diff_name'):
            diff_file_names.append(piece.split('diff_name ')[-1])
            break
        if added:
            added_files.append(piece)
        if deleted:
            deleted_files.append(piece)
    for file_path in diff_file_names:
        jira_ids = get_description_by_diff_file(data, file_path)
        diff_file_names = jira_ids

    return file_names, added_files, deleted_files, diff_file_names
#
#
# prompt = ''' <> '''
#
# extract_file_info(prompt)
