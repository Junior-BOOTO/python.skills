import json
import socket
import pytest
from autodata import collection as c
from autodata.ingestion import DataError


@pytest.mark.parametrize('url', ['http://example.com/a', 'https://user:pass@example.com', 'https://example.com:8443', 'https://example.com/?api_key=secret'])
def test_unsafe_urls_rejected(url):
    with pytest.raises(DataError):
        c.public_endpoint(url)


@pytest.mark.parametrize('address', ['127.0.0.1', '10.0.0.1', '169.254.169.254', '::1', '224.0.0.1'])
def test_private_and_multicast_dns_rejected(monkeypatch, address):
    monkeypatch.setattr(c.socket, 'getaddrinfo', lambda *a, **k: [(socket.AF_INET, socket.SOCK_STREAM, 6, '', (address, 443))])
    with pytest.raises(DataError):
        c.public_endpoint('https://example.com')


def test_valid_public_resolution(monkeypatch):
    monkeypatch.setattr(c.socket, 'getaddrinfo', lambda *a, **k: [(socket.AF_INET, socket.SOCK_STREAM, 6, '', ('8.8.8.8', 443))])
    _, host, ip = c.public_endpoint('https://example.com/data')
    assert host == 'example.com' and ip == '8.8.8.8'


def test_nested_json_and_column_arrays():
    assert c.json_table(b'{"data":{"results":[{"x":1,"details":{"y":2}}]}}', 'data.results').columns.tolist() == ['x', 'details.y']
    assert c.json_table(b'{"x":[1,2],"y":[3,4]}').shape == (2, 2)


@pytest.mark.parametrize('payload,path', [(b'<html>error</html>', ''), (b'{"a":1}', ''), (b'[]', ''), (b'[{"x":[1,2]}]', ''), (b'{"data":[]}', 'missing')])
def test_non_tabular_json_rejected(payload, path):
    with pytest.raises(DataError):
        c.json_table(payload, path)


def test_pagination_provenance_and_total_budget(monkeypatch):
    calls = []
    def fetch(url, limit):
        calls.append((url, limit))
        return json.dumps([{'x': len(calls), 'y': 2}]).encode()
    monkeypatch.setattr(c, 'fetch_public', fetch)
    frame, meta = c.collect('https://example.com/data?category=abc', pages=2, page_parameter='page')
    assert frame['x'].tolist() == [1, 2]
    assert 'page=1' in calls[0][0] and 'page=2' in calls[1][0]
    assert calls[1][1] < calls[0][1]
    assert 'abc' not in json.dumps(meta)
    assert len(meta['sources']) == 2


def test_csv_collection(monkeypatch):
    monkeypatch.setattr(c, 'fetch_public', lambda *a: b'x;y\n1;2\n3;4')
    frame, _ = c.collect('https://example.com/data.csv', format='csv')
    assert frame.shape == (2, 2)


def test_schema_change_fails(monkeypatch):
    payloads = iter([b'[{"x":1}]', b'[{"y":1}]'])
    monkeypatch.setattr(c, 'fetch_public', lambda *a: next(payloads))
    with pytest.raises(DataError, match='colonnes'):
        c.collect('https://example.com', pages=2, page_parameter='page')


@pytest.mark.parametrize('status', [301, 403, 429, 500])
def test_http_errors_and_redirects_not_followed(monkeypatch, status):
    class Response:
        pass
    response = Response()
    response.status = status
    class Connection:
        def request(self, *a, **k): pass
        def getresponse(self): return response
        def close(self): pass
    monkeypatch.setattr(c, 'public_endpoint', lambda url: (c.urlsplit(url), 'example.com', '8.8.8.8'))
    monkeypatch.setattr(c, '_PinnedHTTPS', lambda *a: Connection())
    with pytest.raises(DataError, match=f'HTTP {status}'):
        c.fetch_public('https://example.com')



def test_response_size_limit(monkeypatch):
    class Response:
        status = 200
        def getheader(self, key, default=None): return default
        def read1(self, amount): return b'x' * amount
    class Connection:
        def request(self, *a, **k): pass
        def getresponse(self): return Response()
        def close(self): pass
    monkeypatch.setattr(c, 'public_endpoint', lambda url: (c.urlsplit(url), 'example.com', '8.8.8.8'))
    monkeypatch.setattr(c, '_PinnedHTTPS', lambda *a: Connection())
    with pytest.raises(DataError, match='5 Mo'):
        c.fetch_public('https://example.com', limit=10)
