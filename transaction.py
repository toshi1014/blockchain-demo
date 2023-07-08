import json
import Crypto.Hash.SHA256
import Crypto.PublicKey.RSA
import Crypto.Signature.pkcs1_15


class Transaction:
    sender_addr: str
    receiver_addr: str
    value: float
    sign: str = None

    def __init__(self, sender_addr, receiver_addr, value):
        self.sender_addr = sender_addr.decode()
        self.receiver_addr = receiver_addr.decode()
        self.value = value

    @property
    def repr(self):
        prop = {
            "sender_addr": self.sender_addr,
            "receiver_addr": self.receiver_addr,
            "value": self.value,
        }
        return json.dumps(prop, sort_keys=True)

    @staticmethod
    def verify_transaction(transaction):
        if transaction.sign is None:
            return False

        hashed_transaction = Crypto.Hash.SHA256.new(transaction.repr.encode())
        verifier = Crypto.Signature.pkcs1_15.new(
            Crypto.PublicKey.RSA.importKey(transaction.sender_addr.encode())
        )
        try:
            verifier.verify(
                hashed_transaction,
                bytes.fromhex(transaction.sign),
            )
            return True
        except ValueError:
            return False
