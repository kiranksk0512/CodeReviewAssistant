from atlassian.bitbucket import Cloud
from atlassian.bitbucket import Bitbucket
import requests


api_url = f"<fileURLINREPO>"
# api_url = f"https://api.bitbucket.org/2.0/repositories/kiran0512/aeromart-thin-air/contents"
# Add the Authorization header with the token
headers = {'Authorization': f'token <pasteTokenHere>'}
# Make the request
response = requests.get(api_url,headers=headers)
# items = response.json()
print(response.content)  
    
  
    

# print(bitbucket.workspaces.get("kiran0512").repositories.get("aeromart-thin-air"))
# print(bitbucket.get_content_of_file("Aero-Mart", "aeromart-thin-air", "WSClientBD.java", at=None, markup=None))


