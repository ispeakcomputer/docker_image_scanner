import requests
from github import Github
import os

source="https://gist.githubusercontent.com/jmelis/c60e61a893248244dc4fa12b946585c4/raw/25d39f67f2405330a6314cad64fac423a171162c/sources.txt"

r = requests.get(source)
mytext = r.text

list_of_repos=[]
for line in mytext.split('\n'):
    # ['https://github.com/container-images.git', 'c260deaf135fc0efaab365ea234a5b86b3ead404']
    # converted now to this:
    #['app-sre/qontract-reconcile', '30af65af14a2dce962df923446afff24dd8f123e']
    text  = line
    splittext = text.split(' ')
    # Strip github url and file extension
    splittext[0] = splittext[0].replace('https://github.com/','')
    splittext[0] = splittext[0].replace('.git','')
    # remove dead line 
    if splittext[0] == '':
        pass
    else:
        list_of_repos.append(splittext)

print(list_of_repos) 

mytoken = str(os.environ['GITHUBTOKEN'])
g = Github(mytoken)

for list in list_of_repos:
    repo = list[0]
    print(repo)
    repo_data = g.get_repo(repo)
    contents = repo_data.get_contents("")

    while contents:
        file_content = contents.pop(0)
        if file_content.type == "dir":
            contents.extend(repo_data.get_contents(file_content.path))
        else:
            print(file_content)








contents = repo.get_contents("")

while contents:
    file_content = contents.pop(0)
    if file_content.type == "dir":
        contents.extend(repo.get_contents(file_content.path))
    else:
        print(file_content)




if __name__ == "__main__":
    if not mytoken:
        print('\033[31m' + ' * Error: Github token missing. Exiting.')
        print('\033[39m')
        quit() 
