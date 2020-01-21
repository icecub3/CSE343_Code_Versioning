import requests
import json 
import logging
import os
import time

# Log messages written into file
logging.basicConfig(format='%(asctime)s %(message)s',
                datefmt='%m/%d/%Y %I:%M:%S %p',
                filename='code_versioning.log',
                filemode='w',
                level=logging.INFO)

# Functions to convert Unicode files into UTF-8. (Red u problem bugfix)      
# Mostly taken from internet
def json_load_byteified(file_handle):
    return _byteify(
        json.load(file_handle, object_hook=_byteify),
        ignore_dicts=True
    )

# Functions to convert Unicode files into UTF-8. (Red u problem bugfix)      
# Mostly taken from internet
def json_loads_byteified(json_text):
    return _byteify(
        json.loads(json_text, object_hook=_byteify),
        ignore_dicts=True
    )

# Functions to convert Unicode files into UTF-8. (Red u problem bugfix)      
# Mostly taken from internet
def _byteify(data, ignore_dicts = False):
    # if this is a unicode string, return its string representation
    if isinstance(data, unicode):
        return data.encode('utf-8')
    # if this is a list of values, return list of byteified values
    if isinstance(data, list):
        return [ _byteify(item, ignore_dicts=True) for item in data ]
    # if this is a dictionary, return dictionary of byteified keys and values
    # but only if we haven't already byteified it
    if isinstance(data, dict) and not ignore_dicts:
        return {
            _byteify(key, ignore_dicts=True): _byteify(value, ignore_dicts=True)
            for key, value in data.iteritems()
        }
    # if it's anything else, return it in its original form
    return data

