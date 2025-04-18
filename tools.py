import json
from searchSimilarSearch import parse_git_diff, generate_embedding, extract_file_info
from jiraUtil import JiraEntry, JiraService
from langchain.tools import tool
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores.chroma import Chroma


class Tools:

    @tool("Get Git Differences of similar Jira")
    def getSimilarGitDiff(gitDiff):
      """
        used to get the similar git difference from the vector Database based on user git difference 
      """
      try:
        openai_api_key="<pasteKeyHere>"
        CHROMA_PATH = "chroma"
        print("gitDiff from tools")
        print(gitDiff)
        file_changes = parse_git_diff(gitDiff)
        print("gitDiff from file_changes")
        print(file_changes)
        embedding_text = generate_embedding(file_changes)
        db = Chroma(persist_directory=CHROMA_PATH, embedding_function=OpenAIEmbeddings(api_key=openai_api_key))
        docs = db.similarity_search(embedding_text)
        result = extract_file_info(docs[0].page_content)
        print("result from first agent : -----------")
        print(result)
        return result
      except SyntaxError:
        return "Error: getGitDiffSimilarJiraSearch"

    @tool("Get Jira Details of its parent and child Jiras based on the given list of Jira Ids")
    def getRelatedJiraDetails(jiraId):
      """
        used to get the similar git difference from the vector Database based on user git difference 
      """
      try:
        jiraService = JiraService()
        jira = jiraService.get(jiraId)
        print("jira : ")
        print(jira)
        return jira
      except SyntaxError:
        return "Error: getRelatedJiraDetails"


sample_diff = """ <pasteHere>
"""


# def getSimilarGitDiff(gitDiff):
#   """
#     used to get the similar git difference from the vector Database based on user git difference
#   """
#   try:
#     openai_api_key = "<pasteKey>"
#     CHROMA_PATH = "chroma"
#     print("gitDiff from tools")
#     print(gitDiff)
#     file_changes = parse_git_diff(gitDiff)
#     print("gitDiff from file_changes")
#     print(file_changes)
#     embedding_text = generate_embedding(file_changes)
#     db = Chroma(persist_directory=CHROMA_PATH, embedding_function=OpenAIEmbeddings(api_key=openai_api_key))
#     docs = db.similarity_search(embedding_text)
#     print("docs from tools")
#     print(docs)
#     result = extract_file_info(docs[0].page_content)
#     return result
#   except SyntaxError:
#     return "Error: getGitDiffSimilarJiraSearch"
#
# getSimilarGitDiff(sample_diff)