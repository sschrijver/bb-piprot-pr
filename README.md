# Bitbucket piprot Pull Request Review
This Docker container helps you create automatic pull request comments.  
Provide the following variables in the pipeline, using account variables or repository variables.
Except for the `BITBUCKET_USER` and `BITBUCKET_PWD`, everything should be provided automatically.

```
REQUIREMENTS_FILE - path to the requirements.txt (Default: requirements.txt)
BITBUCKET_PR_ID - Pull Request ID
BITBUCKET_REPO_SLUG - Slug of the repository
BITBUCKET_WORKSPACE - Workspace name
BITBUCKET_USER - Username of Bitbucket (bot) user
BITBUCKET_PWD - Password of Bitbucket (bot) user
```

## Local testing
```
docker run \
-e "REQUIREMENTS_FILE=requirements.txt" \
-e "BITBUCKET_PR_ID=1" \
-e "BITBUCKET_REPO_SLUG=repo_name" \
-e "BITBUCKET_WORKSPACE=workspace_name" \
-e "BITBUCKET_USER=user@mail.com" \
-e "BITBUCKET_PWD=password" 
image:tag  
```
