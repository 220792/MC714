from threading import Lock
import requests
import random
import time

current_leader = ""
running_election = False
thread_lock = Lock()

def set_leader(new_leader, logger):
    global current_leader
    global running_election
    
    logger.info('Assuming %s as new leader!', new_leader)

    with thread_lock:
        running_election = False
        current_leader = new_leader

def ping(node, logger):
    url = f'http://{node}/leader/ping'

    logger.info('Pinging node: %s', node)

    requests.get(url)      

def broadcast_leadership(lower_nodes, logger):
    for node in lower_nodes:
        url = f'http://{node}/leader'
        body = {'new_leader': str(current_leader)}

        logger.info('Annoucing leadership to node: %s', node)

        try:    
            requests.post(url, json = body)
        except:
            logger.warn('Could not broadcast_leadership to node %s', node)
    
def election(upper_nodes, lower_nodes, port, logger):
    global current_leader
    global running_election

    with thread_lock:
        running_election = True
    
        logger.info('Running election...')

    for node in upper_nodes:
        url = f'http://{node}/leader/election'

        logger.info('Requesting election to node: %s', node)

        try:
            requests.post(url)
            return # If any request is successfull, I am not the leader
        except:
            continue

    # If no request is successfull, I am the leader
    with thread_lock:
        current_leader = port
    
    broadcast_leadership(lower_nodes, logger)

def split_nodes(available_nodes, port):
    return ([node for node in available_nodes if int(node.split(":")[1]) < int(port)], \
            [node for node in available_nodes if int(node.split(":")[1]) > int(port)])

def run_loop(available_nodes, port, logger):
    global current_leader
    global running_election
    
    (lower_nodes, upper_nodes) = split_nodes(available_nodes, port)
    
    # Leaders should not worry about themselves (?)
    if len(upper_nodes) == 0:
        return
        
    set_leader(upper_nodes[-1], logger)

    while(len(upper_nodes) > 0):
        time.sleep(5)
        node = random.choice(upper_nodes)
        
        try:
            ping(node, logger)
        except:
            logger.warn('Node %s did not answer, will be considered dead.', node)

            available_nodes.remove(node)
            (lower_nodes, upper_nodes) = split_nodes(available_nodes, port)

            if node == current_leader and not running_election:
                logger.info('Dead node was the leader, will start election.')
                election(upper_nodes, lower_nodes, port, logger)