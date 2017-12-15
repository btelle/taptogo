import unittest, os
from taptogo import TapToGo

class TestDescribeCards(unittest.TestCase):
    def setUp(self):
        self.tap = TapToGo()
        self.tap.login(os.environ['TAPTOGO_EMAIL'], os.environ['TAPTOGO_PASSWORD'])
    
    def test_describe(self):
        cards = self.tap.describe_tap_cards()
        
        self.assertEqual(type(cards), list)
        self.assertTrue(len(cards) > 0)

        for card in cards:
            self.assertTrue(len(card.get('id', '')) > 0)
            self.assertTrue(len(card.get('name', '')) > 0)
            self.assertEqual(type(card.get('balance', None)), float)
            self.assertTrue('reload_url' in card)
            self.assertTrue('history_url' in card)
            self.assertTrue('cancel_url' in card)
