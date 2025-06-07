import random
import hashlib

class Point:
    def __init__(self, x, y, infinity=False):
        self.x = x
        self.y = y
        self.infinity = infinity
    
    def __eq__(self, other):
        if self.infinity and other.infinity:
            return True
        if self.infinity or other.infinity:
            return False
        return self.x == other.x and self.y == other.y
    
    def __str__(self):
        if self.infinity:
            return "Point(infinity)"
        return f"Point({self.x}, {self.y})"

class ECCCipher:
    def __init__(self):
        # Sử dụng đường cong elliptic secp256k1
        self.p = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
        self.n = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
        self.a = 0x0000000000000000000000000000000000000000000000000000000000000000
        self.b = 0x0000000000000000000000000000000000000000000000000000000000000007
        self.G = Point(
            0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798,
            0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8
        )
        self.private_key = None
        self.public_key = None
    
    def generate_key(self):
        """
        Tạo cặp khóa ECC
        :return: Tuple (private_key, public_key)
        """
        # Tạo khóa riêng tư ngẫu nhiên
        self.private_key = random.randint(1, self.n - 1)
        
        # Tính khóa công khai bằng cách nhân điểm G với khóa riêng tư
        self.public_key = self._multiply(self.G, self.private_key)
        
        return self.private_key, self.public_key
    
    def sign(self, message: str) -> tuple:
        """
        Ký văn bản sử dụng khóa riêng tư
        :param message: Văn bản cần ký
        :return: Tuple (r, s) là chữ ký
        """
        if not self.private_key:
            raise ValueError("Khóa riêng tư chưa được tạo")
        
        # Tạo hash của văn bản
        message_hash = int(hashlib.sha256(message.encode()).hexdigest(), 16)
        
        while True:
            # Chọn số ngẫu nhiên k
            k = random.randint(1, self.n - 1)
            
            # Tính điểm R = k * G
            R = self._multiply(self.G, k)
            
            # Tính r = R.x mod n
            r = R.x % self.n
            if r == 0:
                continue
            
            # Tính s = (message_hash + r * private_key) * k^(-1) mod n
            k_inv = self._mod_inverse(k, self.n)
            s = ((message_hash + r * self.private_key) * k_inv) % self.n
            if s == 0:
                continue
            
            return (r, s)
    
    def verify(self, message: str, signature: tuple) -> bool:
        """
        Xác thực chữ ký sử dụng khóa công khai
        :param message: Văn bản gốc
        :param signature: Tuple (r, s) là chữ ký
        :return: True nếu chữ ký hợp lệ, False nếu không
        """
        if not self.public_key:
            raise ValueError("Khóa công khai chưa được tạo")
        
        r, s = signature
        
        # Kiểm tra điều kiện của r và s
        if not (1 <= r <= self.n - 1 and 1 <= s <= self.n - 1):
            return False
        
        # Tạo hash của văn bản
        message_hash = int(hashlib.sha256(message.encode()).hexdigest(), 16)
        
        # Tính w = s^(-1) mod n
        w = self._mod_inverse(s, self.n)
        
        # Tính u1 = message_hash * w mod n
        u1 = (message_hash * w) % self.n
        
        # Tính u2 = r * w mod n
        u2 = (r * w) % self.n
        
        # Tính điểm X = u1 * G + u2 * public_key
        X = self._add(
            self._multiply(self.G, u1),
            self._multiply(self.public_key, u2)
        )
        
        # Kiểm tra r == X.x mod n
        return r == X.x % self.n
    
    def _add(self, P: Point, Q: Point) -> Point:
        """Cộng hai điểm trên đường cong elliptic"""
        if P.infinity:
            return Q
        if Q.infinity:
            return P
        
        if P.x == Q.x:
            if (P.y + Q.y) % self.p == 0:
                return Point(0, 0, True)
            else:
                return self._double(P)
        
        # Tính lambda = (Q.y - P.y) * (Q.x - P.x)^(-1) mod p
        dx = (Q.x - P.x) % self.p
        dy = (Q.y - P.y) % self.p
        lam = (dy * self._mod_inverse(dx, self.p)) % self.p
        
        # Tính x3 = lambda^2 - P.x - Q.x mod p
        x3 = (lam * lam - P.x - Q.x) % self.p
        
        # Tính y3 = lambda * (P.x - x3) - P.y mod p
        y3 = (lam * (P.x - x3) - P.y) % self.p
        
        return Point(x3, y3)
    
    def _double(self, P: Point) -> Point:
        """Nhân đôi một điểm trên đường cong elliptic"""
        if P.infinity:
            return P
        
        if P.y == 0:
            return Point(0, 0, True)
        
        # Tính lambda = (3 * P.x^2 + a) * (2 * P.y)^(-1) mod p
        lam = ((3 * P.x * P.x + self.a) * self._mod_inverse(2 * P.y, self.p)) % self.p
        
        # Tính x3 = lambda^2 - 2 * P.x mod p
        x3 = (lam * lam - 2 * P.x) % self.p
        
        # Tính y3 = lambda * (P.x - x3) - P.y mod p
        y3 = (lam * (P.x - x3) - P.y) % self.p
        
        return Point(x3, y3)
    
    def _multiply(self, P: Point, k: int) -> Point:
        """Nhân một điểm với một số nguyên"""
        result = Point(0, 0, True)
        temp = P
        
        while k > 0:
            if k & 1:
                result = self._add(result, temp)
            temp = self._double(temp)
            k >>= 1
        
        return result
    
    def _mod_inverse(self, a: int, m: int) -> int:
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