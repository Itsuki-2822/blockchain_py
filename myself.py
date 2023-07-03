### 最終更新日 ###
# 7月1日

### TODO ###
# walletを別ファイルに格納
# genesis_blockの表示
# mine_blockの表示
# ブロックの検証: ブロックチェーンにおいては、ブロックが正当であるかどうかを検証する仕組みが必要です。ブロックのハッシュや直前のブロックのハッシュなど、様々な要素を検証するロジックを導入することで、ブロックチェーンのセキュリティを強化できます。
# P2Pの導入
# PoSの導入の検討


import json
import hashlib
import datetime
from datetime import timezone
from ecdsa import SigningKey, NIST256p
import base58
import wallet


class Blockchain(object):
    def __init__(self):
        self.chain = []

    def genesis_block(self):
        genesis_data = {
            'index': 0,
            'timestamp': self.get_timestamp(),
            'data': 'GENESIS',
            'nonce': None,
            'previous_hash': None,
            'block_hash': self.calculate_hash({})
        }
        self.chain.append(genesis_data)

    def get_timestamp(self):
        return datetime.datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")

    def calculate_hash(self, block):
        block_str = json.dumps(block, sort_keys=True).encode()
        block_hash = hashlib.sha256(block_str).hexdigest()
        return block_hash

    def mine_block(self, data):
        previous_block = self.chain[-1]
        previous_hash = previous_block['block_hash']
        index = previous_block['index'] + 1
        nonce = 0
        mining_difficulty = '00000'

        while True:
            block = {
                'index': index,
                'timestamp': self.get_timestamp(),
                'data': data,
                'nonce': nonce,
                'previous_hash': previous_hash,
                'block_hash': None
            }
            block_hash = self.calculate_hash(block)

            if block_hash[:len(mining_difficulty)] == mining_difficulty:
                block['block_hash'] = block_hash
                self.chain.append(block)
                break

            nonce += 1

        return block


    
def get_transaction_details():
    recipient_address = input("Enter recipient address: ")
    value = float(input("Enter value: "))
    return recipient_address, value

if __name__ == "__main__":
    blockchain = Blockchain()
    blockchain.genesis_block()

    recipient_address = input("Enter recipient address: ")
    value = float(input("Enter value: "))

    wallet = wallet.Wallet(recipient_address=recipient_address, value=value)
    print("Private Key:", wallet.private_key)
    print("Public Key:", wallet.public_key)
    print("Blockchain Address:", wallet.blockchain_address)
    print()

    transaction = wallet.create_transaction()
    print("Transaction:", transaction)
    print()


    """
    if __name__ == "__main__":
    blockchain = Blockchain()

    genesis_block = blockchain.genesis_block(1, "GENESIS", None, None, blockchain.calculate_hash({}))
    print_chain(blockchain.chain)
    print(" ")

    # ブロックのマイニングとチェーンの更新
    block1 = blockchain.mine_block("いつき",blockchain.chain[-1]['Block_hash'])
    print_chain(blockchain.chain)
    print(" ")
    """