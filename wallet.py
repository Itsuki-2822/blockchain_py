### TODO ###
# 認証の機能追加 6/27
# 認証の機能の詳しい理解と応用

import base58
import codecs
import hashlib

from ecdsa import NIST256p
from ecdsa import SigningKey


class Wallet(object):

    def __init__(self):
        self._private_key = SigningKey.generate(curve=NIST256p)
        self._public_key = self._private_key.get_verifying_key()
        self._blockchain_address = self.generate_blockchain_address()

    @property
    def private_key(self):
        return self._private_key.to_string().hex()

    @property
    def public_key(self):
        return self._public_key.to_string().hex()

    @property
    def blockchain_address(self):
        return self._blockchain_address

    def generate_blockchain_address(self):
        # 公開鍵をバイト列に変換し、SHA-256ハッシュを計算する
        public_key_bytes = self._public_key.to_string()
        sha256_bpk_digest = hashlib.sha256(public_key_bytes).digest()

        # RIPEMD-160ハッシュを計算する
        ripemed160_bpk_digest = hashlib.new('ripemd160', sha256_bpk_digest).digest()

        # ネットワークバイトを追加してアドレスを形成する
        network_bitcoin_public_key = b'00' + ripemed160_bpk_digest

        # ハッシュのチェックサムを計算する
        sha256_2_nbpk_digest = hashlib.sha256(hashlib.sha256(network_bitcoin_public_key).digest()).digest()
        checksum = sha256_2_nbpk_digest[:8]

        # アドレスの16進数表現を生成する
        address_hex = (network_bitcoin_public_key + checksum).hex()

        # Base58エンコードしてブロックチェーンアドレスを生成する
        blockchain_address = base58.b58encode(bytes.fromhex(address_hex)).decode('utf-8')
        return blockchain_address

class Transaction(object):
    def __init__(self,sender_private_key,sender_public_key,
                 sender_blockchain_address,recipient_blockchain_address,value):
        self.sender_private_key = sender_private_key
        self.sender_public_key = sender_public_key
        self.sender_blockchain_address = sender_blockchain_address
        self.recipient_blockchain_address = recipient_blockchain_address
        self.value = value

    def generate_signature(self):
        transacrion = {
            'sender_blockchain_address':self.sender_blockchain_address,
            'recipient_blockchain_address':self.recipient_blockchain_address,
            'value':float(self.value)
        }
        message = hashlib.sha256().digest()
        private_key = SigningKey.from_string(bytes().fromhex(self.sender_private_key),curve = NIST256p)
        private_key_sign = private_key.sign(message)
        signature = private_key_sign.hex()
        return signature


if __name__ == '__main__':
    wallet = Wallet()
    print("private_key :",wallet.private_key)
    print("public_key :",wallet.public_key)
    print("address :",wallet.blockchain_address)
    
    transaction = Transaction(wallet.private_key,wallet.public_key,wallet.blockchain_address,"B",1.0)
    print("signature :",transaction.generate_signature())