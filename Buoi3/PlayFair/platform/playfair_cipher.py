import string

class PlayfairCipher:
    def __init__(self):
        pass

    def _generate_key_square(self, key: str):
        key = key.upper().replace('J', 'I')
        key_square = []
        used = set()
        for char in key:
            if char in string.ascii_uppercase and char not in used:
                key_square.append(char)
                used.add(char)
        for char in string.ascii_uppercase:
            if char == 'J':
                continue
            if char not in used:
                key_square.append(char)
                used.add(char)
        return [key_square[i*5:(i+1)*5] for i in range(5)]

    def _process_text(self, text: str, for_encrypt=True):
        text = text.upper().replace('J', 'I')
        result = ''
        i = 0
        while i < len(text):
            a = text[i]
            b = ''
            if i + 1 < len(text):
                b = text[i+1]
            if a not in string.ascii_uppercase:
                i += 1
                continue
            if b and b not in string.ascii_uppercase:
                result += a
                i += 1
                continue
            if not b or a == b:
                b = 'X'
                i += 1
            else:
                i += 2
            result += a + b
        return result

    def encrypt(self, plaintext: str, key: str) -> str:
        key_square = self._generate_key_square(key)
        plaintext = self._process_text(plaintext, True)
        ciphertext = ''
        for i in range(0, len(plaintext), 2):
            a, b = plaintext[i], plaintext[i+1]
            row1, col1 = self._find_position(key_square, a)
            row2, col2 = self._find_position(key_square, b)
            if row1 == row2:
                ciphertext += key_square[row1][(col1+1)%5]
                ciphertext += key_square[row2][(col2+1)%5]
            elif col1 == col2:
                ciphertext += key_square[(row1+1)%5][col1]
                ciphertext += key_square[(row2+1)%5][col2]
            else:
                ciphertext += key_square[row1][col2]
                ciphertext += key_square[row2][col1]
        return ciphertext

    def decrypt(self, ciphertext: str, key: str) -> str:
        key_square = self._generate_key_square(key)
        plaintext = ''
        for i in range(0, len(ciphertext), 2):
            a, b = ciphertext[i], ciphertext[i+1]
            row1, col1 = self._find_position(key_square, a)
            row2, col2 = self._find_position(key_square, b)
            if row1 == row2:
                plaintext += key_square[row1][(col1-1)%5]
                plaintext += key_square[row2][(col2-1)%5]
            elif col1 == col2:
                plaintext += key_square[(row1-1)%5][col1]
                plaintext += key_square[(row2-1)%5][col2]
            else:
                plaintext += key_square[row1][col2]
                plaintext += key_square[row2][col1]
        return plaintext

    def _find_position(self, key_square, char):
        for i in range(5):
            for j in range(5):
                if key_square[i][j] == char:
                    return i, j
        raise ValueError(f"Ký tự {char} không có trong key square!") 