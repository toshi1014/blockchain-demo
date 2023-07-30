import json


filename_chain = "chain.json"
filename_transactions = "transaction_record.json"


def is_same_transactions(chain, transaction_record):
    str_transaction_in_chain = [
        json.dumps(tx, sort_keys=True)
        for transactions in
        [
            block["transactions"]
            for block in chain
        ]
        for tx in transactions
    ]
    str_transaction_record = [
        json.dumps(tx, sort_keys=True)
        for tx in transaction_record
    ]

    flg_invalid = sum([
        int(str_tx_in_chain != str_tx_record)
        for str_tx_in_chain, str_tx_record in zip(str_transaction_in_chain, str_transaction_record)
    ])
    return flg_invalid == 0


def main():
    with open(filename_chain, "r", encoding="utf-8") as f:
        chain = json.loads(f.read())

    with open(filename_transactions, "r", encoding="utf-8") as f:
        transaction_record = json.loads("[" + f.read()[:-1] + "]")

    print(is_same_transactions(chain, transaction_record))


if __name__ == "__main__":
    main()
