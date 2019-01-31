import copy
from app import app
from flask import json


class TestFlaskAPI(object):
    def setUp(self):
        self.test_app = app.test_client()
        self.service_url = 'getloss'
        self.default_args = ({'num_samples': 500,
                              'macroevent_rate': 20,
                              'macroevent_mean': 2,
                              'macroevent_stddev': 1.5,
                              'selfevent_rate': 28,
                              'selfevent_mean': 1,
                              'selfevent_stddev': 2})

    def test_missing_parameters(self):
        for p in self.default_args:
            arguments = copy.deepcopy(self.default_args)
            arguments.pop(p)
            resp = self.test_app.get(self.service_url, query_string=arguments)
            assert json.loads(resp.data)['status'] == 'Error'
            assert 'not defined' in json.loads(resp.data)['message']
            assert resp.status_code == 400

    def test_incorrect_types(self):
        for p in self.default_args:
            arguments = copy.deepcopy(self.default_args)
            arguments[p] = 'aaa'
            resp = self.test_app.get(self.service_url, query_string=arguments)
            assert json.loads(resp.data)['status'] == 'Error'
            assert 'not of type' in json.loads(resp.data)['message']
            assert resp.status_code == 400

    def test_overflow(self):
        arguments = copy.deepcopy(self.default_args)
        arguments['selfevent_mean'] = 1000
        arguments['selfevent_stddev'] = 29
        resp = self.test_app.get(self.service_url, query_string=arguments)
        assert json.loads(resp.data)['status'] == 'Error'
        assert 'Overflow' in json.loads(resp.data)['message']
        assert resp.status_code == 200

    def test_loss_model(self):
        arguments = copy.deepcopy(self.default_args)
        resp = self.test_app.get(self.service_url, query_string=arguments)
        assert json.loads(resp.data)['status'] == 'OK'
        assert 100 <= json.loads(resp.data)['result'] <= 1000
        assert resp.status_code == 200
