class RailFenceCipher:
    def __init__(self):
        pass

    def encrypt(self, text: str, key: int) -> str:
        if key < 2:
            return "Invalid key. Number of rails must be at least 2."

        # Remove spaces and convert to uppercase for simpler processing
        clean_text = "".join(text.split()).upper()
        n = len(clean_text)
        # If key is greater than or equal to the text length, it's effectively just 1 rail.
        # Although mathematically it might work, practically for Rail Fence, key >= length/2 + 1 doesn't add complexity
        # and key >= length makes it trivial. Let's keep the key check simple for now based on the problem context.
        if key >= n:
             # While not strictly an error, it makes the cipher trivial. Handling for clarity.
             # Depending on desired behavior, could return text directly or handle specifically.
             # For now, let the logic proceed which will handle this, but min key 2 check is vital.
             pass # Proceed with standard logic

        # Create the rail matrix
        rail = [[] for _ in range(key)]
        direction = -1 # -1 for going up, 1 for going down
        row = 0

        # Fill the rail matrix in a zigzag pattern
        for char in clean_text:
            rail[row].append(char)
            if row == 0 or row == key - 1:
                direction *= -1 # Reverse direction at top or bottom rail
            row += direction

        # Concatenate the rails to get the ciphertext
        ciphertext = "".join("".join(r) for r in rail)
        return ciphertext

    def decrypt(self, text: str, key: int) -> str:
        if key < 2:
            return "Invalid key. Number of rails must be at least 2."

        clean_text = "".join(text.split()).upper()
        n = len(clean_text)
        if key >= n:
             # Handle trivial case as in encryption if necessary, but decryption logic handles this
             pass # Proceed with standard logic

        # Create an empty matrix to track positions
        rail = [['\n' for _ in range(n)] for _ in range(key)]
        direction = -1
        row = 0
        col = 0

        # Mark the positions in zigzag pattern
        for i in range(n):
            rail[row][col] = '*'
            col += 1
            if row == 0 or row == key - 1:
                direction *= -1
            row += direction

        # Fill the marked positions with ciphertext characters
        index = 0
        for i in range(key):
            for j in range(n):
                if rail[i][j] == '*' and index < n:
                    rail[i][j] = clean_text[index]
                    index += 1

        # Read the matrix in zigzag pattern to get the plaintext
        result = []
        direction = -1
        row = 0
        col = 0

        for i in range(n):
            result.append(rail[row][col])
            if row == 0 or row == key - 1:
                direction *= -1
            row += direction
            col += 1

        return "".join(result) 