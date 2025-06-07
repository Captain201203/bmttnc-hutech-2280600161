class CaesarCipher:
    def __init__(self):
        self.alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    
    def encrypt(self, plaintext: str, key: int) -> str:
        """
        Mã hóa văn bản sử dụng mã Caesar
        :param plaintext: Văn bản cần mã hóa
        :param key: Khóa dịch chuyển
        :return: Văn bản đã mã hóa
        """
        plaintext = plaintext.upper()
        ciphertext = ''
        
        for char in plaintext:
            if char in self.alphabet:
                # Tìm vị trí của ký tự trong bảng chữ cái
                position = self.alphabet.find(char)
                # Dịch chuyển theo khóa và lấy modulo 26
                new_position = (position + key) % 26
                ciphertext += self.alphabet[new_position]
            else:
                # Giữ nguyên các ký tự không phải chữ cái
                ciphertext += char
                
        return ciphertext
    
    def decrypt(self, ciphertext: str, key: int) -> str:
        """
        Giải mã văn bản đã mã hóa Caesar
        :param ciphertext: Văn bản cần giải mã
        :param key: Khóa dịch chuyển
        :return: Văn bản đã giải mã
        """
        # Giải mã bằng cách mã hóa với khóa âm
        return self.encrypt(ciphertext, -key) 