import unittest
from flask import jsonify, request
import requests,json
#from foods.__init__ import app,db
#from foods.models import *
#from foods.schemas import *

class TestAllUsers(unittest.TestCase):

    @classmethod
    def tearDownClass(cls):
        print('tearDownClass')

    def setUp(self):
        print('setUp')
        self.url="http://127.0.0.1:5000/all_users"


    def test_all_users(self):
        resp=requests.get(self.url)
        self.assertEqual(resp.status_code , 200)



if __name__=='__main__':
    unittest.main()
