import requests
import json 
import logging
import os
logging.basicConfig(format='%(asctime)s %(message)s',
                datefmt='%m/%d/%Y %I:%M:%S %p',
                filename='code_versioning.log',
                filemode='w',
                level=logging.INFO)
                
def json_load_byteified(file_handle):
    return _byteify(
        json.load(file_handle, object_hook=_byteify),
        ignore_dicts=True
    )

def json_loads_byteified(json_text):
    return _byteify(
        json.loads(json_text, object_hook=_byteify),
        ignore_dicts=True
    )

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

class code_versioning:  
        
    # Instance Variable 
    comingJson = json
    sendJson = json
        
    # The init method or constructor  
    def __init__(self, jsonFile):      
        logging.info('Object created')
        #parametre olarak gelen json fileini load(islenebilecek hale getirir) eder.
        self.comingJson = json_loads_byteified(jsonFile)
    
    #directoryde bir json file olusturur(asagi kisimlarda hem request olarak gonderilcek hem okunarak bilgiler alincak)
    def createJsonFileInDirectory(self):
        print(self.sendJson)
        with open('cv_response.json', 'w') as outfile:
            writeString=(str)(self.sendJson).replace("\'","\"")
            outfile.write(writeString)
        logging.info('Json file created.')
    
    def splitPathAndReturnFilename(self,path):
        return path.split("/")[-1]

    def commit(self,repositoryPath,commitFilePath):
        logging.info('Commit function.')
        #split ederek file ismini bulur ve filename degiskenine kaydeder
        filename=self.splitPathAndReturnFilename(commitFilePath)
        #eger path directory ise onu repository directorysi icine kopyalar ve siler
        if os.path.isdir(commitFilePath):  
            os.popen('cp -r '+commitFilePath+' '+repositoryPath)
            os.popen('rm -rf '+commitFilePath)
        #eger path file ise onu repository directorysi icine kopyalar ve siler
        elif os.path.isfile(commitFilePath):  
            os.popen('cp '+commitFilePath+' '+repositoryPath)
            os.popen('rm -f '+commitFilePath)
        #kopyalanan file veya directory'i repository'e ekler ve commit eder
        os.popen('git -C '+repositoryPath+' add '+filename)
        os.popen('git -C '+repositoryPath+' commit -m \"'+filename+'\"')

    def push(self,repositoryPath,id,password,url):
        logging.info('Push function.')
        #url'den proje ismini split ederek bulur
        projectName=self.splitPathAndReturnFilename(url)
        #id ve password kullanarak remote'u gunceller
        os.popen('git -C '+repositoryPath+' remote set-url origin https://'+id+':'+password+'@github.com/'+id+'/'+projectName+'.git')
        #pushlar 
        #BRANCHLER AKTIF KULLANILACAKSA MASTER YERINE BRANCH EKLENEBILIR.
        os.popen('git -C '+repositoryPath+' push -u origin master')

    def pull(self,repositoryPath,id,password,url):
        logging.info('Pull function.')
        #url'den proje ismini split ederek bulur
        projectName=self.splitPathAndReturnFilename(url)
        #id ve password kullanarak remote'u gunceller
        os.popen('git -C '+repositoryPath+' remote set-url origin https://'+id+':'+password+'@github.com/'+id+'/'+projectName+'.git')
        #pull yapar
        #BRANCHLER AKTIF KULLANILACAKSA MASTER YERINE BRANCH EKLENEBILIR.
        os.popen('git -C '+repositoryPath+' pull origin master')

    #Hata vermiyor calisip calismadigindan emin degilim
    def merge(self,repositoryPath,id,password,url):
        logging.info('Merge function.')
        #url'den proje ismini split ederek bulur
        projectName=self.splitPathAndReturnFilename(url)
        #id ve password kullanarak remote'u gunceller
        os.popen('git -C '+repositoryPath+' remote set-url origin https://'+id+':'+password+'@github.com/'+id+'/'+projectName+'.git')
        #merge yapar
        #BRANCHLER AKTIF KULLANILACAKSA MASTER YERINE BRANCH EKLENEBILIR.
        os.popen('git -C '+repositoryPath+' merge')

    def revert(self,repositoryPath,id,password,url):
        logging.info('Revert function.')
        #url'den proje ismini split ederek bulur
        projectName=self.splitPathAndReturnFilename(url)
        #id ve password kullanarak remote'u gunceller
        os.popen('git -C '+repositoryPath+' remote set-url origin https://'+id+':'+password+'@github.com/'+id+'/'+projectName+'.git')
        #merge yapar
        #BRANCHLER AKTIF KULLANILACAKSA MASTER YERINE BRANCH EKLENEBILIR.
        os.popen('git -C '+repositoryPath+' revert HEAD')
        os.popen('git -C '+repositoryPath+' commit -m "Revert commit"')
        os.popen('git -C '+repositoryPath+' push -u origin master')

    # Parses the coming json file / Gelen json dosyasini parse eder.
    def parseJson(self):
        #logger hangi stagede ise o stage hakkinda bilgi verir.
        logging.info('Json Parsing Function')

        #gelen json file'a gore islemler yapar
        if(self.comingJson['destination']!='6'): #Eger destination'u cv olmayan bir dosya alirsa error verir ve cikar.
            logging.error('Json destination is not code versioning ')
            exit()
        
        #plandan gelmisse ve islem repository creation ise hem request icin hemde commit icin json file olusturur ve directory'e yazar.
        elif(self.comingJson['origin']=='2' and self.comingJson['operation']=='repository_creation'):
            self.sendJson = self.comingJson
            self.sendJson['title']='Code versioning request'
            self.sendJson['description']='will build'
            self.sendJson['destination']='2'
            self.sendJson['origin']='6'
            self.sendJson['operation']='build'
            self.createJsonFileInDirectory()
            logging.info('Repository informations are received')
        
        #plandan gelmisse ve islem repository creation ise hem request icin hemde commit icin json file olusturur ve directoryde json file olustur.
        elif(self.comingJson['origin']=='2' and self.comingJson['operation']=='commit'):
            #onceden cv_response.json olarak yazdigi dosyayi okur
            path=os.getcwd()
            path=path+'/cv_response.json'
            jsonFile=open(path,'r')
            self.sendJson = json.load(jsonFile)
            self.commit(self.sendJson['repository_path'],self.comingJson['project_path'])
            self.push(self.sendJson['repository_path'],self.sendJson['github_login'],self.sendJson['github_password'],self.sendJson['repository_url'])
            r = requests.post(url = 'http://localhost:8081', data = json.dumps(self.sendJson)) 

        elif(self.comingJson['origin']=='2' and self.comingJson['operation']=='push'):
            #onceden cv_response.json olarak yazdigi dosyayi okur
            path=os.getcwd()
            path=path+'/cv_response.json'
            jsonFile=open(path,'r')
            self.sendJson =json.load(jsonFile)
            self.push(self.sendJson['repository_path'],self.sendJson['github_login'],self.sendJson['github_password'],self.sendJson['repository_url'])
            r = requests.post(url = 'http://localhost:8081', data = json.dumps(self.sendJson)) 

        elif(self.comingJson['origin']=='2' and self.comingJson['operation']=='pull'):
            #onceden cv_response.json olarak yazdigi dosyayi okur
            path=os.getcwd()
            path=path+'/cv_response.json'
            jsonFile=open(path,'r')
            readJson =json.load(jsonFile)
            self.pull(readJson['repository_path'],readJson['github_login'],readJson['github_password'],readJson['repository_url'])
        
        elif(self.comingJson['origin']=='2' and self.comingJson['operation']=='merge'):
            #onceden cv_response.json olarak yazdigi dosyayi okur
            path=os.getcwd()
            path=path+'/cv_response.json'
            jsonFile=open(path,'r')
            readJson =json.load(jsonFile)
            self.merge(readJson['repository_path'],readJson['github_login'],readJson['github_password'],readJson['repository_url'])
        
        elif(self.comingJson['origin']=='2' and self.comingJson['operation']=='revert'):
            #onceden cv_response.json olarak yazdigi dosyayi okur
            path=os.getcwd()
            path=path+'/cv_response.json'
            jsonFile=open(path,'r')
            readJson =json.load(jsonFile)
            self.revert(readJson['repository_path'],readJson['github_login'],readJson['github_password'],readJson['repository_url'])

    
# Driver Code  
def main(jfile):
    #alttaki json datasi mule tarafindan direk verilecek.
    #ilk calismasi icin gereken json file
    #jfile = open(r'/home/fatihselimyakar/Desktop/CSE343_Code_Versioning/initial_request.json', 'r')
    #jfile = open(r'/home/fatihselimyakar/Desktop/CSE343_Code_Versioning/process_file.json', 'r')
    cv_obj=code_versioning(jfile)
    cv_obj.parseJson()


main(jfile)

