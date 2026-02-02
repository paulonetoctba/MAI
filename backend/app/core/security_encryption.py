
from cryptography.fernet import Fernet
import base64
import hashlib
from app.config import settings

def get_cipher_suite():
    """
    Get Fernet cipher suite using settings.SECRET_KEY.
    Ensures key is 32 url-safe base64-encoded bytes.
    """
    # Hash the secret key to get 32 bytes
    key = hashlib.sha256(settings.SECRET_KEY.encode()).digest()
    # Base64 encode to make it url-safe for Fernet
    key_b64 = base64.urlsafe_b64encode(key)
    return Fernet(key_b64)

def encrypt_string(plain_text: str) -> str:
    """Encrypt a string"""
    if not plain_text:
        return ""
    cipher = get_cipher_suite()
    return cipher.encrypt(plain_text.encode()).decode()

def decrypt_string(cipher_text: str) -> str:
    """Decrypt a string"""
    if not cipher_text:
        return ""
    try:
        cipher = get_cipher_suite()
        return cipher.decrypt(cipher_text.encode()).decode()
    except Exception:
        return ""
