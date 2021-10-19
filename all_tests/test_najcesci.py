import flask_unittest
from app import create_app
from flask import request,json
import requests


class TestNajcesci(flask_unittest.ClientTestCase):

    app=create_app()

    def setUp(self,client):
        response = requests.get('http://127.0.0.1:5000/login', auth=('dzenankosuta', 'afc14'))
        self.token=json.loads(response.text)['token']
        self.headers = {'x-access-token': self.token}
        self.maxDiff=None

        self.exit={
            "Najčešće korišćeni sastojci su": [
                [
                    "Naziv sastojka: meso",
                    "Upotrebljen 3 put"
                ],
                [
                    "Naziv sastojka: jagode",
                    "Upotrebljen 2 put"
                ],
                [
                    "Naziv sastojka: kecap",
                    "Upotrebljen 2 put"
                ],
                [
                    "Naziv sastojka: boranija",
                    "Upotrebljen 1 put"
                ],
                [
                    "Naziv sastojka: cokolada",
                    "Upotrebljen 1 put"
                ]
            ]
        }

    def test_najcesci(self,client):
        resp = client.get('/najcesci', headers=self.headers)
        self.assertEqual(resp.status_code, 200)
        self.assertDictEqual(resp.get_json(), self.exit)
