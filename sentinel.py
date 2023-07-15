import json
import time


class Sentinel:
    def __init__(self):
        self.transaction_record = []
        self.network = None

    def get_longest_chain(self):
        longest_chain = []

        for neighbor_chain in self.network.get_neighbor_chain_list(None):
            if len(neighbor_chain) > len(longest_chain):
                longest_chain = neighbor_chain

        return longest_chain

    def is_all_transactions_included(self):
        chain = self.get_longest_chain()

        if len(chain) <= 1:      # ignore genesis block
            return True

        transaction_chain = [
            tx for transactions in
            [
                json.loads(str_block)["transactions"]
                for str_block in chain
            ]
            for tx in transactions
        ]

        flg_invalid = sum([
            int(tx_record not in transaction_chain)
            for tx_record in self.transaction_record
        ])

        return flg_invalid != 0

    def register_network(self, network):
        self.network = network

    def post_transaction(self, transaction):
        self.transaction_record.append(transaction)

    def run(self):
        while True:
            if not self.is_all_transactions_included():
                raise RuntimeError("Broken transactions")
            time.sleep(1)
