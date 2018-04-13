from flask import render_template

from application import app
from application.api import interface as InterfaceAPI


@app.route('/')
def index():
    return app.send_static_file('index.html')


@app.route('/parameter')
def parameter_index():
    return app.send_static_file('parameter.html')


@app.route('/interface')
def interface_index():
    return app.send_static_file('interface.html')


@app.route('/use_case')
def use_case_index():
    return app.send_static_file('use_case.html')


@app.route('/batch')
def batch_index():
    return app.send_static_file('batch.html')


@app.route('/run_log')
def run_log_index():
    return app.send_static_file('run_log.html')
