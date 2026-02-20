import secrets
import hashlib
import hmac


def generate_password(length: int = 20) -> str:
    h = hashlib.sha256(b"NU11BYT3_CRYPTO_PASSWORD_SEED_1337").digest()
    key = secrets.token_bytes(32)
    crypto_password = hmac.new(key, h, hashlib.sha1).hexdigest()
    return crypto_password[:length]

if __name__ == "__main__":
    print("Generated password:", generate_password())
