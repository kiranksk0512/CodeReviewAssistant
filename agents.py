from crewai import Agent
from tools import Tools
from langchain.llms import Ollama

class Agents:

  openai_api_key="<pasteKeyHere>"
  # MODEL='openhermes'
  
  # def __init__(self):
  #   MODEL='openhermes'
  #   self.llm = Ollama(model=MODEL)

  def vectorSearchAgent(self):
    return Agent(
      role='Vector Search agent',
      goal='Conduct a search within a vector database using both the user question and a git difference parameter.',
      backstory='This agent was developed to enhance the efficiency of issue tracking and resolution '
                   'by leveraging vector-based search algorithms. By incorporating user questions and '
                   'Git difference parameters, it aims to provide more accurate and relevant results '
                   'for similar Jira issues, thereby streamlining the development and debugging process.',
      tools=[Tools.getSimilarGitDiff],
      verbose=True,
      allow_delegation=False # if it's true then agent will be able to delegate task to another agent
    )

  def jiraAgent(self):
    return Agent(
      role='Jira Search agent',
      goal='Conduct a search on Jira Boards utilizing a jiraId and will return description, summary'
      'commits, parent, children, status arguments of its parent Jiras and details of its Child Jira',
      backstory='This agent has been developed to streamline the process of gathering information '
                   'related to Jira issues within software development projects. By automating the '
                   'search process and retrieving comprehensive details such as description, summary, '
                   'and associated commits, it aims to enhance the efficiency of developers and project '
                   'managers in tracking and managing Jira issues effectively.',
      tools=[Tools.getRelatedJiraDetails],
      verbose=True,
      allow_delegation=False # if it's true then agent will be able to delegate task to another agent
    )

  # def domainSpecificPrAnalysisAgent():
  #   return Agent(
  #     role='Domain Specific Pr Analysis agent',
  #     goal='Perform the calculations on the numbers given to you',
  #     backstory='An maths expert working with numbers who have experience solving complex and basic maths problems',
  #     tools=[Tools.verifyDomianSpecifcLogic],
  #     verbose=True,
  #     allow_delegation=False # if it's true then agent will be able to delegate task to another agent
  #   )

  # def staticCodeAnalysisAgent():
  #   return Agent(
  #     role='Static Code Analyzer',
  #     goal='Conduct comprehensive static code analysis on software projects',,
  #     tools=[Tools.staticCodeAnalysis],
  #     verbose=True,
  #     allow_delegation=False # if it's true then agent will be able to delegate task to another agent
  #   )