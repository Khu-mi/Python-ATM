"""Security helpers for hashing and verifying PINs."""

import hashlib
import hmac
import secrets


class PinSecurity:
    """Hashes and verifies PINs so raw PINs are never stored."""

    # Algorithm choice: SHA-256 via PBKDF2.
    # - MD5 and SHA-1 are broken/weak, so they are ruled out.
    # - Plain SHA-256 is secure but very fast, which makes brute-forcing
    #   a short PIN cheap. PBKDF2 repeats it many times to slow guessing.
    # - BLAKE2b is modern and fast, but speed is a disadvantage here.
    ITERATIONS = 100000

    @staticmethod
    def _digest(pin, salt):
        """Return the hex digest of a PIN combined with a salt."""
        return hashlib.pbkdf2_hmac(
            "sha256",
            pin.encode(),
            salt.encode(),
            PinSecurity.ITERATIONS,
        ).hex()

    @staticmethod
    def hash_pin(pin):
        """Return 'salt$hash' for a PIN, using a fresh random salt."""
        salt = secrets.token_hex(16)
        digest = PinSecurity._digest(pin, salt)
        return f"{salt}${digest}"

    @staticmethod
    def verify_pin(pin, stored_value):
        """Return True if the PIN matches the stored 'salt$hash'."""
        salt, stored_digest = stored_value.split("$")
        digest = PinSecurity._digest(pin, salt)
        # compare_digest avoids leaking information through timing
        return hmac.compare_digest(digest, stored_digest)
    