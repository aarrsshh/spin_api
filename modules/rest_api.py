import time
import requests
import requests.exceptions
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

class HttpError(Exception):
    def __init__(self, response_code, message=None):
        if message is None:
            message = "HTTP request resulted in HTTP status: [%s]" % (
                response_code)
        Exception.__init__(self, message)
        self.response_code = response_code
        self.message = message
    def __str__(self):
        return str(self.message)

class HttpException(Exception):
    def __init__(self, message=None):
        if message is None:
            message = "HTTP request resulted in network error: [%s]" % (
                message)
        Exception.__init__(self, message)
        self.message = message
    def __str__(self):
        return str(self.message)

def __call_api(server, method, api, data, **kwargs):
    kwargs = {} if not kwargs else kwargs
    function = getattr(requests, method)
    headers = {
        'Accept': 'application/json',
        "Content-Type": "application/json"
    }
    headers.update(kwargs.get("headers", {}))
    kwargs['headers'] = headers
    kwargs['timeout'] = kwargs.get('timeout', (15, 60))
    kwargs['verify'] = kwargs.get('verify', False)
    api_uri = server
    if api:
        api_uri = ''.join([server, api])
    return __execute_request(method, function, api_uri, data, **kwargs)

def __execute_request(method, function, api_uri, data, **kwargs):
    error_handler = kwargs.pop('error_handler', None)
    raw_output = kwargs.pop('raw_output', False)
    retries = kwargs.pop("retries", 3)
    back_off_time = 1
    while True:
        try:
            if method == 'get':
                response = function(api_uri,
                                    params=data,
                                    **kwargs)
            else:
                response = function(api_uri,
                                    data=data,
                                    **kwargs)
        except requests.exceptions.RequestException as http_error:
            if retries > 0:
                back_off_time *= 2 if back_off_time < 64 else 1
                time.sleep(back_off_time)
                retries -= 1
                continue
            raise HttpException(str(http_error)) from http_error
        if response.status_code >= 500 and retries > 0:
            back_off_time *= 2 if back_off_time < 64 else 1
            time.sleep(back_off_time)
            retries -= 1
        else:
            break
    return _process_response(response, raw_output, error_handler)

def _process_response(response, raw_output, error_handler):
    r_json = None
    if raw_output:
        output = response.text
    else:
        try:
            r_json = response.json()
            output = r_json
        except ValueError as err:
            output = {}
            print(err)
    if response.status_code == 404 and output == '{"error":"NOT_FOUND"}':
        return output
    if not response.ok:
        message = r_json
        if error_handler and r_json:
            message = error_handler(r_json)
        raise HttpError(response.status_code, message)
    return output

def http_get(server, api, data=None, **kwargs):
    response = __call_api(server,
                          'get',
                          api,
                          data,
                          **kwargs)
    return response

def http_delete(server, api="", data=None, **kwargs):
    response = __call_api(server,
                          'delete',
                          api,
                          data,
                          **kwargs)
    return response
