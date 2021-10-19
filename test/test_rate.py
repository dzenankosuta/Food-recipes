import flask_unittest
from app import create_app
from flask import request, json
import requests



class TestRate(flask_unittest.ClientTestCase):

    app=create_app()

    def setUp(self,client):
        response = requests.get('http://127.0.0.1:5000/login', auth=('dzenankosuta', 'afc14'))
        self.token=json.loads(response.text)['token']
        self.headers = {'x-access-token': self.token}

        self.body={
            "ocena":"5",
            "recipe_id": "5"
        }

        self.exit={
            "Ocena je": {
                "ocena": 5,
                "recipe_id": 5,
                "user_id": 1
            }
        }


    def test_rate(self,client):

        resp = client.post('/rate', json=self.body, headers=self.headers)
        self.assertEqual(resp.status_code, 200)
        self.assertDictEqual(resp.get_json(), self.exit)
