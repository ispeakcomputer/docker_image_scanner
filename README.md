# Dockerfile Source Scanner

A part of our compliance requirements, we want to make sure that we are building containers with trusted source images.

Dockerfile Source Scanner is a tool that given a list of repositories, it identifies all the Dockerfile files inside each repository,
 extracts the image names from the FROM statement, and returns a json with the aggregated information for all the repositories.

### Quick Launch  
1. Pull down the Docker Image ```docker pull ispeakcomputer/scanner:latest ```
2. Now lets run the image. Here you will need a [Github token](https://github.com/settings/tokens) with read permissions and the repository text file list source url. 
   The test file must have the repo url a space and a SHA on each line. I have included a url to test with below. Just create a Github token and run
   ```sudo docker run  \
      --env GITHUBTOKEN='<Your Token Here>' \
      --env REPOSITORY_LIST_URL='https://gist.githubusercontent.com/jmelis/c60e61a893248244dc4fa12b946585c4/raw/25d39f67f2405330a6314cad64fac423a171162c/sources.txt' \
        ispeakcomputer/scanner ```


1. Clone this repo with  ```git clone git@github.com:ispeakcomputer/docker_image_scanner.git```
2. Move into the repo by running ```cd docker_image_scanner ```
3. Now make a docker image from our Dockerfile ```docker build -t scanner . ```
