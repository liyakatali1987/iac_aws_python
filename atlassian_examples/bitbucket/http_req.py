import requests


class HttpRequests:
    def __init__(self, type, uri, user, pwrd, data={}, headers={}, params={}):
        self.type = type
        self.uri = uri
        self.user = user
        self.pwrd = pwrd
        self.data = data
        self.headers = {'Accept': 'application/json',
                        'Content-Type': 'application/json'}
        self.params = params

    def http_requests(self):
        resp = ""
        if self.type == 'get':
            resp = requests.get(self.uri, headers=self.headers,
                                params=self.params, auth=(self.user, self.pwrd))
        if self.type == 'post':
            resp = requests.post(self.uri, data=self.data, headers=self.headers,
                                 params=self.params, auth=(self.user, self.pwrd))
        if self.type == 'put':
            resp = requests.put(self.uri, data=self.data, headers=self.headers,
                                params=self.params, auth=(self.user, self.pwrd))
        if self.type == 'delete':
            resp = requests.delete(self.uri, data=self.data, headers=self.headers,
                                   params=self.params, auth=(self.user, self.pwrd))
        return resp
