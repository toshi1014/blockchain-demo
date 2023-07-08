import hashlib
import json
import time


class Block:
    def __init__(
        self,
        timestamp,
        previous_block_hash,
        merkle_root,
        difficulty,
        nonce,
        transaction_counter,
        transactions,
    ):
        block_size = None

        block_header = {
            "version": "1.0",
            "timestamp": timestamp,
            "previous_block_hash": previous_block_hash,
            "merkle_root": merkle_root,
            "difficulty": difficulty,
            "nonce": nonce,
        }

        self.block = {
            "block_size": block_size,
            "block_header": block_header,
            "transaction_counter": transaction_counter,
            "transactions": transactions,
        }

    @property
    def repr(self):
        return json.dumps(self.block, sort_keys=True)

    @classmethod
    def hash(cls, obj):
        string = json.dumps(obj, sort_keys=True)
        return hashlib.sha256(string.encode()).hexdigest()

    @classmethod
    def get_genesis_block(cls, initial_difficulty):
        genesis_block = cls(
            timestamp=time.time(),
            previous_block_hash="",
            merkle_root="",
            difficulty=initial_difficulty,
            nonce=0,
            transaction_counter=0,
            transactions=[],
        )

        return genesis_block
