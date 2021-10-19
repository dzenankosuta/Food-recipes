import unittest
from flask import jsonify, request
import requests,json
#from foods.__init__ import app,db
#from foods.models import *
#from foods.schemas import *


class TestRegister(unittest.TestCase):

    @classmethod
    def tearDownClass(cls):
        print('tearDownClass')

    def setUp(self):
        print('setUp')
        self.url="http://127.0.0.1:5000/register"
        self.body={
        "email":"ab@gmail.com",
        "username":"ab",
        "first_name":"A",
        "last_name":"B",
        "password":"afc14"
        }
        self.exit={
        "Registracija je uspesna za sledeceg usera": {
            "email": "ab@gmail.com",
            "first_name": "A",
            "last_name": "B",
            "password": "afc14",
            "username": "ab"
            }
        }

    def test_register(self):
        resp=requests.post(self.url , json=self.body)
        self.assertEqual(resp.status_code , 200)
        self.assertDictEqual(resp.json() , self.exit)




if __name__=='__main__':
    unittest.main()
