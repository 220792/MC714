import requests
import random
import time

local_timestamp = 0

def receive_message(received_timestamp, logger):
    global local_timestamp 
    logger.info('Received timestamp: %s', received_timestamp)
    # TODO: thread lock
    local_timestamp = max(local_timestamp, received_timestamp) + 1
    logger.info('New timestamp: %s', local_timestamp)

def send_message(port, logger):
    url = f'http://0.0.0.0:{port}/lamport'
    body = {'timestamp': str(local_timestamp)}

    logger.info('Sending request to port: %s', port)
    requests.post(url, json = body)

def run_loop(available_ports, logger):
    while(True):
        time.sleep(10)
        port = random.choice(available_ports)
        send_message(port, logger)