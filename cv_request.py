# importing the requests library 
import requests 
import json

jsonFile = open(r'/home/fatihselimyakar/Desktop/codeversioning/code_versioning_response.json', 'r')
data = json.load(jsonFile)
print (data)

# sending post request and saving response as response object 
r = requests.post(url = 'http://localhost:8081', data = data) 
# extracting response text 
pastebin_url = r.text 
print("\nThe pastebin URL is:%s"%pastebin_url)
