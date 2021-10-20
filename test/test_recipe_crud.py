import flask_unittest
from app import create_app
from flask import request,json
import requests


class TestRecipeCRUD(flask_unittest.ClientTestCase):

    app=create_app()

    def setUp(self,client):
        resp = client.post('/login', json={"username":"dzenankosuta","password":"afc14"})
        token= resp.get_json()[0]["token"]
        client.environ_base['HTTP_AUTHORIZATION'] = 'Bearer ' + token


        self.body1={
                   "name":"burek",
                   "ingredients":"brasno,meso,sir",
                   "recipe_text":"Pece se 20min."
                   }
        self.exit1={
                   "Uneti recept je": {
                       "id": 1,
                       "ingredients": "brasno,meso,sir",
                       "name": "burek",
                       "recipe_text": "Pece se 20min."
                       }
                   }

        self.exit2={
            "Izbrisani recept je": {
                "id": 1,
                "ingredients": "brasno,meso,sir",
                "name": "burek",
                "recipe_text": "Pece se 20min."
            }
        }


    def test_1add(self,client):

        resp = client.post('/add', json=self.body1)
        self.assertEqual(resp.status_code, 200)
        self.assertDictEqual(resp.get_json(), self.exit1)


    def test_2all(self,client):

        resp = client.get('/all')
        self.assertEqual(resp.status_code, 200)


    def test_3my(self,client):
        resp = client.get('/my')
        self.assertEqual(resp.status_code, 200)


    def test_4prosek(self,client):
        resp = client.get('/prosek')
        self.assertEqual(resp.status_code, 200)


    def test_5najcesci(self,client):
        resp = client.get('/najcesci')
        self.assertEqual(resp.status_code, 200)


    def test_6delete(self,client):
        resp = client.delete('/delete/1')
        self.assertEqual(resp.status_code, 200)
        self.assertDictEqual(resp.get_json(), self.exit2)
