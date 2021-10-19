import flask_unittest
from app import create_app
from flask import request,json
import requests


class TestClearbit(flask_unittest.ClientTestCase):

    app=create_app()

    def setUp(self,client):
        response = requests.get('http://127.0.0.1:5000/login', auth=('dzenankosuta', 'afc14'))
        self.token=json.loads(response.text)['token']
        self.headers = {'x-access-token': self.token}



        self.body={
            "email":"dzenan.kosuta@triglav.rs"
        }

    def test_cbit(self,client):
        resp = client.get('/cbit', json=self.body, headers=self.headers)
        self.assertEqual(resp.status_code, 200)
