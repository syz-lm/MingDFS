from unittest import TestCase
from mingdfs.utils import load_hosts, dump_hosts
import pprint
import logging
# logging.basicConfig(level=logging.DEBUG)


class Test(TestCase):
    def test_load_hosts(self):
        pprint.pprint(load_hosts())

    def test_dump_hosts(self):
        ih = load_hosts()
        dump_hosts(ih)