from copy import deepcopy


class Network:
    def __init__(self):
        self.node_chain_dict = dict()
        self.node_new_block_dict = dict()
        self.transaction_pool = dict()

    # chain
    def update_chain(self, node_id, chain):
        self.node_chain_dict[node_id] = chain

    def get_chain(self, node_id):
        if node_id not in self.node_chain_dict:
            return []
        return self.node_chain_dict[node_id]

    def get_neighbor_chain_list(self, self_node_id):
        return [
            self.get_chain(node_id)
            for node_id in self.node_chain_dict if self_node_id != node_id
        ]
    # end chain

    # block
    def update_new_block(self, block, node_id):
        if node_id not in self.node_new_block_dict:
            self.node_new_block_dict[node_id] = [block]
        else:
            self.node_new_block_dict[node_id].append(block)

    # TODO: add sign
    def broadcast_new_block(self, node_id, block):
        for neighbor in self.node_chain_dict:
            if neighbor != node_id:
                self.update_new_block(block, neighbor)

    def get_updated_block(self, node_id):
        if node_id not in self.node_new_block_dict:
            return []
        else:
            updated = [b for b in self.node_new_block_dict[node_id]]
            self.node_new_block_dict[node_id][:] = []
            return updated
    # end block

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
            transactions = deepcopy(self.transaction_pool[node_id])
            self.transaction_pool[node_id][:] = []
            return transactions
    # end transaction
