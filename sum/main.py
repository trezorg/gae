"""Sum service."""

import json
import time
import logging

from flask import (
    Flask,
    request,
    Response,
)

from utils import prepare_row

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

app = Flask(__name__)


@app.route('/sum', methods=['POST'])
def sums():
    """Calculate prime sums."""
    start_time = time.perf_counter()
    data = json.loads(request.data)
    logger.info('Got data: %s', data)
    number = data['number']
    row = prepare_row(number)
    time_diff = round((time.perf_counter() - start_time) * 1000, 3)
    result_data = row + (time_diff,)
    logger.info('Result data: %s', result_data)
    return Response(
        json.dumps({'result': result_data}), mimetype='application/json')


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8081, debug=True)
