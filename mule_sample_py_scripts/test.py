import json 

import requests

def ok(json1):
	json_file=json.loads(json1)
	#print(json_file)
	a=json_file['destination']
	if a == "3":
		b="4"


	## do your stuff

	
	r=requests.post("http://localhost:8081",json={  
   "title": "Request information",
   "type": "object",
   "description": "Information necessary to access project sources on github repository and method to be applied Important: object_type = general_request",
   "object_type": "general_request",
   "destination": b
         
	}
	)

def main(filep):
	#json.dumps(filep, indent=4)
	#data=filep.json()
	print(filep)
	ok(filep)
main(json_file)

