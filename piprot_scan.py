import io
import json
import os
import sys
import errno
import requests
from contextlib import redirect_stdout

from piprot import piprot

ENV_VARS = [
    "REQUIREMENTS_FILE",
    "BITBUCKET_PR_ID",
    "BITBUCKET_REPO_SLUG",
    "BITBUCKET_WORKSPACE",
    "BITBUCKET_USER",
    "BITBUCKET_PWD"
]


def __check_env_vars(env_vars: [str]) -> None:
    """
    Check if all environment variables are present
    :return: None
    """
    for var in env_vars:
        try:
            os.environ[var]
        except KeyError as e:
            print(f"Environment variable {var} not set!", file=sys.stderr)
            raise e


def __check_existence_requirements_file(requirements_file_path: str) -> None:
    if not os.path.isfile(requirements_file_path):
        print(f"Requirements file {requirements_file_path} does not exist!", file=sys.stderr)
        raise FileNotFoundError(
            errno.ENOENT, os.strerror(errno.ENOENT), requirements_file_path)


def __get_outdated_dependencies(requirements_file_path: str) -> str:
    with open(requirements_file_path, "r") as req_file:
        # piprot prints it output, find a way to capture the output as str
        stdout = io.StringIO()
        with redirect_stdout(stdout):
            try:
                piprot.main([req_file], outdated=True, verbose=True)
            except SystemExit:
                print('exited')

        # Get output of piprot, remove last 2 lines (exited + empty line)
        piprot_output = stdout.getvalue().rsplit("\n", 2)[0]
        return piprot_output


def __get_request_body(piprot_output: str) -> dict:
    raw_string = json.dumps(piprot_output).replace("\\n", "    \n")

    content = {
        "content":
            {
                "raw": "**piprot report:**  \n" + raw_string.strip("\"")
            }
    }
    return content


def __get_url(bb_workspace: str,
              bb_repo_slug: str,
              bb_pr_id: str) -> str:
    return f"https://api.bitbucket.org/2.0/repositories/{bb_workspace}/{bb_repo_slug}/pullrequests/{bb_pr_id}/comments"


def __create_pr_comment(request_body: dict,
                        bb_workspace: str,
                        bb_repo_slug: str,
                        bb_pr_id: str,
                        username: str,
                        password: str):
    url = __get_url(bb_workspace, bb_repo_slug, bb_pr_id)
    r = requests.post(url=url, json=request_body, auth=(username, password))

    if r.status_code != 201:
        print(f"HTTP status code: {r.status_code}, reason: {r.reason}!", file=sys.stderr)
        raise Exception("Failed to create PR comment.")
    else:
        print("Succeeded!")


def main(requirements_file_path: str,
         bb_workspace: str,
         bb_repo_slug: str,
         bb_pr_id: str,
         username: str,
         password: str):
    __check_existence_requirements_file(requirements_file_path=requirements_file_path)
    piprot_output = __get_outdated_dependencies(requirements_file_path=requirements_file_path)
    request_body = __get_request_body(piprot_output=piprot_output)
    __create_pr_comment(request_body=request_body,
                        bb_workspace=bb_workspace,
                        bb_repo_slug=bb_repo_slug,
                        bb_pr_id=bb_pr_id,
                        username=username,
                        password=password)


if __name__ == "__main__":
    __check_env_vars(ENV_VARS)
    main(requirements_file_path=os.environ["REQUIREMENTS_FILE"],
         bb_workspace=os.environ["BITBUCKET_WORKSPACE"],
         bb_repo_slug=os.environ["BITBUCKET_REPO_SLUG"],
         bb_pr_id=os.environ["BITBUCKET_PR_ID"],
         username=os.environ["BITBUCKET_USER"],
         password=os.environ["BITBUCKET_PWD"]
         )
