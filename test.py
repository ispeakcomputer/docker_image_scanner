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
        except Exception as e: 
            print('Check your source text file formatting and try again')
            print(e)

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
                                if 'FROM' in line_dict:
                                    #Cleaning string. need only 1st col
                                    string_list = line_dict['FROM'].split(' ')
                                    #print("string: " + string_list[0])
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
                #print(url)
                for file in url['file_w_image']:
                    
                    data[url['combined']][file['Dockerfile']] = []
                    data[url['combined']][file['Dockerfile']].extend(file['images'])
            container_data['data']={}
            container_data['data'].update(data)
            return container_data
                #for file in url['file_w_image']:
                #    print(inner_data[file['Dockerfile']]) 
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
        
        text = checker.grab_txt_file(source)
        dict_of_repos_data = checker.clean_and_package(text)
        repo_dict_with_url_sha = checker.url_sha_combiner(dict_of_repos_data)
        completed_list = checker.parse_docker(mytoken, repo_dict_with_url_sha)
        structured_dict = checker.structure_json(completed_list)
        print(structured_dict)
        #pprint.pprint(completed_list, indent=6)


