import json
import random
import time
import Crypto.Hash.SHA256
import Crypto.PublicKey.RSA
import Crypto.Signature.pkcs1_15
from block import Block


DIFFICULTY = 4


class Node:
    def __init__(self, network):
        self.network = network
        self.chain = [Block.get_genesis_block(DIFFICULTY).repr]
        self.status = ""
        self.interval = random.randint(1, 10)   # as computing power diff

        # sign
        key = Crypto.PublicKey.RSA.generate(1024)
        self.private_key = key.export_key(format="PEM")
        self.node_id = key.publickey().export_key(format="PEM").decode()
        self.signer = Crypto.Signature.pkcs1_15.new(
            Crypto.PublicKey.RSA.importKey(self.private_key)
        )

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
                Block.hash(json.dumps(block["transactions"], sort_keys=True)),
                block["block_header"]["nonce"],
            ):

                return False

            last_block = str_block

        return True

    def set_status(self, status):
        self.status = status
        time.sleep(0.5)             # for view

    def proof_of_work(self, previous_block_hash, new_transaction_list):
        new_transaction_list_hash = Block.hash(new_transaction_list)

        nonce = 0

        while True:
            if nonce % 100 == 0:
                if self.resolve_conflict():
                    self.set_status("resolved")
                    return

            if Node.is_valid_proof(
                previous_block_hash,
                new_transaction_list_hash,
                nonce,
            ):
                return nonce
            nonce += 1

    def mine(self):
        time.sleep(self.interval)

        previous_block = self.chain[-1]
        str_new_transaction_list = self.network.get_transactions(self.node_id)

        if len(str_new_transaction_list) == 0:
            return False

        previous_block_hash = Block.hash(previous_block)
        merkle_root = Node.get_merkle_root(str_new_transaction_list)

        nonce = self.proof_of_work(
            previous_block_hash,
            "[" + ", ".join(str_new_transaction_list) + "]",
        )

        if nonce is None:   # already been mined
            return False

        new_block = Block(
            timestamp=time.time(),
            previous_block_hash=previous_block_hash,
            merkle_root=merkle_root,
            difficulty=DIFFICULTY,
            nonce=nonce,
            transaction_counter=len(str_new_transaction_list),
            transactions=[
                json.loads(str_new_tx)
                for str_new_tx in str_new_transaction_list
            ],
        )

        self.chain.append(new_block.repr)

        return True

    def resolve_conflict(self):
        longest_chain = self.chain
        bool_resolved = False

        for neighbor_chain in self.network.get_neighbor_chain_list(self.node_id):
            if Node.is_valid_chain(neighbor_chain):
                if len(neighbor_chain) > len(longest_chain):
                    bool_resolved = True
                    longest_chain = neighbor_chain

        self.chain = longest_chain
        return bool_resolved

    def post_updated_chain(self):
        str_chain = json.dumps(self.chain, sort_keys=True)
        hashed_chain = Crypto.Hash.SHA256.new(str_chain.encode())
        sign = self.signer.sign(hashed_chain).hex()

        self.network.update_chain(self.node_id, str_chain, sign)

    def run(self):
        while True:
            self.set_status("mining...")
            if self.mine():
                self.set_status("mined\t")

            self.post_updated_chain()
