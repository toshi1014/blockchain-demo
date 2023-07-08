import json
import random
import time
from block import Block


DIFFICULTY = 2


class Node:
    def __init__(self, node_id, network):
        self.node_id = node_id
        self.network = network
        self.chain = [Block.get_genesis_block(DIFFICULTY).repr]
        self.node_list = set()

    @classmethod
    def proof_hash(
        cls,
        previous_block_hash,
        new_transaction_list_hash,
        str_nonce,
    ):
        return previous_block_hash + new_transaction_list_hash + str_nonce

    @classmethod
    def is_valid_proof(
        cls,
        previous_block_hash,
        new_transaction_list_hash,
        nonce,
    ):
        hashed = Block.hash(
            Node.proof_hash(
                previous_block_hash,
                new_transaction_list_hash,
                str(nonce),
            )
        )
        return hashed[:DIFFICULTY] == "0" * DIFFICULTY

    @classmethod
    def get_merkle_root(cls, transaction_hash_list):
        if len(transaction_hash_list) == 0:
            return Block.hash({})
        if len(transaction_hash_list) == 1:
            return Block.hash(transaction_hash_list[0])
        if len(transaction_hash_list) % 2 == 1:
            transaction_hash_list.append(transaction_hash_list[-1])

        hash_list = []

        for i in range(0, len(transaction_hash_list), 2):
            pair = [transaction_hash_list[i]] + [transaction_hash_list[i+1]]
            hash_val = Block.hash(pair)
            hash_list.append(hash_val)

        return Node.get_merkle_root(hash_list)

    @staticmethod
    def is_valid_chain(chain):
        last_block = chain[0]
        for str_block in chain[1:]:
            block = json.loads(str_block)
            if block["block_header"]["previous_block_hash"] != \
                    Block.hash(last_block):
                return False

            if not Node.is_valid_proof(
                block["block_header"]["previous_block_hash"],
                Block.hash(block["transactions"]),
                block["block_header"]["nonce"],
            ):
                return False

            last_block = block

        return True

    def is_minded(self):
        return self.update_block() or self.resolve_conflict()

    def update_block(self):
        for block in self.network.get_updated_block(self.node_id):
            self.chain.append(block)
            if not Node.is_valid_chain(self.chain):
                self.chain.pop(-1)
                return True

        return False

    def proof_of_work(self, previous_block_hash, new_transaction_list):
        new_transaction_list_hash = Block.hash(new_transaction_list)

        nonce = 0

        while True:
            if nonce % 100 == 0:
                if self.is_minded():
                    return

            if Node.is_valid_proof(
                previous_block_hash,
                new_transaction_list_hash,
                nonce,
            ):
                return nonce
            nonce += 1

    def mine(self):
        previous_block = self.chain[-1]
        new_transaction_list = self.network.get_transactions(self.node_id)

        if len(new_transaction_list) == 0:
            return False

        previous_block_hash = Block.hash(previous_block)
        str_new_transaction_list = list(
            map(lambda tx: tx.repr, new_transaction_list)
        )
        merkle_root = Node.get_merkle_root(str_new_transaction_list)

        str_transactions = "[" + ",".join(str_new_transaction_list) + "]"
        nonce = self.proof_of_work(previous_block_hash, str_transactions)

        if nonce is None:   # already been mined
            return True

        new_block = Block(
            timestamp=time.time(),
            previous_block_hash=previous_block_hash,
            merkle_root=merkle_root,
            difficulty=DIFFICULTY,
            nonce=nonce,
            transaction_counter=len(new_transaction_list),
            transactions=str_transactions,
        )

        self.chain.append(new_block.repr)

        self.network.broadcast_new_block(self.node_id, new_block.repr)

        return True

    def resolve_conflict(self):
        longest_chain = self.chain
        bool_resolved = False

        for neighbor_chain in self.network.get_neighbor_chain_list(self.node_id):
            if Node.is_valid_chain(neighbor_chain):
                if len(neighbor_chain) > len(longest_chain):
                    longest_chain = neighbor_chain
                    bool_resolved = True

        self.chain = longest_chain
        return bool_resolved

    def run(self):
        while True:
            if self.mine():
                ...
                # print(self.node_id[:4], "mined")

            if self.update_block():
                ...
                # print(self.node_id[:4], "updated")

            if self.resolve_conflict():
                ...
                # print(self.node_id, "resolved")

            self.network.update_chain(self.node_id, self.chain)

            time.sleep(random.random() * 5)
