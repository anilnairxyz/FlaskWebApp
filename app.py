# -*- coding: utf-8 -*-
"""
A flask web service API that invokes loss_model for hurricane
loss estimation
"""
from flask import Flask, request, render_template, jsonify, make_response
import loss_model
import logging
from logging.handlers import TimedRotatingFileHandler

app = Flask(__name__)


def _extract_parameters(arguments):
    """
    Validate input parameters for GET requests and extract them
    :param arguments: GET request arguments
    :returns success: flag to indicate success of extraction
    :returns message: error message in case of failure
    :returns paramters: extracted parameters
    """
    permitted_type = ({'num_samples': int,
                       'macroevent_rate': float,
                       'macroevent_mean': float,
                       'macroevent_stddev': float,
                       'selfevent_rate': float,
                       'selfevent_mean': float,
                       'selfevent_stddev': float})
    parameters = {}
    for p in permitted_type:
        if p not in arguments:
            success = False
            message = 'Parameter {x} not defined'.format(x=p)
            break
        else:
            parameters[p] = request.args.get(p, type=permitted_type[p])
            if not parameters[p]:
                success = False
                message = ('Parameter {x} not of type {t}'
                           .format(x=p, t=permitted_type[p].__name__))
                break
    else:
        success = True
        message = 'OK'
    return success, message, parameters


@app.route('/', methods=['GET'])
def index():
    """
    A sample HTML web form for entering parameters
    """
    return render_template('index.html')


@app.route('/getloss', methods=['GET'])
def get_loss():
    """
    The web service end point returning JSON responses
    responses:
        400:
            One or more parameters not defined
            Incorrect type of parameters
            Runtime exceptions
        200:
            Correct loss value computed
            Overflow
    """
    success, message, parameters = _extract_parameters(request.args)
    if not success:
        response = {'result': None, 'status': 'Error', 'message': message}
        app.logger.error(response['message'])
        return make_response(jsonify(response), 400)
    try:
        result = loss_model.estimate_annual_loss(**parameters)
        response = {'result': result, 'status': 'OK', 'message': 'OK'}
    except OverflowError:
        response = ({'result': 'Infinity',
                     'status': 'Error', 'message': 'Overflow'})
        app.logger.warning(response['message'])
    except Exception:
        response = {'result': None, 'status': 'Error', 'message': 'Exception'}
        app.logger.error(response['message'])
        return make_response(jsonify(response), 400)
    return make_response(jsonify(response), 200)


@app.errorhandler(404)
def url_not_found(error):
    """
    Custom JSON error handler for 404 response
    """
    response = {'status': 'Error', 'message': 'URL not found'}
    app.logger.error(response['message'])
    return make_response(jsonify(response), 404)


@app.errorhandler(405)
def method_not_allowed(error):
    """
    Custom JSON error handler for 405 response
    """
    response = {'status': 'Error', 'message': 'Method not allowed'}
    app.logger.error(response['message'])
    return make_response(jsonify(response), 405)


if __name__ == '__main__':
    logfile = 'log/api.log'
    handler = TimedRotatingFileHandler(logfile, when='midnight', interval=1)
    formatter = logging.Formatter(fmt='%(asctime)s %(levelname)s %(message)s',
                                  datefmt='%d-%m-%Y %H:%M:%S')
    handler.setFormatter(formatter)
    handler.setLevel(logging.DEBUG)
    app.logger.addHandler(handler)
    app.run(host='0.0.0.0', port=8000)
