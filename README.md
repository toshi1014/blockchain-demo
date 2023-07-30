# blockchain-demo

# Usage

`$ python3 main.py`

# Structure

```.ts
[
    ...,
    {
        "block_header": {
            "difficulty": 4,
            "merkle_root": MERKLE_ROOT_HASH,
            "nonce": NONCE,
            "previous_block_hash": PREVIOUS_BLOCK_HASH,
            "timestamp": UNIX_TIME,
            "version": "1.0"
        },
        "block_size": null,
        "transaction_counter": TX_COUNT,
        "transactions": [
            ...,
            {
                "receiver_addr": RECEIVER_PUBLIC_ADDR,
                "sender_addr": SENDER_PUBLIC_ADDR,
                "sign": PublicKey_Cryptography_SIGN,
                "timestamp": UNIX_TIME,
                "value": AMOUNT,
            },
            ...
    },
    ...
]
```

# Demo

https://github.com/toshi1014/blockchain-demo/assets/64947537/37d77aa5-8461-41e5-ae4f-2519b924e667
