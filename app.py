from flask import Flask, request
from logging.config import dictConfig
import threading

import os
import lamport

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

@app.route('/')
def hello_world():
    return 'Hello, Docker!'

@app.route('/lamport', methods=["POST"])
def lamport_handler():
    received_timestamp = int(request.json['timestamp'])
    lamport.receive_message(received_timestamp, app.logger)
    
    return ('', 204)

if __name__ == '__main__':
    lamport_thread = threading.Thread(target=lamport.run_loop, args=[[5000], app.logger])
    lamport_thread.start()
    app.run(host='0.0.0.0', port=os.environ['PORT'])