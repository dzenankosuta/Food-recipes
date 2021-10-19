import flask_unittest
from app import create_app
from flask import request,json
import requests


class TestDelete(flask_unittest.ClientTestCase):

    app=create_app()

    def setUp(self,client):
        response = requests.get('http://127.0.0.1:5000/login', auth=('dzenankosuta', 'afc14'))
        self.token=json.loads(response.text)['token']
        self.headers = {'x-access-token': self.token}

        self.exit={
            "Izbrisani recept je": {
                "id": 3,
                "ingredients": "corba,krompir",
                "name": "krompir corba",
                "recipe_text": "Krompir corba se kuva 3h."
            }
        }

    def test_delete(self,client):
        resp = client.delete('/delete/3', headers=self.headers)
        self.assertEqual(resp.status_code, 200)
        self.assertDictEqual(resp.get_json(), self.exit)
