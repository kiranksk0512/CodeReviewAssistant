from crewai import Crew, Agent, Task
from textwrap import dedent
from agents import Agents
from tasks import Tasks
from llm import giveDecriptiveAnswer, get_static_code_analysis
import os
import json
import requests


def generate_context_for_jira_retrieve(getGitDiffofSimilarJirasTask):
    print("printing the task from agent 1")
    print(getGitDiffofSimilarJirasTask.json)
    # added_file = getGitDiffofSimilarJirasTask.json.get('added_files')
    print("added files")
    # print(added_file)
    # deleted_files = getGitDiffofSimilarJirasTask.json.get('deleted_files')
    print("deleted files")
    # print(deleted_files)
    # jira_ids =  getGitDiffofSimilarJirasTask.json.get('jira_ids')
    # print(jira_ids)
    # text = f'''
    # the files which are generally changed in the files are  {added_file} and {deleted_files}
    # the jira ids for these changes {jira_ids}
    # '''
    text = f'''de'''
    return text


class PrReviewer:

    # def __init__(self, gitDff):
    #   # self.userInput = userInput
    #   self.gitDff = gitDff

    def run(self, gitDff):
        agents = Agents();
        vectorSearchAgent = agents.vectorSearchAgent()
        jiraRetrieverAgent = agents.jiraAgent()

        # staticCodeAnalysisAgent = Agents.staticCodeAnalysisAgent()
        # domainSpecificPrAnalysisAgent = Agents.domainSpecificPrAnalysisAgent()
        getGitDiffofSimilarJirasTask = Tasks.getGitDiffofSimilarJiras(vectorSearchAgent, gitDff)
        jiraRetrieverTask = Tasks.jiraRetriever(jiraRetrieverAgent, [getGitDiffofSimilarJirasTask])
        # staticCodeAnalysisTask = Tasks.staticCodeAnalysisAgent()
        # domainSpecificPrAnalysisTask = Tasks.domainSpecificPrAnalysisTask()

        crew = Crew(
                agents=[vectorSearchAgent, jiraRetrieverAgent],
                tasks=[getGitDiffofSimilarJirasTask, jiraRetrieverTask],
                verbose=2,  # You can set it to 1 or 2 to different logging levels
            )



        result = crew.kickoff()
        print("result")
        print(result)
        jsonObjArray = json.loads(result)
        # res = o[0]
        print("jsonObjArray : ")
        print(jsonObjArray)
        print(type(result));
        out = ""
        for jira in jsonObjArray:
            out += "jira Id : " + jira["key"] + ", description : " + jira["description"] + ", "
        print("final_output : ------------")
        print(out)

        static_code_analysis = get_static_code_analysis(gitDff)
        descriptiveAnswer = giveDecriptiveAnswer(out)
        #append the two strings


        return static_code_analysis + descriptiveAnswer
