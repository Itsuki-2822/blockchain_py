### 最終更新日 ###
# 6月25日

### TODO ###
# トランザクションの追加: 現在のコードでは、ブロックにデータを含めることができますが、より実用的なブロックチェーンを構築するためには、トランザクションの追加やトランザクションの検証機能を実装することが重要です。
# ブロックの検証: ブロックチェーンにおいては、ブロックが正当であるかどうかを検証する仕組みが必要です。ブロックのハッシュや直前のブロックのハッシュなど、様々な要素を検証するロジックを導入することで、ブロックチェーンのセキュリティを強化できます。
# P2Pの導入
# PoSの導入の検討


from datetime import datetime, timezone, timedelta
import hashlib
import json
import wallet

jst = timezone(timedelta(hours=+9), 'JST')


class Blockchain(object):
    def __init__(self):
        self.chain = []
        self.wallets = {}

    def genesis_block(self, index, data, nonce, previous_hash, Block_hash):
        JAPAN_time = datetime.now(jst).strftime("%Y-%m-%d %H:%M:%S")
        genesis_data = {
            'index': index,
            'timestamp': JAPAN_time,
            'data': data,
            'nonce': nonce,
            'previous_hash': previous_hash,
            'Block_hash': Block_hash,
            'transactions': []
        }
        self.chain.append(genesis_data)
        return genesis_data

    def calculate_hash(self, block):
        block_str = json.dumps(block, sort_keys=True)
        block_hash = hashlib.sha256(block_str.encode()).hexdigest()
        return block_hash

    def mine_block(self, data,Block_hash):
        JAPAN_time = datetime.now(jst).strftime("%Y-%m-%d %H:%M:%S")
        previous_block = self.chain[-1]
        previous_hash = previous_block['Block_hash']
        index = previous_block['index'] + 1
        nonce = 0

        mining_difficulty = '00000'
        while True:
            block = {
                'index': index,
                'timestamp': JAPAN_time,
                'data':data,
                'nonce': nonce,
                'previous_hash': previous_hash,
                'Block_hash': None,
            }
            self.block_hash = self.calculate_hash(block)

            if self.block_hash[:len(mining_difficulty)] == mining_difficulty:
                block['Block_hash'] = self.block_hash
                self.chain.append(block)
                break

            nonce += 1

        return self.chain[-1]


def print_chain(chain):
    print("------------------------------------")
    for block in chain:
        print(" ")
        print("index:", block['index'])
        print("timestamp:", block['timestamp'])
        print("data:", block['data'])
        print("nonce:", block['nonce'])
        print("previous_hash:", block['previous_hash'])
        print("Block_hash:", block['Block_hash'])
        print(" ")
    print("------------------------------------")


if __name__ == "__main__":
    blockchain = Blockchain()

    genesis_block = blockchain.genesis_block(1, "GENESIS", None, None, blockchain.calculate_hash({}))
    print_chain(blockchain.chain)
    print(" ")

    # ブロックのマイニングとチェーンの更新
    block1 = blockchain.mine_block("いつき",blockchain.chain[-1]['Block_hash'])
    print_chain(blockchain.chain)
    print(" ")
