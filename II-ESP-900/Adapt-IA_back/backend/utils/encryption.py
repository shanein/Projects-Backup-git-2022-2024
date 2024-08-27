from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Random import get_random_bytes
from base64 import b64encode, b64decode


temp_key = "2VKIB0cz89nVTvv7DMeIXqAyv1eQMg/3ERrjiMzpU5c="


def generate_aes_key():
    key = get_random_bytes(32)
    return b64encode(key).decode("utf-8")


def aes_encrypt(data):
    key = b64decode(temp_key)
    iv = get_random_bytes(AES.block_size)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    ct_bytes = cipher.encrypt(pad(data.encode("utf-8"), AES.block_size))
    encrypted_data = b64encode(iv + ct_bytes)
    return encrypted_data
