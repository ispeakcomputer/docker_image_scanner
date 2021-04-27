import requests
from github import Github
import os
import json
from dockerfile_parse import DockerfileParser


source="https://gist.githubusercontent.com/jmelis/c60e61a893248244dc4fa12b946585c4/raw/25d39f67f2405330a6314cad64fac423a171162c/sources.txt"

r = requests.get(source)
mytext = r.text

list_of_repos=[]
for line in mytext.split('\n'):
   
    repo_info={}

    text  = line
    splittext = text.split(' ')
    
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
print(list_of_repos) 

# ------------------------------------GITHUB------------------------------
mytoken = str(os.environ['GITHUBTOKEN'])
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
