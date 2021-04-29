import requests
from github import Github
import os
import json
from dockerfile_parse import DockerfileParser
from pprint import pprint


class Dockerchecker:
    def grab_txt_file(self, url):
        try:
            r = requests.get(url)
            mytext = r.text
            return mytext
        except Exception as e: 
            print('Check your source url or internet connection')
            print(e)

    def clean_and_package(self, mytext ):
        try:
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
                repo_info['url'] = splittext[0]
                parsed_string = splittext[0].replace('https://github.com/','')
                repo_info['user_repo'] = parsed_string.replace('.git','')
                if splittext[0] == '':
                    pass
                else:
                    list_of_repos.append(repo_info)
            return list_of_repos
        except Exception as e: 
            print('Check your source text file formatting and try again')
            print(e)
    
    def verify_sha(self, mytoken, list_of_repos):
        g = Github(mytoken)
        try:
            for dic in list_of_repos:#for each repo
                repo = dic['user_repo']
                repo_data = g.get_repo(repo)
                commit = repo_data.get_commit(sha=dic['sha']) #d
            return True    
        except GithubException as e:
                return False

    def url_sha_combiner(self, dict_of_repos):
        try:
                for url in dict_of_repos:
                    combined = ":".join([url['url'],url['sha']])
                    url['combined'] = combined
                   
                return dict_of_repos
        
        except Exception as e: 
            print('Check your text file formatting')
            print(e)
    

    def parse_docker(self, mytoken, list_of_repos):
        try:
            g = Github(mytoken)
    
            for dic in list_of_repos:#for each repo
              
                repo = dic['user_repo']
                dic['file_w_image']=[]
                repo_data = g.get_repo(repo)
               # commit = repo.get_commit(sha=dic['sha']) #doesn't return True/False. Must check for failure
                contents = repo_data.get_contents("")
                dfp = DockerfileParser()
    
                while contents: #loop over file / path
                    file_content = contents.pop(0)
                    if file_content.type == "dir":
                        contents.extend(repo_data.get_contents(file_content.path)) #add dir contents to search
                    else:
                        if file_content.name == 'Dockerfile':# each file get image list in dict
                            file_images={}
                            file_images['images']=[]
                            file_images['Dockerfile'] = file_content.path
                            dfp.content = str(file_content.decoded_content, 'utf-8')
                            dockerfile_dicts = json.loads(dfp.json)
                          
                            for line_dict in dockerfile_dicts:
                                if 'FROM' in line_dict: #only need first col
                                    string_list = line_dict['FROM'].split(' ')
                                    file_images['images'].append(string_list[0])
                                  
                            dic['file_w_image'].append(file_images)
            return list_of_repos
        except Exception as e: 
            print('Check your scanned repos Dockerfile formatting')
            print(e)
    
    def structure_json(self,input):
        try:
            container_data={}
            data={}
            for url in input:
                data[url['combined']]={}
                for file in url['file_w_image']:
                    
                    data[url['combined']][file['Dockerfile']] = []
                    data[url['combined']][file['Dockerfile']].extend(file['images'])
            container_data['data']={}
            container_data['data'].update(data)
            return container_data
        except Exception as e: 
            print(e)

if __name__ == "__main__":
   
    if 'GITHUBTOKEN' and 'REPOSITORY_LIST_URL' not in os.environ:
        print('\033[31m' + ' * ERROR: Github API token and/or source url is missing. Exiting.')
        print('\033[39m')
        quit() 
        
    else:        
        mytoken = str(os.environ['GITHUBTOKEN'])
        source = str(os.environ['REPOSITORY_LIST_URL'])
        checker = Dockerchecker()
        data = {}
        
        text = checker.grab_txt_file(source) #Grab our endpoint data
        dict_of_repos_data = checker.clean_and_package(text) #Clean dead lines, start a dict for adding user/repo data and removing dead lines
        verified = checker.verify_sha(mytoken, dict_of_repos_data)
        if verified:
            repo_dict_with_url_sha = checker.url_sha_combiner(dict_of_repos_data) #combine url and sha and add to main dict
            completed_list = checker.parse_docker(mytoken, repo_dict_with_url_sha) #parse our repo for Dockerfiles then extract FROM line and 1ast position
            structured_dict = checker.structure_json(completed_list) #Structure everything into the required data format
            print(structured_dict)
        else:
            print('\033[31m' + ' * ERROR: Cannot Verify SHA within repo. Exiting.')
            print('\033[39m')
            quit() 
