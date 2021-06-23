import os
from pathlib import Path
import subprocess
import json
from http_req import HttpRequests
from getpass import getpass

"""
    This script will help user to create a bitbucket repo with a readme file.

"""


def validate_inputs(values):
    if None in values:
        raise Exception('Invalid Value Provided')


class BitbucketApi:
    def __init__(self, host, user, password):
        self.host = f'{host}/rest/api/latest'
        self.user = user
        self.password = password

    def __bitbucket_requests(self, type, url, data=None):
        try:
            response = HttpRequests(type, url, self.user,
                                    self.password, data=json.dumps(data)).http_requests()
            if response.text:
                return response.status_code, response.json()
            else:
                return response.status_code, None
        except Exception as e:
            return None, e

    def create_repository(self):
        project_key = input('Enter project key (*required): ')
        repository_name = input('Enter repository name (*required): ')
        validate_inputs([project_key, repository_name])
        description = input('Enter Description (optional) : ')
        url = f'{self.host}/projects/{project_key}/repos'
        data = {
            "slug": repository_name,
            "name": repository_name,
            "project": {
                "key": project_key
            },
            "description": description if description else f'New Repository {repository_name}'
        }

        status, response = self.__bitbucket_requests('post', url, data)
        if status == 201:
            res = self.add_readme_file(
                repository_name, response['links']['clone'][0]['href'])
            if not res:
                raise Exception(
                    'Could not add the readme file to the repository')

        return status, response

    def add_readme_file(self, repo_name, clone_url):
        print(clone_url)
        curr_dir = os.getcwd()
        temp_dir = f'{curr_dir}/temp'

        Path(temp_dir).mkdir(parents=True, exist_ok=True)
        try:
            clone = subprocess.Popen(
                ['git', 'clone', clone_url], stdout=subprocess.PIPE, cwd=temp_dir)
            output, err = clone.communicate()

        except FileNotFoundError as e:
            print('Creating temp folder')
        except Exception as e:
            print('Creating temp folder')

        try:
            repo_dir = f'{temp_dir}/{repo_name}'
            with open(f'{temp_dir}/{repo_name}/README.md', 'w') as f:
                f.write(' # README.md file')

            add = subprocess.Popen(
                ['git', 'add', 'README.md'], stdout=subprocess.PIPE, cwd=repo_dir)
            commit = subprocess.Popen(
                ['git', 'commit', '-m', 'Adding Readme file'], stdin=add.stdout, stdout=subprocess.PIPE, cwd=repo_dir)
            add.stdout.close()
            push = subprocess.Popen(
                ['git', 'push'], stdin=commit.stdout, stdout=subprocess.PIPE, cwd=repo_dir)
            commit.stdout.close()
            output, err = push.communicate()

            delete = subprocess.Popen(
                ['rm', '-rf', f'{temp_dir}/'],  stdout=subprocess.PIPE)
            output, err = delete.communicate()
            print(output)
            if not err:
                return 1
            else:
                return 0
        except Exception as e:
            return e


host = input(
    'Enter host address : [e.g. http://localhost:7990] ') or 'http://localhost:7990'
user = input('Enter userid : ')
password = getpass(prompt='Enter password : ')


try:
    validate_inputs([host, user, password])
    bb_api = BitbucketApi(host, user, password)
    status, response = bb_api.create_repository()
    print(status, response)
except Exception as e:
    print(e)
