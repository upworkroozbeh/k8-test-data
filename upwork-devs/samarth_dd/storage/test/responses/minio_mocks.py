from http import client as httplib

from nose.tools import eq_

from minio.fold_case_dict import FoldCaseDict

class MockResponse(object):
    def __init__(self, method, url, headers, status_code,
                 response_headers=None, content=None):
        self.method = method
        self.url = url
        self.request_headers = FoldCaseDict()
        for header in headers:
            self.request_headers[header] = headers[header]
        self.status = status_code
        self.headers = response_headers
        self.data = content
        if content is None:
            self.reason = httplib.responses[status_code]

    # noinspection PyUnusedLocal
    def read(self, amt=1024):
        return self.data

    def mock_verify(self, method, url, headers):
        eq_(self.method, method)
        eq_(self.url, url)
        if headers:
            for header in headers:
                eq_(self.request_headers[header], headers[header])

    # noinspection PyUnusedLocal
    def stream(self, chunk_size=1, decode_unicode=False):
        if self.data is not None:
            return iter(bytearray(self.data, 'utf-8'))
        return iter([])

    # dummy release connection call.
    def release_conn(self):
        return

    def __getitem__(self, key):
        if key == "status":
            return self.status


class MockConnection(object):
    def __init__(self):
        self.requests = []

    def mock_add_request(self, request):
        self.requests.append(request)

    # noinspection PyUnusedLocal
    def request(self, method, url, headers, redirect=False):
        # only pop off matching requests
        return_request = self.requests[0]
        return_request.mock_verify(method, url, headers)
        return self.requests.pop(0)

    # noinspection PyRedeclaration,PyUnusedLocal,PyUnusedLocal

    def urlopen(self, method, url, headers={}, preload_content=False,
                body=None, redirect=False):
        return self.request(method, url, headers)