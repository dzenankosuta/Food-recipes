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
        self.maxDiff=None
        self.exit={
            "Svi useri su": [
                {
                    "email": "dzenankosuta@gmail.com",
                    "first_name": "Dzenan",
                    "id": 1,
                    "last_name": "Kosuta",
                    "password_hash": "pbkdf2:sha256:150000$rt0dXPEI$0ec889d8ef7e707c628442f29b23ed94b9e84afba2687576d8ff0b11d75c81d5",
                    "username": "dzenankosuta"
                },
                {
                    "email": "peraperic@gmail.com",
                    "first_name": "Pera",
                    "id": 2,
                    "last_name": "Peric",
                    "password_hash": "pbkdf2:sha256:150000$2XQj9Fs7$1b01b60c1af2c776da87f7a228e2ba59236df9cccef720136dba801ea0372f6b",
                    "username": "peraperic"
                },
                {
                    "email": "damirdakic@gmail.com",
                    "first_name": "Damir",
                    "id": 3,
                    "last_name": "Dakic",
                    "password_hash": "pbkdf2:sha256:150000$Az0eXfzw$24d0f54c55e0651dde9c1250dd8130e13a32d7f51c3decb3bfa7f64e39c1ef68",
                    "username": "damirdakic"
                }
            ]
        }

    def test_all_users(self):
        resp=requests.get(self.url)
        self.assertEqual(resp.status_code , 200)
        self.assertDictEqual(resp.json() , self.exit)


if __name__=='__main__':
    unittest.main()
