import Crypto.Hash.SHA256
import Crypto.PublicKey.RSA
import Crypto.Signature.pkcs1_15
from transaction import Transaction


class Wallet:
    def __init__(self, network, node_id_list=[]):
        key = Crypto.PublicKey.RSA.generate(1024)
        self.private_key = key.export_key(format="PEM")
        self.addr = key.publickey().export_key(format="PEM")

        self.network = network
        self.node_id_list = node_id_list

    def sign_transaction(self, transaction):
        signer = Crypto.Signature.pkcs1_15.new(
            Crypto.PublicKey.RSA.importKey(self.private_key)
        )

        hashed_transaction = Crypto.Hash.SHA256.new(transaction.repr.encode())
        transaction.sign = signer.sign(hashed_transaction).hex()
        return transaction

    def send(self, receiver_addr, value):
        tx = Transaction(self.addr, receiver_addr, value)
        signed_tx = self.sign_transaction(tx)
        self.broadcast(signed_tx)

    def broadcast(self, transaction):
        for node_id in self.node_id_list:
            self.network.post_transaction(node_id, transaction)
