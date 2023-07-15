import json


filename_chain = "chain.json"
filename_transactions = "transaction_record.json"


def is_same_transactions(chain, transaction_record):
    transaction_chain = [
        tx for transactions in
        [
            block["transactions"]
            for block in chain
        ]
        for tx in transactions
    ]

    flg_invalid = sum([
        int(tx_chain != tx_record)
        for tx_chain, tx_record in zip(transaction_chain, transaction_record)
    ])

    return flg_invalid != 0


def main():
    with open(filename_chain, "r", encoding="utf-8") as f:
        chain = json.loads(f.read())

    with open(filename_transactions, "r", encoding="utf-8") as f:
        transaction_record = json.loads("[" + f.read()[:-1] + "]")

    for block in chain[1:]:
        block["transactions"] = json.loads(block["transactions"])

    print(is_same_transactions(chain, transaction_record))


if __name__ == "__main__":
    main()
