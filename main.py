import hashlib
import json
import os
import random
import threading
import time
import uuid
from network import Network
from node import Node
from wallet import Wallet


node_num = 5
wallet_num = 10
opt_verbose = True


def dispatch_node(node_id, network):
    node = Node(node_id, network)
    node.run()


def generate_transactions(wallet_list):
    while True:
        for _ in range(random.randint(1, 2)):
            sender, receiver = random.sample(wallet_list, 2)
            value = random.randint(1, 100)
            sender.send(receiver.addr, value)
        time.sleep(random.random())


def show_network(network, opt_verbose):
    while True:
        out = ""
        max_len = 0
        longest_chain_list = []

        for node_id, chain_list in list(network.node_chain_dict.items()):
            if len(chain_list) > max_len:
                longest_chain_list = chain_list
                max_len = len(chain_list)

            chain = "-".join(
                [
                    "[" + hashlib.sha256(
                        json.dumps(chain, sort_keys=True).encode()
                    ).hexdigest()[:5] + "]"
                    for chain in chain_list
                ]
            )

            out += f"{node_id[:4]}:\t{chain}\n"

        if out != "":
            if opt_verbose:
                os.system("clear")
                print(f"Node\tChains\n\n{out}")

            with open("chain.json", "w", encoding="utf-8") as f:
                f.write("[" + ",\n".join(longest_chain_list) + "]")

            time.sleep(1)


def main():
    # init
    network = Network()
    node_id_list = [str(uuid.uuid4()) for _ in range(node_num)]
    wallet_list = [
        Wallet(
            network,
            random.sample(node_id_list, random.randint(1, node_num)),
        )
        for _ in range(wallet_num)
    ]

    # node
    for node_id in node_id_list:
        threading.Thread(
            target=dispatch_node,
            args=(node_id, network, )
        ).start()

    # show_network
    threading.Thread(
        target=show_network,
        args=(network, opt_verbose, )
    ).start()

    # generate transaction
    threading.Thread(
        target=generate_transactions,
        args=(wallet_list, )
    ).start()


if __name__ == "__main__":
    main()
