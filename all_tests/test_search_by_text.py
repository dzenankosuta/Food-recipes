import flask_unittest
from app import create_app
from flask import request,json
import requests


class TestSearchByText(flask_unittest.ClientTestCase):

    app=create_app()

    def setUp(self,client):
        response = requests.get('http://127.0.0.1:5000/login', auth=('dzenankosuta', 'afc14'))
        self.token=json.loads(response.text)['token']
        self.headers = {'x-access-token': self.token}
        self.maxDiff=None
        null='null'
        self.body={
            "recipe_text":"kuva"
        }
        self.exit={
            "Recept sa datim tekstom je": [
                {
                    "id": 5,
                    "ingredients": "meso,supa,sargarepa,grasak,boranija,luk,sos",
                    "name": "corba",
                    "recipe_text": "Corba se kuva 30min. Potrebno je dobro promesati sastojke."
                }
            ]
        }

    def test_search_by_text(self,client):
        resp = client.get('/search_by_text', json=self.body, headers=self.headers)
        self.assertEqual(resp.status_code, 200)
        self.assertDictEqual(resp.get_json(), self.exit)
