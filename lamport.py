import requests

local_timestamp = 0

def receive_message(received_timestamp, logger):
    global local_timestamp 
    logger.info('Received timestamp: %s', received_timestamp)
    # TODO: thread lock
    local_timestamp = max(local_timestamp, received_timestamp) + 1
    logger.info('New timestamp: %s', local_timestamp)

def sending_message(port):
    url = f'http://0.0.0.0:{port}/lamport'
    body = {'timestamp': str(local_timestamp)}

    requests.post(url, json = body)