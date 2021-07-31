#!/bin/bash
set -e

# First check for env variables: REQUIREMENTS_FILE, BITBUCKET_PR_ID, BITBUCKET_REPO_SLUG, BITBUCKET_WORKSPACE, BITBUCKET_USER & BITBUCKET_PWD
declare -a ENV_VARS=("REQUIREMENTS_FILE" "BITBUCKET_PR_ID" "BITBUCKET_REPO_SLUG" "BITBUCKET_WORKSPACE" "BITBUCKET_USER" "BITBUCKET_PWD")
any_var_not_set=false

for VAR in "${ENV_VARS[@]}"
do
  if test -z ${!VAR}
  then
    echo "$VAR environment variable not set"
    any_var_not_set=true
  fi
done

# Fail if one of vars is not set
if $any_var_not_set
then
  exit 1
fi

# Check if requirements file exists
if ! test -f "$REQUIREMENTS_FILE"
then
  echo "$REQUIREMENTS_FILE not found"
  exit 1
fi

# Get piprot output
declare piprot_output=$(piprot $REQUIREMENTS_FILE)

# Create temp folder
mkdir -p ./tmp

# Output to json, some manipulation to get tabs and new lines correct for curl command
echo "$piprot_output" | awk -vRS="\n" -vORS="  \\\\n" '1' > ./tmp/raw.json

# Append and prepend other required JSON contents
printf '%s' '{"content":{"raw":"**piprot report:**  \n' "$(cat ./tmp/raw.json)" >./tmp/raw.json
echo '"}}' >> ./tmp/raw.json

# Create PR
code=$(curl -sSL -w '%{http_code}' --output ./tmp/curl_output.txt --user $BITBUCKET_USER:$BITBUCKET_PWD --data-binary @tmp/raw.json  -H "Content-Type:application/json" -X POST https://api.bitbucket.org/2.0/repositories/${BITBUCKET_WORKSPACE}/${BITBUCKET_REPO_SLUG}/pullrequests/${BITBUCKET_PR_ID}/comments)

if [[ "$code" =~ ^2 ]]
then
    echo "Success!"
elif [[ "$code" = 401 ]]
then
    echo "Unauthorized error $code"
    exit 1
else
    echo "Returned error $code"
    exit 1
fi