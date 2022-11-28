from flask import Flask, request
from logging.config import dictConfig
import threading

import os
import leader

# creates a list of hosts of the service excluding the own instance
def get_other_nodes(own_port):
    all_ports = os.environ['ALL_PORTS'].split(',')
    all_ports.remove(own_port)
    return [f"app-{port}:{port}" for port in all_ports]

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
def health_check_handler():
    return ('UP', 200)

@app.route('/leader', methods=["POST"])
def leader_handler():
    new_leader = request.json['new_leader']
    leader.set_leader(new_leader, app.logger)
    return ('', 204)

@app.route('/election', methods=["POST"])
def leader_election_handler():
    own_port = os.environ['PORT']
    other_nodes = get_other_nodes(own_port)
    
    (lower_nodes, upper_nodes) = leader.split_nodes(other_nodes, own_port)
    
    leader.election(upper_nodes, lower_nodes, own_port, app.logger)
    return ('', 204)

if __name__ == '__main__':
    own_port = os.environ['PORT']
    other_nodes = get_other_nodes(own_port)
    
    leader_thread = threading.Thread(target=leader.run_loop, args=[other_nodes, own_port, app.logger])
    leader_thread.start()
    
    app.run(host='0.0.0.0', port=own_port)