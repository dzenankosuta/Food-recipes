import flask_unittest
from app import create_app
from flask import request,json
import requests


class TestRecipeWithMinIng(flask_unittest.ClientTestCase):

    app=create_app()

    def setUp(self,client):
        response = requests.get('http://127.0.0.1:5000/login', auth=('dzenankosuta', 'afc14'))
        self.token=json.loads(response.text)['token']
        self.headers = {'x-access-token': self.token}

        self.exit={
            "Recept sa najmanjim brojem sastojaka je ": [
                [
                    "Naziv recepta: torta",
                    "Broj sastojaka recepta: 2"
                ]
            ]
        }
        
    def test_min_ingredients(self,client):
        resp = client.get('/min_ingredients', headers=self.headers)
        self.assertEqual(resp.status_code, 200)
        self.assertDictEqual(resp.get_json(), self.exit)
