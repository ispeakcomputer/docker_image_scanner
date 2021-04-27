import requests
from github import Github
import os
import json
from dockerfile_parse import DockerfileParser
source="https://gist.githubusercontent.com/jmelis/c60e61a893248244dc4fa12b946585c4/raw/25d39f67f2405330a6314cad64fac423a171162c/sources.txt"
mytoken = str(os.environ['GITHUBTOKEN'])


class Dockerchecker: 
    def grab_txt_file(self, url):
        r = requests.get(url)
        mytext = r.text
        return mytext

    def clean_and_package(self, mytext ):
        list_of_repos=[]
        for line in mytext.split('\n'):
            repo_info={}
            text  = line
            splittext = text.split(' ')
            print(len(splittext))

            try:
                splittext[1]
                repo_info['sha'] = splittext[1]
            except IndexError:
                pass

            repo_info['url'] = splittext[0]
            # Strip github url and file extension from 0 index
            parsed_string = splittext[0].replace('https://github.com/','')
            repo_info['user_repo'] = parsed_string.replace('.git','')

            # remove dead line
            if splittext[0] == '':
                pass
            else:
                list_of_repos.append(repo_info)

        return list_of_repos
    
   # ------------------------------------GITHUB------------------------------
    def parse_docker(self, mytoken, list_of_repos):
        g = Github(mytoken)
    
        for dic in list_of_repos:
            repo = dic['user_repo']
            repo_data = g.get_repo(repo)
            contents = repo_data.get_contents("")
            dfp = DockerfileParser()
        
            while contents: #recursive dir search
                file_content = contents.pop(0)
                if file_content.type == "dir":
                    contents.extend(repo_data.get_contents(file_content.path))
                else:
                    if file_content.name == 'Dockerfile':
                        dfp.content = str(file_content.decoded_content, 'utf-8') #start jsonify if Dockerfile
                        container_repo = json.loads(dfp.json)
                        
                        for dic in container_repo:
                            if 'FROM' in dic: #Needed lines too long. Split and only keep 1st col
                                string_list = dic['FROM'].split(' ')
                                print(string_list[0])
    def dict_packager(self)
if __name__ == "__main__":
    checker = Dockerchecker()

    text = checker.grab_txt_file(source)
    print(text)
    print(mytoken)
    repos_data = checker.clean_and_package(text)
    checker.parse_docker(mytoken, rmport requests
from github import Github
import os
import json
from dockerfile_parse import DockerfileParser
source="https://gist.githubusercontent.com/jmelis/c60e61a893248244dc4fa12b946585c4/raw/25d39f67f2405330a6314cad64fac423a171162c/sources.txt"
mytoken = str(os.environ['GITHUBTOKEN'])
 
 
class Dockerchecker:
    def grab_txt_file(self, url):
        r = requests.get(url)
        mytext = r.text
        return mytext
 
 
    def clean_and_package(self, mytext ):
        list_of_repos=[]
        for line in mytext.split('\n'):
            repo_info={}
            text  = line
            splittext = text.split(' ')
            
            try:                                                              
                splittext[1]                       
                repo_info['sha'] = splittext[1]
            except IndexError:                   
                pass  
            #repo_info['sha'] = splittext[1]
            repo_info['url'] = splittext[0]
            # Strip github url and file extension from 0 index
            parsed_string = splittext[0].replace('https://github.com/','')
            repo_info['user_repo'] = parsed_string.replace('.git','')
            # remove dead line
            if splittext[0] == '':
                pass
            else:
                list_of_repos.append(repo_info)
 
        return list_of_repos
    
    def url_sha_combiner(self, dict_of_repos):
            for url in dict_of_repos:
                combined = ":".join([url['url'],url['sha']])
                url['combined'] = combined
            return dict_of_repos
 
    # ------------------------------------GITHUB------------------------------
    def parse_docker(self, mytoken, list_of_repos):
        g = Github(mytoken)
 
        for dic in list_of_repos:
            repo = dic['user_repo']
            repo_data = g.get_repo(repo)
            contents = repo_data.get_contents("")
            dfp = DockerfileParser()
 
            while contents:
                file_content = contents.pop(0)
                if file_content.type == "dir":
                    contents.extend(repo_data.get_contents(file_content.path))
                else:
                    if file_content.name == 'Dockerfile':
                        dfp.content = str(file_content.decoded_content, 'utf-8')
                        container_repo = json.loads(dfp.json)
 
                        for dic in container_repo:
                            if 'FROM' in dic:
                                #Cleaning string. need only 1st col
                                string_list = dic['FROM'].split(' ')
                                print(string_list[0])

if __name__ == "__main__":
    checker = Dockerchecker()
 
    text = checker.grab_txt_file(source)
    dict_of_repos_data = checker.clean_and_package(text)
    checker.url_sha_combiner(dict_of_repos_data)
    checker.parse_docker(mytoken, dict_of_repos_data)
