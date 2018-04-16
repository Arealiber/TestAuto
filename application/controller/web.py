from application import app


@app.route('/')
def index():
    return app.send_static_file('index.html')


@app.route('/parameter/<page_num>')
def parameter_page(page_num):
    return app.send_static_file('parameter.html')


@app.route('/parameter_detail/<parameter_id>')
def parameter_detail(parameter_id):
    return app.send_static_file('parameter_detail.html')


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
