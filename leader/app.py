from flask import Flask, request
from logging.config import dictConfig
import threading

import os
import leader

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

@app.route('/leader', methods=["POST"])
def leader_handler():
    new_leader = request.json['new_leader']
    leader.set_leader(new_leader, app.logger)
    return ('', 204)

@app.route('/leader/ping', methods=["GET"])
def leader_ping_handler():
    return ('UP', 200)

@app.route('/leader/election', methods=["POST"])
def leader_election_handler():
    port = os.environ['PORT']
    other_nodes = os.environ['OTHER_NODES'].split(',')
    upper_nodes = [node for node in other_nodes if int(node.split(":")[1]) > int(port)]
    lower_nodes = [node for node in other_nodes if int(node.split(":")[1]) < int(port)]
    
    leader.election(upper_nodes, lower_nodes, port, app.logger)
    return ('', 204)

if __name__ == '__main__':
    port = os.environ['PORT']
    other_nodes = os.environ['OTHER_NODES'].split(',')
    
    leader_thread = threading.Thread(target=leader.run_loop, args=[other_nodes, port, app.logger])
    leader_thread.start()
    
    app.run(host='0.0.0.0', port=port)