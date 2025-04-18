from crewai import Task
from textwrap import dedent

class Tasks:

  def getGitDiffofSimilarJiras(agent, gitDff):
    return Task(
      description=dedent(f"""
        you have given a git Difference and you have to search vectorDataBase and find the similar git Differences
        Here is the git difference on a file:
        {gitDff}
      """),
      agent=agent,
      expected_output="list of similar git difference"
    )

  def jiraRetriever(agent, context):
    # print("Context from Task1 : ")
    # print(context)
    return Task(
      description=dedent(f"""
        you have be given a list of jira Ids in the from Related Jira field from the context passed to you
         and you have to search the jira board and find the details of its parent jira and all child jiras
        The context will be some thing like this, you have the get the jira Ids from the Related Jira field
        , an example of the context is given below ':
        Context:
        File: aaservices/src/java/com/isa/thinair/aaservices/core/bl/ChangeFare/AAChangeFareUtils.java
        Added Lines:
          ++b/aaservices/src/java/com/isa/thinair/aaservices/core/bl/ChangeFare/AAChangeFareUtils.java
          ondInfoTO.setFlownOnd(ondInfo.isFlownOnd());
          ondInfoTO.setUnTouchedOnd(ondInfo.isUnTouchedOnd());
        Deleted Lines:
          --a/aaservices/src/java/com/isa/thinair/aaservices/core/bl/ChangeFare/AAChangeFareUtils.java
            parent_jira_id 1890561c06c
        Related Jira: [<jira_id-1>,<jira_id-2>]
      """),
      agent=agent,
      expected_output='''return the list of details of its parent jiras and child jiras in the fomrat "
                      example for your response
                       {
                          "key": "ASPPI-5308",
                          "description": "This Jira pertains to the development of the AAChangeFareUtils module in the aaservices project",
                          "summary": "Development of AAChangeFareUtils module",
                          "commits": ["1890561c06c"],
                          "parent": ["SUPP-12"],
                          "children": ["SUPP-15"],
                          "status": "Completed"
                       },
                      ''',
      context=context
    )