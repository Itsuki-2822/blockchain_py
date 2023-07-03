### TODO ###
# 認証の機能追加 6/27
# 認証の機能の詳しい理解と応用

import json
import hashlib
import datetime
from datetime import timezone
from ecdsa import SigningKey, NIST256p
import base58


class Wallet(object):
    def __init__(self, recipient_address=None, value=None):
        self._private_key = SigningKey.generate(curve=NIST256p)
        self._public_key = self._private_key.get_verifying_key()
        self._blockchain_address = self.generate_blockchain_address()
        self.recipient_address = recipient_address
        self.value = value

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
        public_key_bytes = self._public_key.to_string()
        sha256_bpk_digest = hashlib.sha256(public_key_bytes).digest()
        ripemed160_bpk_digest = hashlib.new('ripemd160', sha256_bpk_digest).digest()
        network_bitcoin_public_key = b'00' + ripemed160_bpk_digest
        sha256_2_nbpk_digest = hashlib.sha256(hashlib.sha256(network_bitcoin_public_key).digest()).digest()
        checksum = sha256_2_nbpk_digest[:8]
        address_hex = (network_bitcoin_public_key + checksum).hex()
        blockchain_address = base58.b58encode(bytes.fromhex(address_hex)).decode('utf-8')
        return blockchain_address

    def create_transaction(self):
        signature = self.generate_signature()
        transaction = {
            'sender_blockchain_address': self.blockchain_address,
            'recipient_blockchain_address': self.recipient_address,
            'value': self.value,
            'signature': signature
        }
        return transaction

    def generate_signature(self):
        transaction_data = {
            'sender_blockchain_address': self.blockchain_address,
            'recipient_blockchain_address': self.recipient_address,
            'value': self.value
        }
        transaction_str = json.dumps(transaction_data, sort_keys=True).encode()
        private_key = SigningKey.from_string(bytes.fromhex(self.private_key), curve=NIST256p)
        signature = private_key.sign(transaction_str)
        return signature.hex()


if __name__ == '__main__':
    wallet = Wallet()
    print("private_key :",wallet.private_key)
    print("public_key :",wallet.public_key)
    print("address :",wallet.blockchain_address)
    print("signature :",wallet.generate_signature())
