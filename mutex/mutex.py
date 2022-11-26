from threading import Lock
import requests
import random
import time

local_counter = 0
resource_needed = False
thread_lock = Lock()

def set_resource_needed(logger):
    global resource_needed
    if local_counter > 2:
        logger.info('Resource needed, counter: %s', local_counter)
        resource_needed = True

def reset_values(logger):
    global resource_needed
    global local_counter
    with thread_lock:
        resource_needed = resource_needed
        local_counter = local_counter
        logger.info('Values Reseted')

def use_resource(resource_addr, logger):
    url = f'http://{resource_addr}/save'
    body = {'value': str(local_counter)}

    logger.info('Using resource')
    requests.post(url, json = body)

def pass_token(next_node, logger):
    time.sleep(1)
    url = f'http://app-{next_node}:{next_node}/token'

    logger.info('Passing token')
    requests.post(url, json = {})

def receive_token(resource_addr, next_node, logger):
    logger.info('Token received')
    global local_counter
    if resource_needed:
        use_resource(resource_addr, logger)
        reset_values(logger)
    
    pass_token(next_node, logger)

def start_passing_token(current_node, next_node, logger):
    if int(next_node) < int(current_node):
        logger.info('Starting to pass token')
        pass_token(next_node, logger)

def count(logger):
    global local_counter
    should_count = bool(random.getrandbits(1)) and not resource_needed
    if should_count:
        with thread_lock:
            local_counter += 1
        logger.info('Local counter: %s', local_counter)
        set_resource_needed(logger)

def start_count_loop(logger):
    while True:
        time.sleep(1)
        count(logger)