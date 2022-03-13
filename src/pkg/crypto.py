from hashlib import sha256

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa


def get_keypair() -> tuple[bytes]:
    """Returns a private/ public keypair

    Args:

    Returns:
        tuple(rsa.RSAPrivateKey, rsa.RSAPublicKey): tuple containing private and public key
    """
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    public_key = private_key.public_key()

    pem_private_key = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption())

    pem_public_key = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo)

    return pem_private_key, pem_public_key


def get_signature(message: str, private_key: bytes) -> bytes:
    """get a signature of message

    Args:
        message (str): a message to sign
        private_key (rsa.RSAPrivateKey): the private key used for signing

    Returns:
        bytes: the signature
    """
    private_key = serialization.load_pem_private_key(private_key, password=None)

    return private_key.sign(
        message.encode(),
        padding.PSS(mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH), hashes.SHA256())


def is_signature_valid(signature: bytes, message: str,
                       public_key: bytes) -> bool:
    """check if a signature is valid

    Args:
        signature (bytes): the signature to be validated
        message (str): the message of the signature
        public_key (rsa.RSAPublicKey): public key to be used for validation

    Returns:
        bool: True if signature is valid else False
    """
    try:
        public_key = serialization.load_pem_public_key(public_key)

        public_key.verify(
            signature, message.encode(),
            padding.PSS(mgf=padding.MGF1(hashes.SHA256()),
                        salt_length=padding.PSS.MAX_LENGTH), hashes.SHA256())
        return True

    except InvalidSignature:
        return False


def hash_to_str(message: str) -> str:
    """hash a message and return it's digest

    Args:
        message (str): The object to hash

    Returns:
        str: the digest of the hash
    """
    return sha256(message.encode()).hexdigest()
