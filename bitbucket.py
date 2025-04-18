from atlassian.bitbucket import Cloud

bitbucket = Cloud(
    username="<pasteUsernameHere>",
    password="<pastePassHere>",
    token=True)
 print(bitbucket.workspaces.get("<pasteUsernameHere>").repositories.get("<pasteRepoName>"))