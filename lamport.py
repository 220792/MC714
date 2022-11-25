from threading import Lock
import requests
import random
import time

local_timestamp = 0
thread_lock = Lock()

def receive_message(received_timestamp, logger):
    global local_timestamp 
    logger.info('Received timestamp: %s', received_timestamp)
    
    with thread_lock:
        local_timestamp = max(local_timestamp, received_timestamp) + 1
    
    logger.info('New timestamp: %s', local_timestamp)

def send_message(node, logger):
    url = f'http://{node}/lamport'
    body = {'timestamp': str(local_timestamp)}

    logger.info('Sending request to node: %s', node)
    requests.post(url, json = body)

def run_loop(available_nodes, logger):
    while(True):
        time.sleep(10)
        node = random.choice(available_nodes)
        send_message(node, logger)