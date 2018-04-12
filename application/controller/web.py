from flask import render_template

from application import app


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/parameter')
def parameter():
    return render_template('parameter.html')


@app.route('/interface')
def interface():
    return render_template('interface.html')


@app.route('/use_case')
def use_case():
    return render_template('use_case.html')


@app.route('/batch')
def batch():
    return render_template('batch.html')


@app.route('/run_log')
def run_log():
    return render_template('run_log.html')