# Class for managing code versioning and its operations.
class code_versioning:  
    comingJson = json 	# Incoming request file
    sendJson = json 	# Outgoing response file
        
    # The init method or constructor  
    def __init__(self, jsonFile):      
        logging.info('code_versioning object created.')
        # Parses the incoming JSON file, converts it to an object.
        self.comingJson = json_loads_byteified(jsonFile)
    
    # Creates a JSON file in the current directory. (It will be used for both incoming requests and outgoing responses.)
    def createJsonFileInDirectory(self):
        print(self.sendJson)
        with open('cv_response.json', 'w') as outfile:
            writeString=(str)(self.sendJson).replace("\'","\"")
            outfile.write(writeString)
        logging.info('Response JSON file created.')
    
    def splitPathAndReturnFilename(self,path):
        return path.split("/")[-1]

    # git commit
    def commit(self,repositoryPath,commitFilePath):
        logging.info('Commit function called.')
        # Finds filename from the incoming path.
        filename=self.splitPathAndReturnFilename(commitFilePath)
        # If it is a directory, copies it to repository and deletes from current directory.
        if os.path.isdir(commitFilePath):  
            os.popen('cp -r '+commitFilePath+' '+repositoryPath)
            #os.popen('rm -rf '+commitFilePath)
        # If it is a file, copies it to repository and deletes from current directory.
        elif os.path.isfile(commitFilePath):  
            os.popen('cp '+commitFilePath+' '+repositoryPath)
            #os.popen('rm -f '+commitFilePath)
        # Adds copied file or directory to the repository, then commits it.
        time.sleep(1)
        os.popen('git -C '+repositoryPath+' add '+filename)
        time.sleep(1)
        os.popen('git -C '+repositoryPath+' commit -m \"'+filename+'\"')
        logging.info('Commit function finished.')

    # git push
    def push(self,repositoryPath,id,password,url):
        logging.info('Push function called.')
        # Finds project name by parsing the incoming url.
        projectName=self.splitPathAndReturnFilename(url)
        # Updates remote repository url by using the incoming github id and password. 
        os.popen('git -C '+repositoryPath+' remote set-url origin https://'+id+':'+password+'@github.com/'+id+'/'+projectName+'.git')
        #Bilgisayarda calismasi icin
        #os.popen('git -C '+repositoryPath+' remote set-url origin https://'+id+':'+password+'@github.com/'+id+'/GtuDevOps'+'.git')
        time.sleep(1)
        # Performs push
        os.popen('git -C '+repositoryPath+' push -u origin master')
        #Alternatif olarak
        #os.popen('git -C '+repositoryPath+' push --force -u origin master')
        logging.info('Push function finished.')

    # git pull
    def pull(self,repositoryPath,id,password,url):
        logging.info('Pull function called.')
        # Finds project name by parsing the incoming url.
        projectName=self.splitPathAndReturnFilename(url)
        # Updates remote repository url by using the incoming github id and password. 
        os.popen('git -C '+repositoryPath+' remote set-url origin https://'+id+':'+password+'@github.com/'+id+'/'+projectName+'.git')
        # os.popen('git -C '+repositoryPath+' remote set-url origin https://'+id+':'+password+'@github.com/'+id+'/GtuDevOps'+'.git')
        time.sleep(1)
        # Performs pull
        os.popen('git -C '+repositoryPath+' pull origin master')
        logging.info('Pull function finished.')

    # git merge
    # Hata vermiyor calisip calismadigindan emin degilim
    # TODO: Needs test
    def merge(self,repositoryPath,id,password,url):
        logging.info('Merge function called.')
        # Finds project name by parsing the incoming url.
        projectName=self.splitPathAndReturnFilename(url)
        # Updates remote repository url by using the incoming github id and password. 
        os.popen('git -C '+repositoryPath+' remote set-url origin https://'+id+':'+password+'@github.com/'+id+'/'+projectName+'.git')
        #os.popen('git -C '+repositoryPath+' remote set-url origin https://'+id+':'+password+'@github.com/'+id+'/GtuDevOps'+'.git')
        time.sleep(1)
        # Performs merge
        os.popen('git -C '+repositoryPath+' merge')
        logging.info('Merge function finished.')

    # git revert
    def revert(self,repositoryPath,id,password,url):
        logging.info('Revert function called.')
        # Finds project name by parsing the incoming url.
        projectName=self.splitPathAndReturnFilename(url)
        # Updates remote repository url by using the incoming github id and password. 
        os.popen('git -C '+repositoryPath+' remote set-url origin https://'+id+':'+password+'@github.com/'+id+'/'+projectName+'.git')
        #os.popen('git -C '+repositoryPath+' remote set-url origin https://'+id+':'+password+'@github.com/'+id+'/GtuDevOps'+'.git')
        time.sleep(1)
        # Performs revert
        os.popen('git -C '+repositoryPath+' revert HEAD')
        time.sleep(1)
        # Performs commit
        os.popen('git -C '+repositoryPath+' commit -m "Revert commit"')
        time.sleep(1)
        # Performs push
        os.popen('git -C '+repositoryPath+' push -u origin master')
        logging.info('Revert function finished.')

    # Parses the coming json file / Gelen json dosyasini parse eder.
    def parseJson(self):
        logging.info('parseJson called.')

        # If the destination is not 'Code Versioning', log the error, then exit from the program.
        if(self.comingJson['destination']!='6'): 
            logging.error('Incoming request destination is not code versioning!')
            exit()
        
        # If the request coming from the 'Plan' group and the operation is 'repository_creation'
        # create JSON response file in the directory for both request and the commit operation
        elif(self.comingJson['origin']=='2' and self.comingJson['operation']=='repository_creation'):
            self.sendJson = self.comingJson
            self.sendJson['title']='Code versioning request'
            self.sendJson['description']='will build'
            self.sendJson['destination']='2'
            self.sendJson['origin']='6'
            self.sendJson['operation']='build'
            self.createJsonFileInDirectory()
            logging.info('Repository informations are received.')
        
        # If the request coming from the 'Plan' group and the operation is 'commit'
        # read data from the response file, perform commit and push, send response back.
    	elif(self.comingJson['origin']=='2' and self.comingJson['operation']=='commit'):
            #onceden cv_response.json olarak yazdigi dosyayi okur
            path=os.getcwd()
            path=path+'/cv_response.json'
            jsonFile=open(path,'r')
            self.sendJson = json.load(jsonFile)
            self.pull(self.sendJson['repository_path'],self.sendJson['github_login'],self.sendJson['github_password'],self.sendJson['repository_url'])
            self.commit(self.sendJson['repository_path'],self.comingJson['project_path'])
            self.push(self.sendJson['repository_path'],self.sendJson['github_login'],self.sendJson['github_password'],self.sendJson['repository_url'])
            r = requests.post(url = 'http://localhost:8081', data = json.dumps(self.sendJson)) 

        # If the request coming from the 'Plan' group and the operation is 'push'
        # read data from the response file, perform push, send response back.
        elif(self.comingJson['origin']=='2' and self.comingJson['operation']=='push'):
            #onceden cv_response.json olarak yazdigi dosyayi okur
            path=os.getcwd()
            path=path+'/cv_response.json'
            jsonFile=open(path,'r')
            self.sendJson =json.load(jsonFile)
            self.push(self.sendJson['repository_path'],self.sendJson['github_login'],self.sendJson['github_password'],self.sendJson['repository_url'])
            r = requests.post(url = 'http://localhost:8081', data = json.dumps(self.sendJson)) 

        # If the request coming from the 'Plan' group and the operation is 'pull'
        # read data from the response file, perform pull.
        elif(self.comingJson['origin']=='2' and self.comingJson['operation']=='pull'):
            #onceden cv_response.json olarak yazdigi dosyayi okur
            path=os.getcwd()
            path=path+'/cv_response.json'
            jsonFile=open(path,'r')
            readJson =json.load(jsonFile)
            self.pull(readJson['repository_path'],readJson['github_login'],readJson['github_password'],readJson['repository_url'])
        
        # If the request coming from the 'Plan' group and the operation is 'merge'
        # read data from the response file, perform merge.
        elif(self.comingJson['origin']=='2' and self.comingJson['operation']=='merge'):
            #onceden cv_response.json olarak yazdigi dosyayi okur
            path=os.getcwd()
            path=path+'/cv_response.json'
            jsonFile=open(path,'r')
            readJson =json.load(jsonFile)
            self.merge(readJson['repository_path'],readJson['github_login'],readJson['github_password'],readJson['repository_url'])
        
        # If the request coming from the 'Plan' group and the operation is 'revert'
        # read data from the response file, perform revert.
        elif(self.comingJson['origin']=='2' and self.comingJson['operation']=='revert'):
            #onceden cv_response.json olarak yazdigi dosyayi okur
            path=os.getcwd()
            path=path+'/cv_response.json'
            jsonFile=open(path,'r')
            readJson =json.load(jsonFile)
            self.revert(readJson['repository_path'],readJson['github_login'],readJson['github_password'],readJson['repository_url'])
        logging.info('parseJson finished.')

    
# Driver Code  
def main(jfile):
    #alttaki json datasi mule tarafindan direk verilecek.
    #ilk calismasi icin gereken json file
    #jfile = open(r'/home/fatihselimyakar/Desktop/CSE343_Code_Versioning/initial_request.json', 'r')
    #jfile = open(r'/home/fatihselimyakar/Desktop/CSE343_Code_Versioning/process_file.json', 'r')
    cv_obj=code_versioning(jfile)
    cv_obj.parseJson()


main(jfile)

