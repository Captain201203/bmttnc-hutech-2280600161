import random
import math

class RSACipher:
    def __init__(self):
        self.p = None
        self.q = None
        self.n = None
        self.phi = None
        self.e = None
        self.d = None
        
    def generate_key(self, bits=8):
        """
        Tạo cặp khóa RSA
        :param bits: Số bit cho các số nguyên tố (mặc định là 8 bit)
        :return: Tuple (public_key, private_key)
        """
        # Tạo hai số nguyên tố p và q
        self.p = self._generate_prime(bits)
        self.q = self._generate_prime(bits)
        
        # Tính n = p * q
        self.n = self.p * self.q
        
        # Tính phi(n) = (p-1) * (q-1)
        self.phi = (self.p - 1) * (self.q - 1)
        
        # Chọn e sao cho 1 < e < phi(n) và e là số nguyên tố cùng nhau với phi(n)
        self.e = self._choose_e(self.phi)
        
        # Tính d sao cho d * e ≡ 1 (mod phi(n))
        self.d = self._mod_inverse(self.e, self.phi)
        
        # Trả về cặp khóa
        public_key = (self.n, self.e)
        private_key = (self.n, self.d)
        
        return public_key, private_key
    
    def encrypt(self, plaintext: str) -> str:
        """
        Mã hóa văn bản sử dụng khóa công khai
        :param plaintext: Văn bản cần mã hóa
        :return: Văn bản đã mã hóa
        """
        if not self.n or not self.e:
            raise ValueError("Khóa công khai chưa được tạo")
            
        # Chuyển văn bản thành số
        message = [ord(char) for char in plaintext]
        
        # Mã hóa từng ký tự
        ciphertext = []
        for m in message:
            c = pow(m, self.e, self.n)
            ciphertext.append(str(c))
            
        return ' '.join(ciphertext)
    
    def decrypt(self, ciphertext: str) -> str:
        """
        Giải mã văn bản sử dụng khóa riêng tư
        :param ciphertext: Văn bản cần giải mã
        :return: Văn bản đã giải mã
        """
        if not self.n or not self.d:
            raise ValueError("Khóa riêng tư chưa được tạo")
            
        # Tách các số từ chuỗi ciphertext
        numbers = [int(x) for x in ciphertext.split()]
        
        # Giải mã từng số
        plaintext = []
        for c in numbers:
            m = pow(c, self.d, self.n)
            plaintext.append(chr(m))
            
        return ''.join(plaintext)
    
    def sign(self, message: str) -> str:
        """
        Ký văn bản sử dụng khóa riêng tư
        :param message: Văn bản cần ký
        :return: Chữ ký
        """
        if not self.n or not self.d:
            raise ValueError("Khóa riêng tư chưa được tạo")
            
        # Tạo hash đơn giản của văn bản
        hash_value = sum(ord(char) for char in message)
        
        # Ký hash bằng khóa riêng tư
        signature = pow(hash_value, self.d, self.n)
        
        return str(signature)
    
    def verify(self, message: str, signature: str) -> bool:
        """
        Xác thực chữ ký sử dụng khóa công khai
        :param message: Văn bản gốc
        :param signature: Chữ ký cần xác thực
        :return: True nếu chữ ký hợp lệ, False nếu không
        """
        if not self.n or not self.e:
            raise ValueError("Khóa công khai chưa được tạo")
            
        try:
            # Tạo hash đơn giản của văn bản
            hash_value = sum(ord(char) for char in message)
            
            # Giải mã chữ ký bằng khóa công khai
            decrypted_hash = pow(int(signature), self.e, self.n)
            
            # So sánh hash đã giải mã với hash của văn bản
            return decrypted_hash == hash_value
            
        except ValueError:
            return False
    
    def _generate_prime(self, bits):
        """Tạo số nguyên tố ngẫu nhiên với số bit cho trước"""
        while True:
            # Tạo số ngẫu nhiên với số bit cho trước
            num = random.getrandbits(bits)
            # Đảm bảo số là lẻ
            num |= 1
            # Kiểm tra tính nguyên tố
            if self._is_prime(num):
                return num
    
    def _is_prime(self, n, k=5):
        """Kiểm tra tính nguyên tố của một số sử dụng thuật toán Miller-Rabin"""
        if n <= 1:
            return False
        if n <= 3:
            return True
        if n % 2 == 0:
            return False
            
        # Tìm r và d sao cho n-1 = 2^r * d
        r, d = 0, n - 1
        while d % 2 == 0:
            r += 1
            d //= 2
            
        # Kiểm tra k lần
        for _ in range(k):
            a = random.randint(2, n - 2)
            x = pow(a, d, n)
            if x == 1 or x == n - 1:
                continue
            for _ in range(r - 1):
                x = pow(x, 2, n)
                if x == n - 1:
                    break
            else:
                return False
        return True
    
    def _choose_e(self, phi):
        """Chọn e sao cho 1 < e < phi và e là số nguyên tố cùng nhau với phi"""
        while True:
            e = random.randint(2, phi - 1)
            if math.gcd(e, phi) == 1:
                return e
    
    def _mod_inverse(self, a, m):
        """Tính nghịch đảo modulo của a theo m"""
        def extended_gcd(a, b):
            if a == 0:
                return b, 0, 1
            gcd, x1, y1 = extended_gcd(b % a, a)
            x = y1 - (b // a) * x1
            y = x1
            return gcd, x, y
            
        gcd, x, _ = extended_gcd(a, m)
        if gcd != 1:
            raise ValueError("Không tồn tại nghịch đảo modulo")
        return x % m 