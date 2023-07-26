import json
import os
import time
from node import Node


filename_chain = "chain.json"
filename_transaction_record = "transaction_record.json"


class Sentinel:
    def __init__(self):
        self.transaction_record = []
        self.network = None
        self.longest_chain = []

        if os.path.exists(filename_transaction_record):
            os.remove(filename_transaction_record)

        self.file_transaction_record = open(
            filename_transaction_record, "a", encoding="utf8")

    def kill(self):
        os._exit(0)

    def register_network(self, network):
        self.network = network

    def post_transaction(self, transaction):
        self.transaction_record.append(transaction)
        self.file_transaction_record.write(transaction + ",")

    def get_longest_chain(self):
        longest_chain = []

        for neighbor_chain in self.network.get_neighbor_chain_list(None):
            if len(neighbor_chain) > len(longest_chain):
                longest_chain = neighbor_chain

        return longest_chain

    def is_all_transactions_included(self):
        transaction_in_chain = [
            json.dumps(tx, sort_keys=True)
            for transactions in
            [
                json.loads(str_block)["transactions"]
                for str_block in self.longest_chain
            ]
            for tx in transactions
        ]

        if len(transaction_in_chain) == len(self.transaction_record):
            return False

        flg_invalid = sum([
            int(tx_in_chain != tx_record)
            for tx_in_chain, tx_record in zip(
                transaction_in_chain, self.transaction_record
            )
        ])

        return flg_invalid == 0

    def is_valid_chain(self):
        return Node.is_valid_chain(self.longest_chain)

    def historian(self):
        with open(filename_chain, "w", encoding="utf-8") as f:
            f.write("[" + ",\n".join(self.longest_chain) + "]")

    def run(self):
        checklist = [
            # self.is_all_transactions_included,
            self.is_valid_chain,
        ]

        while True:
            self.longest_chain = self.get_longest_chain()
            self.historian()

            if len(self.longest_chain) > 1:      # ignore genesis block
                for func in checklist:
                    if not func():
                        self.kill(func)
            time.sleep(1)
