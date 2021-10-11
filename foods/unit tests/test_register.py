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
        "email":"dzenankosuta@gmail.com",
        "username":"dzenankosuta",
        "first_name":"Dzenan",
        "last_name":"Kosuta",
        "password":"afc14"
        }
        self.exit={
        "Registracija je uspesna za sledeceg usera": {
            "email": "dzenankosuta@gmail.com",
            "first_name": "Dzenan",
            "last_name": "Kosuta",
            "password": "afc14",
            "username": "dzenankosuta"
            }
        }

    def test_register(self):
        resp=requests.post(self.url , json=self.body)
        self.assertEqual(resp.status_code , 200)
        self.assertDictEqual(resp.json() , self.exit)




if __name__=='__main__':
    unittest.main()
