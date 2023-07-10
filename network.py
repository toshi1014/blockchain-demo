import copy
import threading


class Network:
    def __init__(self):
        self.node_chain_dict = dict()
        self.transaction_pool = dict()
        self.lock = threading.Lock()        # mutex

    # chain
    # TODO: add sign
    def update_chain(self, node_id, chain):
        self.node_chain_dict[node_id] = chain

    def get_chain(self, node_id):
        if node_id not in self.node_chain_dict:
            return []
        return self.node_chain_dict[node_id]

    def get_neighbor_chain_list(self, self_node_id):
        self.lock.acquire()
        neighbor_chain_list = [
            copy.deepcopy(self.get_chain(node_id))
            for node_id in self.node_chain_dict if self_node_id != node_id
        ]
        self.lock.release()
        return neighbor_chain_list
    # end chain

    # transaction
    def post_transaction(self, node_id, transaction):
        if node_id not in self.transaction_pool:
            self.transaction_pool[node_id] = [transaction]
        else:
            self.transaction_pool[node_id].append(transaction)

    def get_transactions(self, node_id):
        if node_id not in self.transaction_pool:
            return []
        else:
            transactions = copy.deepcopy(self.transaction_pool[node_id])
            self.transaction_pool[node_id][:] = []
            return transactions
    # end transaction
