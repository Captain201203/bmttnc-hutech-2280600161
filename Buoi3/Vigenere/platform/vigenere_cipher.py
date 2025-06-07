class VigenereCipher:
    def __init__(self):
        self.alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    
    def _prepare_key(self, key: str, length: int) -> str:
        """Chuẩn bị khóa với độ dài bằng độ dài văn bản"""
        key = key.upper()
        # Lặp lại khóa cho đến khi đủ độ dài
        return (key * (length // len(key) + 1))[:length]
    
    def encrypt(self, plaintext: str, key: str) -> str:
        """
        Mã hóa văn bản sử dụng khóa Vigenere
        :param plaintext: Văn bản cần mã hóa
        :param key: Khóa mã hóa
        :return: Văn bản đã mã hóa
        """
        # Chuyển văn bản và khóa thành chữ hoa
        plaintext = plaintext.upper()
        key = key.upper()
        
        # Chuẩn bị khóa
        key = self._prepare_key(key, len(plaintext))
        
        # Mã hóa từng ký tự
        ciphertext = ''
        for i in range(len(plaintext)):
            if plaintext[i] in self.alphabet:
                # Tính vị trí mới trong bảng chữ cái
                p = self.alphabet.index(plaintext[i])
                k = self.alphabet.index(key[i])
                c = (p + k) % 26
                ciphertext += self.alphabet[c]
            else:
                # Giữ nguyên các ký tự không phải chữ cái
                ciphertext += plaintext[i]
        
        return ciphertext
    
    def decrypt(self, ciphertext: str, key: str) -> str:
        """
        Giải mã văn bản sử dụng khóa Vigenere
        :param ciphertext: Văn bản cần giải mã
        :param key: Khóa giải mã
        :return: Văn bản đã giải mã
        """
        # Chuyển văn bản và khóa thành chữ hoa
        ciphertext = ciphertext.upper()
        key = key.upper()
        
        # Chuẩn bị khóa
        key = self._prepare_key(key, len(ciphertext))
        
        # Giải mã từng ký tự
        plaintext = ''
        for i in range(len(ciphertext)):
            if ciphertext[i] in self.alphabet:
                # Tính vị trí mới trong bảng chữ cái
                c = self.alphabet.index(ciphertext[i])
                k = self.alphabet.index(key[i])
                p = (c - k) % 26
                plaintext += self.alphabet[p]
            else:
                # Giữ nguyên các ký tự không phải chữ cái
                plaintext += ciphertext[i]
        
        return plaintext 