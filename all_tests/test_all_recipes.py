import flask_unittest
from app import create_app
from flask import request,json
import requests


class TestAllRecipes(flask_unittest.ClientTestCase):

    app=create_app()

    def setUp(self,client):
        response = requests.get('http://127.0.0.1:5000/login', auth=('dzenankosuta', 'afc14'))
        self.token=json.loads(response.text)['token']
        self.headers = {'x-access-token': self.token}
        self.maxDiff=None

        self.exit={
            "Svi recepti su": [
                {
                    "id": 1,
                    "ingredients": "slag,jagode",
                    "name": "torta",
                    "recipe_text": "Torta se sprema iz 5 koraka."
                },
                {
                    "id": 2,
                    "ingredients": "vanila,cokolada,jagode",
                    "name": "sladoled",
                    "recipe_text": "Sladoled se sprema u posebnim masinama najnovije tehnologije."
                },
                {
                    "id": 3,
                    "ingredients": "kecap,meso,pecurke,kackavalj",
                    "name": "pizza",
                    "recipe_text": "Pizza se pece u pecnici 6min."
                },
                {
                    "id": 4,
                    "ingredients": "kecap,majonez,meso",
                    "name": "piroska",
                    "recipe_text": "Proska se pece u pecnici 9min."
                },
                {
                    "id": 5,
                    "ingredients": "meso,supa,sargarepa,grasak,boranija,luk,sos",
                    "name": "corba",
                    "recipe_text": "Corba se kuva 30min. Potrebno je dobro promesati sastojke."
                }
            ]
        }

    def test_all(self,client):

        resp = client.get('/all', headers=self.headers)
        self.assertEqual(resp.status_code, 200)
        self.assertDictEqual(resp.get_json(), self.exit)
