from unittest import TestCase
import json


class Test(TestCase):
    def test_hmac(self):
        import hmac
        import requests

        port = 18000
        host = 'localhost'

        data = hmac.digest(b'key', json.dumps({"a": 1}).encode(), 'sha256')

        r = requests.get('http://%s:%d' % (host, port), data=data)
        print(r.text)