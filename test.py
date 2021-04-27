import requests
from github import Github
import os

source="https://gist.githubusercontent.com/jmelis/c60e61a893248244dc4fa12b946585c4/raw/25d39f67f2405330a6314cad64fac423a171162c/sources.txt"
mytoken = str(os.environ['GITHUBTOKEN'])


r = requests.get(source)
mytext = r.text

for line in mytext.split('\n'):
    text  = line
    splittext = text.split(' ')
    print(splittext)

g = Github(mytoken)

for repo in g.get_user().get_repos():
    print(repo.name)
    print(dir(repo))

   # ['https://github.com/app-sre/qontract-reconcile.git', '30af65af14a2dce962df923446afff24dd8f123e']
   # ['https://github.com/app-sre/container-images.git', 'c260deaf135fc0efaab365ea234a5b86b3ead404']

