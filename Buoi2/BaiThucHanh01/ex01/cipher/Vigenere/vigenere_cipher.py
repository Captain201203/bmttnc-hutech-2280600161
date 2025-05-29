from caesar.alphabet import ALPHABET

class VigenereCipher:
    def __init__(self):
        self.alphabet = ALPHABET
        self.alphabet_len = len(self.alphabet)

    def encrypt(self, text: str, key: str) -> str:
        encrypted_text = []
        text = text.upper()
        key = key.upper()
        key_len = len(key)
        key_index = 0

        for char in text:
            if char in self.alphabet:
                char_index = self.alphabet.index(char)
                key_char = key[key_index % key_len]
                key_char_index = self.alphabet.index(key_char)
                
                # Vigenere encryption formula: (char_index + key_char_index) % alphabet_len
                encrypted_index = (char_index + key_char_index) % self.alphabet_len
                encrypted_char = self.alphabet[encrypted_index]
                encrypted_text.append(encrypted_char)
                
                key_index += 1 # Move to the next character in the key
            else:
                # Keep non-alphabet characters as they are
                encrypted_text.append(char)
                
        return "".join(encrypted_text)

    def decrypt(self, text: str, key: str) -> str:
        decrypted_text = []
        text = text.upper()
        key = key.upper()
        key_len = len(key)
        key_index = 0

        for char in text:
            if char in self.alphabet:
                char_index = self.alphabet.index(char)
                key_char = key[key_index % key_len]
                key_char_index = self.alphabet.index(key_char)

                # Vigenere decryption formula: (char_index - key_char_index) % alphabet_len
                decrypted_index = (char_index - key_char_index) % self.alphabet_len
                decrypted_char = self.alphabet[decrypted_index]
                decrypted_text.append(decrypted_char)
                
                key_index += 1 # Move to the next character in the key
            else:
                # Keep non-alphabet characters as they are
                decrypted_text.append(char)

        return "".join(decrypted_text)
