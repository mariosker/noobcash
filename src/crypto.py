from hashlib import sha256

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa


def get_keypair():
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    public_key = private_key.public_key()

    return private_key, public_key


def hash_to_str(obj) -> str:
    """hash an object and return digest

    Args:
        obj (immutable obj): The object to hash

    Returns:
        str: the digest of the hash
    """
    return sha256(obj).hexdigest()
