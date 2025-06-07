class TranspositionCipher:
    def _get_order(self, key):
        key_list = list(key)
        sorted_key = sorted([(char, i) for i, char in enumerate(key_list)])
        order = [None] * len(key_list)
        for idx, (_, orig_idx) in enumerate(sorted_key):
            order[orig_idx] = idx
        return order

    def encrypt(self, plaintext: str, key: str) -> str:
        filtered = ''.join(c for c in plaintext if c.isalpha())
        n_cols = len(key)
        n_rows = (len(filtered) + n_cols - 1) // n_cols
        padded = filtered.ljust(n_rows * n_cols, 'X')
        table = [padded[i*n_cols:(i+1)*n_cols] for i in range(n_rows)]
        order = self._get_order(key)
        ciphertext = ''
        for idx in sorted(range(n_cols), key=lambda x: order[x]):
            for row in table:
                ciphertext += row[idx]
        return ciphertext

    def decrypt(self, ciphertext: str, key: str) -> str:
        filtered = ''.join(c for c in ciphertext if c.isalpha())
        n_cols = len(key)
        n_rows = (len(filtered) + n_cols - 1) // n_cols
        order = self._get_order(key)
        col_lengths = [n_rows] * n_cols
        total = n_cols * n_rows
        extra = total - len(filtered)
        for i in range(extra):
            col_lengths[sorted(range(n_cols), key=lambda x: order[x])[-(i+1)]] -= 1
        cols = []
        start = 0
        for length in col_lengths:
            cols.append(filtered[start:start+length])
            start += length
        table = [''] * n_rows
        for idx, col in zip(sorted(range(n_cols), key=lambda x: order[x]), cols):
            for row in range(len(col)):
                table[row] += col[row]
        plaintext = ''.join(table)
        return plaintext.rstrip('X') 