import requests
import json 
import logging
import os
logging.basicConfig(format='%(asctime)s %(message)s',
                datefmt='%m/%d/%Y %I:%M:%S %p',
                filename='code_versioning.log',
                filemode='w',
                level=logging.INFO)

class code_versioning:  
        
    # Instance Variable 
    comingJson = json
    sendJson = json
        
    # The init method or constructor  
    def __init__(self, jsonFile):      
        logging.info('Object created')
        #parametre olarak gelen json file'ını load(işlenebilecek hale getirir) eder.
        self.comingJson = json.load(jsonFile)
    
    #directoryde bir json file oluşturur(aşağı kısımlarda hem request olarak gönderilcek hem okunarak bilgiler alıncak)
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
        #split ederek file ismini bulur ve filename değişkenine kaydeder
        filename=self.splitPathAndReturnFilename(commitFilePath)
        #eğer path directory ise onu repository directorysi içine kopyalar ve siler
        if os.path.isdir(commitFilePath):  
            os.popen('cp -r '+commitFilePath+' '+repositoryPath)
            os.popen('rm -rf '+commitFilePath)
        #eğer path file ise onu repository directorysi içine kopyalar ve siler
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
        #id ve password kullanarak remote'u günceller
        os.popen('git -C '+repositoryPath+' remote set-url origin https://'+id+':'+password+'@github.com/'+id+'/'+projectName+'.git')
        #pushlar 
        #BRANCHLER AKTIF KULLANILACAKSA MASTER YERINE BRANCH EKLENEBILIR.
        os.popen('git -C '+repositoryPath+' push -u origin master')

    def pull(self,repositoryPath,id,password,url):
        logging.info('Pull function.')
        #url'den proje ismini split ederek bulur
        projectName=self.splitPathAndReturnFilename(url)
        #id ve password kullanarak remote'u günceller
        os.popen('git -C '+repositoryPath+' remote set-url origin https://'+id+':'+password+'@github.com/'+id+'/'+projectName+'.git')
        #pull yapar
        #BRANCHLER AKTIF KULLANILACAKSA MASTER YERINE BRANCH EKLENEBILIR.
        os.popen('git -C '+repositoryPath+' pull origin master')

    #Hata vermiyor çalışıp çalışmadığından emin değilim
    def merge(self,repositoryPath,id,password,url):
        logging.info('Merge function.')
        #url'den proje ismini split ederek bulur
        projectName=self.splitPathAndReturnFilename(url)
        #id ve password kullanarak remote'u günceller
        os.popen('git -C '+repositoryPath+' remote set-url origin https://'+id+':'+password+'@github.com/'+id+'/'+projectName+'.git')
        #merge yapar
        #BRANCHLER AKTIF KULLANILACAKSA MASTER YERINE BRANCH EKLENEBILIR.
        os.popen('git -C '+repositoryPath+' merge')

    def revert(self,repositoryPath,id,password,url):
        logging.info('Revert function.')
        #url'den proje ismini split ederek bulur
        projectName=self.splitPathAndReturnFilename(url)
        #id ve password kullanarak remote'u günceller
        os.popen('git -C '+repositoryPath+' remote set-url origin https://'+id+':'+password+'@github.com/'+id+'/'+projectName+'.git')
        #merge yapar
        #BRANCHLER AKTIF KULLANILACAKSA MASTER YERINE BRANCH EKLENEBILIR.
        os.popen('git -C '+repositoryPath+' revert HEAD')
        os.popen('git -C '+repositoryPath+' commit -m "Revert commit"')
        os.popen('git -C '+repositoryPath+' push -u origin master')

    # Parses the coming json file / Gelen json dosyasını parse eder.
    def parseJson(self):
        #logger hangi stagede ise o stage hakkında bilgi verir.
        logging.info('Json Parsing Function')

        #gelen json file'a göre işlemler yapar
        if(self.comingJson['destination']!='6'): #Eğer destination'u cv olmayan bir dosya alırsa error verir ve çıkar.
            logging.error('Json destination is not code versioning ')
            exit()
        
        #plandan gelmişse ve işlem repository creation ise hem request için hemde commit için json file oluşturur ve directory'e yazar.
        elif(self.comingJson['origin']=='2' and self.comingJson['operation']=='repository_creation'):
            self.sendJson = self.comingJson
            self.sendJson['title']='Code versioning request'
            self.sendJson['description']='will build'
            self.sendJson['destination']='1'
            self.sendJson['origin']='6'
            self.sendJson['operation']='build'
            self.createJsonFileInDirectory()
            logging.info('Repository informations are received')
        
        #plandan gelmişse ve işlem repository creation ise hem request için hemde commit için json file oluşturur ve directoryde json file oluştur.
        elif(self.comingJson['origin']=='2' and self.comingJson['operation']=='commit'):
            #önceden cv_response.json olarak yazdığı dosyayı okur
            path=os.getcwd()
            path=path+'/cv_response.json'
            jsonFile=open(path,'r')
            readJson = json.load(jsonFile)
            self.commit(readJson['directory_path'],self.comingJson['commit_file_directory'])

        elif(self.comingJson['origin']=='2' and self.comingJson['operation']=='push'):
            #önceden cv_response.json olarak yazdığı dosyayı okur
            path=os.getcwd()
            path=path+'/cv_response.json'
            jsonFile=open(path,'r')
            self.sendJson =json.load(jsonFile)
            self.push(self.sendJson['directory_path'],self.sendJson['github_login'],self.sendJson['github_password'],self.sendJson['repository_url'])
            r = requests.post(url = 'http://localhost:8081', data = json.dumps(self.sendJson)) 

        elif(self.comingJson['origin']=='2' and self.comingJson['operation']=='pull'):
            #önceden cv_response.json olarak yazdığı dosyayı okur
            path=os.getcwd()
            path=path+'/cv_response.json'
            jsonFile=open(path,'r')
            readJson =json.load(jsonFile)
            self.pull(readJson['directory_path'],readJson['github_login'],readJson['github_password'],readJson['repository_url'])
        
        elif(self.comingJson['origin']=='2' and self.comingJson['operation']=='merge'):
            #önceden cv_response.json olarak yazdığı dosyayı okur
            path=os.getcwd()
            path=path+'/cv_response.json'
            jsonFile=open(path,'r')
            readJson =json.load(jsonFile)
            self.merge(readJson['directory_path'],readJson['github_login'],readJson['github_password'],readJson['repository_url'])
        
        elif(self.comingJson['origin']=='2' and self.comingJson['operation']=='revert'):
            #önceden cv_response.json olarak yazdığı dosyayı okur
            path=os.getcwd()
            path=path+'/cv_response.json'
            jsonFile=open(path,'r')
            readJson =json.load(jsonFile)
            self.revert(readJson['directory_path'],readJson['github_login'],readJson['github_password'],readJson['repository_url'])

    
# Driver Code  
def main(jfile):
    #alttaki json datası mule tarafından direk verilecek.
    #ilk calısması için gereken json file
    #jfile = open(r'/Users/fatihselimyakar/Desktop/Git/CSE343_Code_Versioning/initial_request.json', 'r')
    #jfile = open(r'/Users/fatihselimyakar/Desktop/Git/CSE343_Code_Versioning/process_file.json', 'r')
    cv_obj=code_versioning(jfile)
    cv_obj.parseJson()

 
if __name__== "__main__":
  main(jfile)

