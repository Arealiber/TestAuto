from application import app


@app.route('/')
def index():
    return app.send_static_file('index.html')


@app.route('/parameter/<page_num>')
def parameter_page(page_num):
    return app.send_static_file('parameter.html')


@app.route('/parameter_detail/<parameter_id>')
def parameter_detail_page(parameter_id):
    return app.send_static_file('parameter_detail.html')


@app.route('/interface/<page_num>')
def interface_page(page_num):
    return app.send_static_file('interface.html')


@app.route('/interface_detail/<interface_id>')
def interface_detail_page(interface_id):
    return app.send_static_file('interface_detail.html')


@app.route('/use_case/<page_num>')
def use_case_page(page_num):
    return app.send_static_file('use_case.html')


@app.route('/use_case_detail/<use_case_id>')
def use_case_detail_page(use_case_id):
    return app.send_static_file('use_case_detail.html')


@app.route('/batch/<page_num>')
def batch_page(page_num):
    return app.send_static_file('batch.html')


@app.route('/batch_detail/<batch_id>')
def batch_detail_page(batch_id):
    return app.send_static_file('batch_detail.html')


@app.route('/use_case_run_log/<page_num>')
def use_case_run_log_page(page_num):
    return app.send_static_file('use_case_run_log.html')


@app.route('/batch_run_log/<page_num>')
def batch_run_log_page(page_num):
    return app.send_static_file('batch_run_log.html')


@app.route('/use_case_run_log/detail/<run_log_id>')
def use_case_run_log_detail(run_log_id):
    return app.send_static_file('use_case_run_log_detail.html')