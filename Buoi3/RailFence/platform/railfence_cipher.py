class RailFenceCipher:
    def encrypt(self, text: str, num_rails: int) -> str:
        if num_rails <= 1:
            return text
        rail = ['' for _ in range(num_rails)]
        dir_down = False
        row = 0
        for char in text:
            rail[row] += char
            if row == 0 or row == num_rails - 1:
                dir_down = not dir_down
            row += 1 if dir_down else -1
        return ''.join(rail)

    def decrypt(self, cipher: str, num_rails: int) -> str:
        if num_rails <= 1:
            return cipher
        rail = [['\n' for _ in range(len(cipher))] for _ in range(num_rails)]
        dir_down = None
        row, col = 0, 0
        for i in range(len(cipher)):
            if row == 0:
                dir_down = True
            if row == num_rails - 1:
                dir_down = False
            rail[row][col] = '*'
            col += 1
            row += 1 if dir_down else -1
        index = 0
        for i in range(num_rails):
            for j in range(len(cipher)):
                if rail[i][j] == '*' and index < len(cipher):
                    rail[i][j] = cipher[index]
                    index += 1
        result = []
        row, col = 0, 0
        for i in range(len(cipher)):
            if row == 0:
                dir_down = True
            if row == num_rails - 1:
                dir_down = False
            if rail[row][col] != '\n':
                result.append(rail[row][col])
                col += 1
            row += 1 if dir_down else -1
        return ''.join(result) 