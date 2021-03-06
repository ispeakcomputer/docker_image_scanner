# Dockerfile Source Scanner

We want to make sure that we are building containers with trusted source images.

Dockerfile Source Scanner is a tool that given a list of repositories, it identifies all the Dockerfile files inside each repository,
 extracts the image names from the FROM statement, and returns a json with the aggregated information for all the repositories.

### Quick Launch
1. Pull down the Docker Image ```docker pull ispeakcomputer/scanner:latest```
2. Now lets run the image. Here you will need a [Github token](https://github.com/settings/tokens) with read permissions and the repository text file list source url. 
   I have included a url to test with below. Just create a Github token and run with this command.
   
   ```sudo docker run --env GITHUBTOKEN='<Your Token Here>' --env REPOSITORY_LIST_URL='https://gist.githubusercontent.com/jmelis/c60e61a893248244dc4fa12b946585c4/raw/25d39f67f2405330a6314cad64fac423a171162c/sources.txt' ispeakcomputer/scanner ```

### Deploy As Kubernetes Job
1. Clone this repo with  ```git clone git@github.com:ispeakcomputer/docker_image_scanner.git```
2. Move into the deployment repo by running ```cd docker_image_scanner/deployment ```
3. You will need a [Github token](https://github.com/settings/tokens) with read permissions
4. You must convert the Github token to Base64 before adding to your kubernetes secrets yaml by running ```echo -n '<Add your token here>' | base64 ``` 
4. Open up and edit **secret_template.yaml** and put the the encoded data as the GITHUBTOKEN then save the file
5. In the same directory deploy your Kubernetes secrets with ```kubectl apply -f secrets_template.yaml```
6. Next deploy your job by running ```kubectl apply -f deploy.yaml```
7. Run ```pods=$(kubectl get pods --selector=job-name=scanner --output=jsonpath='{.items[*].metadata.name}');echo $pod``` for finding your jobs pod. 
8. Once you get your pod check its output with ```kubectl logs <pod>```

### Running Locally
1. Jump into Github and grab tokens for read-only access (HERE)[https://docs.github.com/en/github/authenticating-to-github/creating-a-personal-access-token#creating-a-token]
2. Clone this repo with ```git clone git@github.com:ispeakcomputer/docker_image_scanner.git```
3. Run ```cd docker_image_scanner.git ```to move into directory
4. Next run ```python3 -m venv venv ``` to create a virtual environment
5. Next run ```source venv/bin/activate```
6. Next Install all our requirements ```python3 -m pip install -r requirements.txt ```
7. Open **start_here.sh** and enter your keys and secrets from step 1 where you see **GITHUBTOKEN** and **REPOSITORY_LIST_URL**. Save and close.
8. Make the start script execute with ```chmod +x start_here.sh ```
9. Run the script with ```./start_here.sh```


### Example Input

The source text url contains a repo url, a space, and the a SHA per line

```
https://github.com/app-sre/qontract-reconcile.git 30af65af14a2dce962df923446afff24dd8f123e
https://github.com/app-sre/container-images.git c260deaf135fc0efaab365ea234a5b86b3ead404
```

### Example Output

The output is a url:sha key nesting the Dockerfile path and a list of the images contained inside the Dockerfile

```
{'data': 
   {'https://github.com/app-sre/qontract-reconcile.git:30af65af14a2dce962df923446afff24dd8f123e': {'dockerfiles/Dockerfile': ['quay.io/app-sre/qontract-reconcile-base:0.3.1']}, 
    'https://github.com/app-sre/container-images.git:c260deaf135fc0efaab365ea234a5b86b3ead404': {'jiralert/Dockerfile': ['registry.access.redhat.com/ubi8/go-toolset:latest', 'registry.access.redhat.com/ubi8-minimal:8.2'], 'qontract-reconcile-base/Dockerfile': ['registry.access.redhat.com/ubi8/ubi:8.2', 'registry.access.redhat.com/ubi8/ubi:8.2']}}}
```
### ??? Design ???

The program is written in Python3 using object oriented design. It doesn't start without the required url/token,
has a exception handling built in, and verifies repos against commit SHAs

***The program follows these steps***

1. Check for Github Token and Url or exit while alerting user
2. Grab our URL endpoint data
3. Start a main dict for adding user/repo data striped from url, url, and sha while removing dead lines from input
4. Check that the commit SHA is found within the repo to verify it
5. Combine url and sha into a single string with : delimiter and add to main dict. A requirement for output.
6. Parse our repos Dockerfiles then extract its path as well as images from 'FROM' lines then add both to main dictionary
7. Structure everything into the required data format from existing dictionary.



