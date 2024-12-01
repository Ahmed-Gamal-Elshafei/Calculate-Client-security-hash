from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
import os
import base64

# AES key size should be 16, 24, or 32 bytes (128, 192, 256 bits respectively)
KEY_SIZE = 32  # For AES-256
BLOCK_SIZE = 16  # AES block size in bytes


class AESHandler:
    def __init__(self, key: bytes = None, iv: bytes = None):
        """
        Initialize AESHandler with optional key and IV.
        Generates random key and IV if not provided.
        """
        self.key = key if key else self.generate_key(KEY_SIZE)
        self.iv = iv if iv else self.generate_iv()
        # print("key", self.key)
        # print("iv", self.iv)

    @staticmethod
    def generate_key(size: int) -> bytes:
        """Generates a random key of the specified size."""
        return os.urandom(size)

    @staticmethod
    def generate_iv() -> bytes:
        """Generates a random initialization vector (IV)."""
        return os.urandom(BLOCK_SIZE)

    def encrypt(self, plaintext: bytes) -> str:
        """
        Encrypts plaintext using AES-CBC mode.
        Returns ciphertext as a Base64-encoded string.
        """
        # Pad plaintext to be a multiple of block size
        padder = padding.PKCS7(algorithms.AES.block_size).padder()
        padded_data = padder.update(plaintext) + padder.finalize()

        # Create AES cipher and encrypt
        cipher = Cipher(
            algorithms.AES(self.key), modes.CBC(self.iv), backend=default_backend()
        )
        encryptor = cipher.encryptor()
        ciphertext = encryptor.update(padded_data) + encryptor.finalize()

        # Encode ciphertext as Base64
        return base64.b64encode(ciphertext).decode('utf-8')

    def decrypt(self, ciphertext: str) -> bytes:
        """
        Decrypts a Base64-encoded ciphertext using AES-CBC mode.
        Returns the original plaintext.
        """
        try:
            # Decode Base64 ciphertext
            ciphertext_bytes = base64.b64decode(ciphertext)

            # Create AES cipher and decrypt
            cipher = Cipher(
                algorithms.AES(self.key), modes.CBC(self.iv), backend=default_backend()
            )
            decryptor = cipher.decryptor()
            padded_plaintext = decryptor.update(ciphertext_bytes) + decryptor.finalize()

            # Unpad the plaintext
            unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
            plaintext = unpadder.update(padded_plaintext) + unpadder.finalize()
            return plaintext
        except Exception as e:
            raise ValueError(f"Decryption failed: {e}")


# if __name__ == "__main__":
#     # Example usage
#     key = b't+H<\xb4`\xb4\x1cQ\xac\x04F\xdf\x06\x99\x05H\xd0a\xd9*)\xc6 h\xcc\xcb%\xc6(\t\xb0'
#     iv = b'C\xe4\xec\xe5&\x91\xf8\xb2\x00_\x81\xa3Y\x06TZ'
#     aes = AESHandler(key, iv)
#     plaintext = b"tTQ8KNc.CS9ap_Q"
#
#     print("Original plaintext:", plaintext.decode('utf-8'))
#
#     # Encryption
#     ciphertext = aes.encrypt(plaintext)
#     print("Encrypted ciphertext (Base64):", ciphertext)
#
#     # Decryption
#     decrypted_plaintext = aes.decrypt(ciphertext)
#     print("Decrypted plaintext:", decrypted_plaintext.decode('utf-8'))
