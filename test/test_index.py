import unittest
import requests

class TestIndex(unittest.TestCase):


    def setUp(self):

        self.url="http://127.0.0.1:5000/"

        self.exit={"Welcome to the food recipes!": ":-)"}

    def test_index(self):
        resp=requests.get(self.url)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json(), self.exit)

if __name__=='__main__':
    unittest.main()
