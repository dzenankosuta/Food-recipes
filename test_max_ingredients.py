import flask_unittest
from app import create_app
from flask import request,json
import requests


class TestRecipeWithMaxIng(flask_unittest.ClientTestCase):

    app=create_app()

    def setUp(self,client):
        response = requests.get('http://127.0.0.1:5000/login', auth=('dzenankosuta', 'afc14'))
        self.token=json.loads(response.text)['token']
        self.headers = {'x-access-token': self.token}

        self.exit={
            "Recept sa najvecim brojem sastojaka je ": [
                [
                    "Naziv recepta: corba",
                    "Broj sastojaka recepta: 7"
                ]
            ]
        }
        
    def test_max_ingredients(self,client):
        resp = client.get('/max_ingredients', headers=self.headers)
        self.assertEqual(resp.status_code, 200)
        self.assertDictEqual(resp.get_json(), self.exit)
