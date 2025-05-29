import random
import math

# Basic functions for RSA (not suitable for production use)
def is_prime(n):
    if n < 2:
        return False
    if n == 2 or n == 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def mod_inverse(a, m):
    m0 = m
    y = 0
    x = 1
    if m == 1:
        return 0
    while a > 1:
        q = a // m
        m, a = a % m, m
        y, x = x - q * y, y
    if x < 0:
        x = x + m0
    return x

def generate_keypair(p, q):
    if not (is_prime(p) and is_prime(q)):
        return "Both numbers must be prime.", None, None
    elif p == q:
        return "p and q cannot be equal.", None, None

    n = p * q
    phi = (p - 1) * (q - 1)

    # Choose e such that 1 < e < phi and gcd(e, phi) == 1
    e = random.randrange(1, phi)
    while gcd(e, phi) != 1:
        e = random.randrange(1, phi)

    # Calculate d, the modular multiplicative inverse of e mod phi
    d = mod_inverse(e, phi)

    # Public key is (e, n), private key is (d, n)
    return (e, n), (d, n)

class RSACipher:
    def __init__(self):
        pass

    # For simplicity, encryption/decryption will work on numbers (ASCII values of characters)
    # Real RSA works on blocks of data.
    def encrypt(self, plaintext: str, public_key: tuple[int, int]) -> list[int]:
        e, n = public_key
        # Ensure public key values are integers
        if not isinstance(e, int) or not isinstance(n, int):
            return [ord(char) for char in "Invalid public key: e and n must be integers."]
        # Basic check for key validity (e.g., e > 1, n > 1)
        if e <= 1 or n <= 1:
             return [ord(char) for char in "Invalid public key: e and n must be greater than 1."]
             
        # Convert plaintext to a list of numbers (ASCII values)
        # For simplicity, each character is encrypted individually.
        # Real RSA encrypts blocks of data.
        try:
            cipher = [(ord(char) ** e) % n for char in plaintext]
            return cipher
        except OverflowError:
            return [ord(char) for char in "Encryption failed: numbers too large for power calculation."]
        except Exception as ex:
            return [ord(char) for char in f"Encryption failed: {ex}"]

    def decrypt(self, ciphertext: list[int], private_key: tuple[int, int]) -> str:
        d, n = private_key
        # Ensure private key values are integers
        if not isinstance(d, int) or not isinstance(n, int):
            return "Invalid private key: d and n must be integers."
        # Basic check for key validity
        if d <= 1 or n <= 1:
             return "Invalid private key: d and n must be greater than 1."

        # Decrypt list of numbers back to characters
        plain = []
        try:
            for char_code in ciphertext:
                # Ensure each element in ciphertext is an integer
                if not isinstance(char_code, int):
                     return "Invalid ciphertext: contains non-integer elements."
                decrypted_char_code = (char_code ** d) % n
                # Basic check if decrypted code is within printable ASCII range
                if 0 <= decrypted_char_code <= 127:
                    plain.append(chr(decrypted_char_code))
                else:
                     # Handle cases where decryption results in non-ASCII values
                     # Depending on requirements, could return error or a placeholder
                     plain.append('?') # Placeholder for unprintable characters

            return "".join(plain)
        except OverflowError:
            return "Decryption failed: numbers too large for power calculation."
        except Exception as ex:
            return f"Decryption failed: {ex}" 