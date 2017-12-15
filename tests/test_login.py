import unittest, os
from taptogo import TapToGo

class TestLogin(unittest.TestCase):
    def setUp(self):
        self.tap = TapToGo()
    
    def test_failed_login(self):
        email = os.environ['TAPTOGO_EMAIL']
        password = os.environ['TAPTOGO_PASSWORD'] + '_wrong'

        self.assertFalse(self.tap.login(email, password))
    
    def test_successful_login(self):
        email = os.environ['TAPTOGO_EMAIL']
        password = os.environ['TAPTOGO_PASSWORD']

        self.assertTrue(self.tap.login(email, password))