import Crypto.Hash.SHA256
import Crypto.PublicKey.RSA
import Crypto.Signature.pkcs1_15
from .transaction import Transaction


class Wallet:
    def __init__(self, network, node_id_list=[]):
        key = Crypto.PublicKey.RSA.generate(1024)
        self.private_key = key.export_key(format="PEM")
        self.addr = key.publickey().export_key(format="PEM")

        self.network = network
        self.node_id_list = node_id_list

        self.signer = Crypto.Signature.pkcs1_15.new(
            Crypto.PublicKey.RSA.importKey(self.private_key)
        )

    def sign_transaction(self, transaction):
        hashed_transaction = Crypto.Hash.SHA256.new(transaction.repr.encode())
        transaction.sign = self.signer.sign(hashed_transaction).hex()
        return transaction

    def send(self, receiver_addr, value):
        tx = Transaction(self.addr, receiver_addr, value)
        str_signed_tx = self.sign_transaction(tx).repr
        self.post_transaction(str_signed_tx)
        return str_signed_tx

    def post_transaction(self, str_transaction):
        self.network.post_transaction(str_transaction)
