import requests


class HttpRequests:
    def __init__(self, req_type, uri, user, pwrd, data=None, headers=None, params=None, timeout=30):
        """Initializing class variables."""
        self.type = req_type
        self.uri = uri
        self.user = user
        self.pwrd = pwrd
        self.data = data
        # Default headers
        default_headers = {'Accept': 'application/json',
                           'Content-Type': 'application/json'}
        if headers: # If custom headers are provided
            default_headers.update(headers) # Merge/override with custom headers
        self.headers = default_headers
        self.params = params
        self.timeout = timeout

    def http_requests(self):
        resp = ""
        if self.type == 'get':
            resp = requests.get(self.uri, headers=self.headers,
                                params=self.params, auth=(self.user, self.pwrd), timeout=self.timeout)
        if self.type == 'post':
            resp = requests.post(self.uri, data=self.data, headers=self.headers,
                                 params=self.params, auth=(self.user, self.pwrd), timeout=self.timeout)
        if self.type == 'put':
            resp = requests.put(self.uri, data=self.data, headers=self.headers,
                                params=self.params, auth=(self.user, self.pwrd), timeout=self.timeout)
        if self.type == 'delete':
            resp = requests.delete(self.uri, headers=self.headers,
                                   params=self.params, auth=(self.user, self.pwrd), timeout=self.timeout) # Removed data=self.data
        return resp
