import unittest
from flask import jsonify, request
import requests,json
#from foods.__init__ import app,db
#from foods.models import *
#from foods.schemas import *

class TestIndex(unittest.TestCase):

    @classmethod
    def tearDownClass(cls):
        print('tearDownClass')

    def setUp(self):
        print('setUp')
        self.url="http://127.0.0.1:5000/"
        self.exit={
        "Welcome to the food recipes!": ":-)"
        }

    def test_index(self):
        resp=requests.get(self.url)
        self.assertEqual(resp.status_code , 200)
        self.assertEqual(resp.json() , self.exit)



if __name__=='__main__':
    unittest.main()
