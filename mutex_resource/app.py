from flask import Flask, request
from logging.config import dictConfig
from threading import Lock
import time
from random import randrange

import os

dictConfig(
    {
        "version": 1,
        "formatters": {
            "default": {
                "format": "[%(asctime)s] %(levelname)s in %(module)s: %(message)s",
            }
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stdout",
                "formatter": "default",
            }
        },
        "root": {"level": "INFO", "handlers": ["console"]},
    }
)

app = Flask(__name__)
thread_lock = Lock()
global_counter = 0

@app.route('/save', methods=["POST"])
def resource_handler():
    global global_counter
    received_value = int(request.json['value'])
    with thread_lock:
        global_counter += received_value

    app.logger.info('Global counter: %s', global_counter)
    time.sleep(randrange(5))
    return ('', 204)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=os.environ['PORT'])