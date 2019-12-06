# importing the requests library 
import requests 
import json

jsonFile = open(r'/home/fatihselimyakar/Desktop/codeversioning/code_versioning_response.json', 'r')
data = json.load(jsonFile)
print (data)

# sending post request and saving response as response object 
r = requests.post(url = 'http://localhost:8081', data = json.dumps(data)) 
# extracting response text 
sent_json = r.headers
print("\nResponse:%s"%sent_json)