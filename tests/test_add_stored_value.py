import unittest, os
from taptogo import TapToGo

class TestDescribeCards(unittest.TestCase):
    def setUp(self):
        self.tap = TapToGo()
        self.tap.login(os.environ['TAPTOGO_EMAIL'], os.environ['TAPTOGO_PASSWORD'])
        self.cards = self.tap.describe_tap_cards()
    
    def test_add_card_obj(self):
        card_dict = {
            'name': 'Bruce Wayne',
            'num': '4444000000000000',
            'exp_month': '01',
            'exp_year': '20',
            'cvv': 123,
            'address': '732 Batcave Lane',
            'city': 'Gotham',
            'state': 'New York',
            'zip': '10001',
            'country': 'United States'
        }

        if len(self.cards) > 0:
            card_id = self.cards[0]['id']
            try:
                self.tap.add_stored_value(5.00, tap_card_id=card_id, card_dict=card_dict)
            except Exception as e:
                self.assertTrue(str(e) == 'Invalid credit card number' or "Cart amount doesn't match" in str(e))
        else:
            self.fail('Missing TAP cards')
    
    def test_add_params(self):
        if len(self.cards) > 0:
            reload_url = self.cards[0]['reload_url']
            try:
                self.tap.add_stored_value(
                    5.00, 
                    reload_url=reload_url, 
                    card_name='Bruce Wayne',
                    card_num='4444000000000000',
                    card_exp_month='01',
                    card_exp_year='20',
                    card_cvv=123,
                    card_address='732 Batcave Lane',
                    card_city='Gotham',
                    card_state='New York',
                    card_zip='10001',
                    card_country='United States'
                )
            except Exception as e:
                self.assertTrue(str(e) == 'Invalid credit card number' or "Cart amount doesn't match" in str(e))
        else:
            self.fail('Missing TAP cards')