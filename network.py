from collections import defaultdict
import copy
import json
import threading
import Crypto.Hash.SHA256
import Crypto.PublicKey.RSA
import Crypto.Signature.pkcs1_15


class Network:
    def __init__(self, sentinel):
        self.sentinel = sentinel
        self.node_chain_dict = defaultdict(lambda: [])
        self.transaction_pool = defaultdict(lambda: [])
        self.lock = threading.Lock()        # mutex

    @staticmethod
    def verify_chain(node_id, str_chain, sign):
        hashed_chain = Crypto.Hash.SHA256.new(str_chain.encode())
        verifier = Crypto.Signature.pkcs1_15.new(
            Crypto.PublicKey.RSA.import_key(node_id.encode())
        )
        try:
            verifier.verify(hashed_chain, bytes.fromhex(sign))
            return True
        except ValueError:
            return False

    # chain
    def update_chain(self, node_id, str_chain, sign):
        if Network.verify_chain(node_id, str_chain, sign):
            self.node_chain_dict[node_id] = json.loads(str_chain)

    def get_chain(self, node_id):
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
        self.sentinel.post_transaction(transaction)
        self.transaction_pool[node_id].append(transaction)

    def get_transactions(self, node_id):
        transactions = copy.deepcopy(self.transaction_pool[node_id])
        self.transaction_pool[node_id][:] = []
        return transactions
    # end transaction
