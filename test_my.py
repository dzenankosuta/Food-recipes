import flask_unittest
from app import create_app
from flask import request,json
import requests


class TestMyRecipes(flask_unittest.ClientTestCase):

    app=create_app()

    def setUp(self,client):
        response = requests.get('http://127.0.0.1:5000/login', auth=('dzenankosuta', 'afc14'))
        self.token=json.loads(response.text)['token']
        self.headers = {'x-access-token': self.token}
        self.maxDiff=None

        self.exit={
            "Svi moji recepti su": [
                {
                    "ingredients": "slag,jagode",
                    "name": "torta",
                    "recipe_text": "Torta se sprema iz 5 koraka."
                },
                {
                    "ingredients": "vanila,cokolada,jagode",
                    "name": "sladoled",
                    "recipe_text": "Sladoled se sprema u posebnim masinama najnovije tehnologije."
                }
            ]
        }
        
    def test_my(self,client):
        resp = client.get('/my', headers=self.headers)
        self.assertEqual(resp.status_code, 200)
        self.assertDictEqual(resp.get_json(), self.exit)
