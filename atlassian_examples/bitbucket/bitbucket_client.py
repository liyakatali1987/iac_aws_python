import json
from http_req import HttpRequests


""" returns the bitbucket client"""


class BitbucketApi:
    def __init__(self, host, user, password):
        self.host = f'{host}/rest/api/latest'
        self.user = user
        self.password = password

    def bitbucket_requests(self, type, url, data=None, params=None):
        try:
            response = HttpRequests(type, url, self.user,
                                    self.password, data=json.dumps(data), params=params).http_requests()
            if response.text:
                return response.status_code, response.json()
            else:
                return response.status_code, None
        except Exception as e:
            return None, e
