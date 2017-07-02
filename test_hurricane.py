import copy
from api_main import app
from flask import json


class TestFlaskAPI(object):
    def setUp(self):
        self.test_app = app.test_client()
        self.service_url = 'gethurricaneloss'
        self.default_args = ({'num_monte_carlo_samples': 500,
                              'florida_landfall_rate': 20,
                              'florida_mean': 2,
                              'florida_stddev': 1.5,
                              'gulf_landfall_rate': 28,
                              'gulf_mean': 1,
                              'gulf_stddev': 2})

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
        arguments['gulf_mean'] = 1000
        arguments['gulf_stddev'] = 29
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
