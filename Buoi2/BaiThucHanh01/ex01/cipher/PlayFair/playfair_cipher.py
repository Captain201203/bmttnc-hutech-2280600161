from caesar.alphabet import ALPHABET

class PlayfairCipher:
    def __init__(self):
        self.alphabet = [c for c in ALPHABET if c != 'J'] # Use I/J together
        self.alphabet_len = len(self.alphabet) # Should be 25

    def create_matrix(self, key: str) -> list[list[str]]:
        key = key.upper().replace('J', 'I')
        key_chars = []
        for char in key:
            if char.isalpha() and char not in key_chars:
                key_chars.append(char)

        alphabet_chars = [char for char in self.alphabet if char not in key_chars]
        matrix_chars = key_chars + alphabet_chars

        matrix = []
        for i in range(0, 25, 5):
            matrix.append(matrix_chars[i:i+5])
        return matrix

    def find_char(self, matrix: list[list[str]], char: str) -> tuple[int, int] | None:
        for r in range(5):
            for c in range(5):
                if matrix[r][c] == char:
                    return r, c
        return None # Should not happen if char is in modified alphabet

    def encrypt(self, text: str, key: str) -> str:
        matrix = self.create_matrix(key)
        text = text.upper().replace('J', 'I')
        clean_text = "".join([char for char in text if char.isalpha()])

        # Prepare digraphs
        digraphs = []
        i = 0
        while i < len(clean_text):
            char1 = clean_text[i]
            if i + 1 == len(clean_text):
                digraphs.append((char1, 'X')) # Add filler if odd length
                i += 1
            else:
                char2 = clean_text[i+1]
                if char1 == char2:
                    digraphs.append((char1, 'X')) # Add filler if same characters
                    i += 1
                else:
                    digraphs.append((char1, char2))
                    i += 2

        encrypted_digraphs = []
        for char1, char2 in digraphs:
            r1, c1 = self.find_char(matrix, char1)
            r2, c2 = self.find_char(matrix, char2)

            # Apply encryption rules
            if r1 == r2: # Same row
                encrypted_char1 = matrix[r1][(c1 + 1) % 5]
                encrypted_char2 = matrix[r2][(c2 + 1) % 5]
            elif c1 == c2: # Same column
                encrypted_char1 = matrix[(r1 + 1) % 5][c1]
                encrypted_char2 = matrix[(r2 + 1) % 5][c2]
            else: # Different row and column
                encrypted_char1 = matrix[r1][c2]
                encrypted_char2 = matrix[r2][c1]

            encrypted_digraphs.append(encrypted_char1 + encrypted_char2)

        return "".join(encrypted_digraphs)

    def decrypt(self, text: str, key: str) -> str:
        matrix = self.create_matrix(key)
        text = text.upper().replace('J', 'I')
        clean_text = "".join([char for char in text if char.isalpha()])

        # Digraphs for decryption should already be paired
        if len(clean_text) % 2 != 0:
             # Should not happen with properly encrypted text, but handle for robustness
             return "Invalid ciphertext length for decryption."

        digraphs = [(clean_text[i], clean_text[i+1]) for i in range(0, len(clean_text), 2)]

        decrypted_digraphs = []
        for char1, char2 in digraphs:
            r1, c1 = self.find_char(matrix, char1)
            r2, c2 = self.find_char(matrix, char2)

            if r1 is None or r2 is None:
                 # Handle characters not found in matrix (e.g., if ciphertext contains non-alpha)
                 # For simplicity, we assume input is valid Playfair ciphertext
                 return "Invalid characters in ciphertext."

            # Apply decryption rules
            if r1 == r2: # Same row
                decrypted_char1 = matrix[r1][(c1 - 1) % 5]
                decrypted_char2 = matrix[r2][(c2 - 1) % 5]
            elif c1 == c2: # Same column
                decrypted_char1 = matrix[(r1 - 1) % 5][c1]
                decrypted_char2 = matrix[(r2 - 1) % 5][c2]
            else: # Different row and column
                decrypted_char1 = matrix[r1][c2]
                decrypted_char2 = matrix[r2][c1]

            decrypted_digraphs.append(decrypted_char1 + decrypted_char2)

        return "".join(decrypted_digraphs) 