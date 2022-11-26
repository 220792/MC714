from flask import Flask
from logging.config import dictConfig
import threading

import os
import mutex

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

@app.route('/token', methods=["POST"])
def mutex_handler():
    mutex_thread = threading.Thread(target=mutex.receive_token, args=[resource_addr, next_node, app.logger])
    mutex_thread.start()
    return ('', 204)

if __name__ == '__main__':
    resource_addr = os.environ['RESOURCE_ADDR']
    next_node = os.environ['NEXT_NODE']
    port = os.environ['PORT']

    counter_thread = threading.Thread(target=mutex.start_count_loop, args=[app.logger])
    counter_thread.start()

    start_thread = threading.Thread(target=mutex.start_passing_token, args=[port, next_node, app.logger])
    start_thread.start()

    app.run(host='0.0.0.0', port=port)