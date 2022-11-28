from threading import Lock
import requests
import random
import time

current_leader = ""
running_election = False
thread_lock = Lock()

############ Election Functions ############

# Checks node status
def ping(node, logger):
    url = f'http://{node}/'

    logger.info('Pinging node: %s', node)

    requests.get(url)      

# Iterates over nodes with lower ports updating who is the leader
def broadcast_leadership(lower_nodes, logger):
    body = {'new_leader': str(current_leader)}

    for node in lower_nodes:
        try:    
            logger.info('Annoucing leadership to node: %s', node)
            requests.post(f'http://{node}/leader', json = body)
        except:
            continue


# Iterates over nodes with higher ports
#   - If any request succeeds, election continues and this node waits for the results
#   - If no request succeed, this should be the leader
def election(upper_nodes, lower_nodes, port, logger):
    global current_leader
    global running_election

    with thread_lock:
        logger.info('Running election...')
        running_election = True

    for node in upper_nodes:
        try:
            logger.info('Requesting election to node: %s', node)
            requests.post(f'http://{node}/election')
            return # If any request is successfull, I am not the leader and my part is done
        except:
            continue

    # If no request is successfull, I am the leader
    with thread_lock:
        current_leader = port
        running_election = False
    
    broadcast_leadership(lower_nodes, logger)

############ Auxiliary Functions ############

def split_nodes(available_nodes, port):
    return ([node for node in available_nodes if int(node.split(":")[1]) < int(port)], \
            [node for node in available_nodes if int(node.split(":")[1]) > int(port)])

def set_leader(new_leader, logger):
    global current_leader
    global running_election
    
    logger.info('Assuming %s as new leader!', new_leader)

    with thread_lock:
        running_election = False
        current_leader = new_leader

# Randomly checks the health of a live node of higher port number 
# If dead node is the current_leader, an election should take place
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
            available_nodes.remove(node)
            (lower_nodes, upper_nodes) = split_nodes(available_nodes, port)

            if node == current_leader and not running_election:
                logger.info('Node %s died and was the leader, will start election.', node)
                election(upper_nodes, lower_nodes, port, logger)