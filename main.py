import hashlib
import json
import os
import random
import threading
import time
import blockchain


def dispatch_node(node):
    node.run()


def dispatch_sentinel(sentinel):
    sentinel.run()


def generate_transactions(wallet_list):
    while True:
        for _ in range(random.randint(1, 2)):
            sender, receiver = random.sample(wallet_list, 2)
            value = random.randint(1, 100)
            sender.send(receiver.addr, value)

        time.sleep(random.random())


def show_network(network, node_dict):
    while True:
        out = ""

        for node_id, chain_list in list(network.node_chain_dict.items()):
            short_node_id = hashlib.sha256(node_id.encode()).hexdigest()[:4]
            status = node_dict[node_id].status
            chain = "-".join(
                [
                    "[" + hashlib.sha256(
                        json.dumps(chain, sort_keys=True).encode()
                    ).hexdigest()[:5] + "]"
                    for chain in chain_list
                ]
            )

            out += f"{short_node_id}:\t{status}\t{chain}\n"

        if out != "":
            os.system("clear")
            print(f"Node\tStatus\t\tChains\n\n{out}")

        time.sleep(0.1)


def main():
    # params
    node_num = 5
    wallet_num = 10
    bool_show_network = True
    # bool_show_network = False

    # init
    sentinel = blockchain.Sentinel()
    network = blockchain.Network(sentinel)
    sentinel.register_network(network)
    node_list = [blockchain.Node(network) for _ in range(node_num)]
    node_dict = {
        node.node_id: node for node in node_list
    }
    wallet_list = [
        blockchain.Wallet(
            network,
            random.sample(node_dict.keys(), random.randint(1, node_num)),
        )
        for _ in range(wallet_num)
    ]

    # node
    for _, node in node_dict.items():
        threading.Thread(
            target=dispatch_node,
            args=(node, )
        ).start()

    # show_network
    if bool_show_network:
        threading.Thread(
            target=show_network,
            args=(network, node_dict, )
        ).start()

    # generate transaction
    threading.Thread(
        target=generate_transactions,
        args=(wallet_list, )
    ).start()

    # sentinel
    threading.Thread(
        target=dispatch_sentinel,
        args=(sentinel, )
    ).start()


if __name__ == "__main__":
    main()
