class TranspositionCipher:
    def __init__(self):
        pass

    def encrypt(self, text: str, key: int) -> str:
        # Remove spaces and convert to uppercase for simpler processing
        clean_text = "".join(text.split()).upper()
        n = len(clean_text)

        # Ensure key is valid
        if key <= 0 or not isinstance(key, int):
             return "Invalid key. Number of rails must be a positive integer."
        if key > n and n > 0:
             # If key (number of columns) is greater than text length, the cipher is trivial
             # Each character goes into its own column.
             # While technically correct, often a key smaller than text length is expected.
             # We can let the logic handle this, but adding a note.
             pass # proceed

        # Create columns
        columns = [''] * key

        # Fill columns top to bottom, left to right
        for i in range(n):
            col_index = i % key
            columns[col_index] += clean_text[i]

        # Concatenate columns to get ciphertext
        ciphertext = ''.join(columns)
        return ciphertext

    def decrypt(self, text: str, key: int) -> str:
        # Remove spaces and convert to uppercase for simpler processing
        clean_text = "".join(text.split()).upper()
        n = len(clean_text)

        # Ensure key is valid
        if key <= 0 or not isinstance(key, int):
             return "Invalid key. Key must be a positive integer."
        if key > n and n > 0:
             # If key (number of columns) is greater than text length, the cipher is trivial
             # We can let the logic handle this.
             pass # proceed

        # Calculate number of rows and shaded boxes (cells not filled)
        num_rows = n // key
        num_shaded_boxes = key - (n % key) if n % key != 0 else 0
        num_full_columns = key - num_shaded_boxes

        # Create a grid to place characters
        grid = [['' for _ in range(key)] for _ in range(num_rows + (1 if num_shaded_boxes > 0 else 0))]

        # Place characters into the grid column by column
        char_index = 0
        for col in range(key):
            # Determine how many characters are in this column
            chars_in_col = num_rows + (1 if col < num_full_columns else 0)

            for row in range(chars_in_col):
                 if char_index < n: # Ensure we don't go out of bounds
                      grid[row][col] = clean_text[char_index]
                      char_index += 1

        # Read the grid row by row to get plaintext
        plaintext = ''.join(grid[row][col] for row in range(len(grid)) for col in range(key) if grid[row][col] != '') # Read only non-empty cells

        return plaintext 