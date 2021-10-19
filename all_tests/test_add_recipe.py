import flask_unittest
from app import create_app
from flask import request,json
import requests


class TestAddRecipe(flask_unittest.ClientTestCase):

    app=create_app()

    def setUp(self,client):
        response = requests.get('http://127.0.0.1:5000/login', auth=('dzenankosuta', 'afc14'))
        self.token=json.loads(response.text)['token']
        self.headers = {'x-access-token': self.token}




        self.body={
                   "name":"omlet",
                   "ingredients":"jaje,mleko,kobasica",
                   "recipe_text":"Sprema se 5min."
                   }
        self.exit={
                   "Uneti recept je": {
                       "id": 6,
                       "ingredients": "jaje,mleko,kobasica",
                       "name": "omlet",
                       "recipe_text": "Sprema se 5min."
                       }
                   }


    def test_add(self,client):

        resp = client.post('/add', json=self.body, headers=self.headers)
        self.assertEqual(resp.status_code, 200)
        self.assertDictEqual(resp.get_json(), self.exit)
