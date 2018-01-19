import os
from concurrent.futures import ThreadPoolExecutor
from itertools import repeat
import logging

from flask import (
    Flask,
    request,
    redirect,
    Response,
    flash,
)


from utils import (
    filter_input_data,
    get_service_result,
    prepare_csv_output,
)


logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

app = Flask(__name__)
SERVICE_URL = os.environ.get('SERVICE_URL', 'sum')
SERVICES_NUMBER = int(os.environ.get('SERVICES_NUMBER', 3))


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file:
            data = file.read().decode('utf8')
            numbers = filter_input_data(data)
            sum_url = '{}{}'.format(request.host_url, SERVICE_URL)
            logger.info('Goes to url %s', sum_url)
            with ThreadPoolExecutor(SERVICES_NUMBER) as pool:
                results = pool.map(get_service_result, repeat(sum_url), numbers)
            data = prepare_csv_output(results)
            return Response(data, mimetype='text/plain')
    return """
    <!doctype html>
    <title>Upload csv File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    """


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
