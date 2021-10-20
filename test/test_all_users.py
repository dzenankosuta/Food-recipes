import unittest
from flask import jsonify, request
import requests,json


class TestAllUsers(unittest.TestCase):


    def setUp(self):
        self.url="http://127.0.0.1:5000/all_users"


    def test_all_users(self):
        resp=requests.get(self.url)
        self.assertEqual(resp.status_code , 200)



if __name__=='__main__':
    unittest.main()
