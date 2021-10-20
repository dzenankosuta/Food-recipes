import flask_unittest
from app import create_app

class TestClearbit(flask_unittest.ClientTestCase):

    app = create_app()

    def setUp(self, client):

        resp = client.post('/login', json={"username":"dzenankosuta","password":"afc14"})
        token= resp.get_json()[0]["token"]
        client.environ_base['HTTP_AUTHORIZATION'] = 'Bearer ' + token



    def test_cbit(self, client):

        resp = client.get('/cbit')
        self.assertEqual(resp.status_code, 200)
