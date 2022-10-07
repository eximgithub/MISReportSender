from Crypto.Cipher import DES3
from Crypto.Hash import SHA256
import hashlib

hash = SHA256.new()
hash.update('message')
hash.digest()
