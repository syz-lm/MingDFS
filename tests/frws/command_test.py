import unittest
import subprocess
from mingdfs.frws import command


class Test(unittest.TestCase):
    def main(self, times):
        try:
            p = subprocess.Popen(["/usr/local/python3.8/bin/python3.8", command.__file__,
                               '--HOST', '0.0.0.0', '--PORT', '15677', '--HOST_NAME', 'frws0',
                               '--FMWS_HOST_NAME', 'fmws0', '--FMWS_PORT', '15675',
                               '--FMWS_KEY', 'mm5201314', '--FRWS_KEY', 'mm5201314',
                               '--SAVE_DIRS', '/mnt/hgfs/mingdfs/frws', '/mnt/hgfs/mingdfs/frws1'], stdout=subprocess.PIPE)
            p.wait(timeout=times)
            print(p.stdout.read())
        except subprocess.TimeoutExpired as e:
            print(e)
            p.kill()

    def test_main_3_seconds(self):
        self.main(3)

    def test_main_3600_seconds(self):
        self.main(3600)