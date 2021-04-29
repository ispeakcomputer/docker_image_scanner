# Dockerfile Source Scanner

A part of our compliance requirements, we want to make sure that we are building containers with trusted source images.

Dockerfile Source Scanner is a tool that given a list of repositories, it identifies all the Dockerfile files inside each repository,
 extracts the image names from the FROM statement, and returns a json with the aggregated information for all the repositories.

### Quick Launch Locally 
1. Pull down the Docker Image ```docker pull ispeakcomputer/scanner:latest```
2. Now lets run the image. Here you will need a [Github token](https://github.com/settings/tokens) with read permissions and the repository text file list source url. 
   The test file must have the repo url a space and a SHA on each line. I have included a url to test with below. Just create a Github token and run
   
   ```sudo docker run --env GITHUBTOKEN='<Your Token Here>' --env REPOSITORY_LIST_URL='https://gist.githubusercontent.com/jmelis/c60e61a893248244dc4fa12b946585c4/raw/25d39f67f2405330a6314cad64fac423a171162c/sources.txt' ispeakcomputer/scanner ```

### Deploy As Kubernetes Job
1. Clone this repo with  ```git clone git@github.com:ispeakcomputer/docker_image_scanner.git```
2. Move into the deployment repo by running ```cd docker_image_scanner/deployment ```
3. You will need a [Github token](https://github.com/settings/tokens) with read permissions for adding to a file
4. You must convert the Github token to Base64 before adding to your kubernetes secrets yaml by running ```echo -n '<Add your token here>' | base64 ``` 
4. Open up and edit **secret_template.yaml** and put the the encoded data as the GITHUBTOKEN then save the file
5. In the same directory deploy your Kubernetes secrets with ```kubectl apply -f secrets_template.yaml```
6. Next deploy your the job by running ```kubectl apply -f deploy.yaml```
7. Run ```pods=$(kubectl get pods --selector=job-name=scanner --output=jsonpath='{.items[*].metadata.name}');echo $pod``` for find your jobs pod. 
8. Once you get your pod check its output with ```kubectl logs <pod>```
