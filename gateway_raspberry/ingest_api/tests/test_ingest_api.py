import os
from ingest_api import ingest_api
import json
import unittest
import tempfile

class IngestApiTestCase(unittest.TestCase):

    def setUp(self):
        self.db_fd, ingest_api.app.config['DATABASE'] = tempfile.mkstemp()
        ingest_api.app.testing = True
        self.app = ingest_api.app.test_client()
        with ingest_api.app.app_context():
            ingest_api.init_db()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(ingest_api.app.config['DATABASE'])

    def test_sauna(self):
        response = self.app.post('/sauna', data=json.dumps({
            "temperature": 60,
            "humidity": 40,
            "mac_address": "00:00:00:00:00:00"
        }), content_type='application/json')
        assert response.status_code == 204

    def test_json_check_fails(self):
        response = self.app.post('/sauna', data="junk",
        content_type='application/json')
        assert response.status_code == 400

    def test_schema_fails(self):
        response = self.app.post('/sauna', data=json.dumps({
            "temperature": 60,
            "mac_address": "00:00:00:00:00:00"
        }), content_type='application/json')
        assert response.status_code == 400