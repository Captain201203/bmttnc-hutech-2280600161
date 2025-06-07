import sys
from PyQt5 import QtWidgets
from ui.rsa import Ui_Form
from platform.rsa_cipher import RSACipher

class RSAApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.cipher = RSACipher()
        
        # Kết nối các nút với hàm xử lý
        self.ui.pushButton_5.clicked.connect(self.generate_key)  # Generate Key
        self.ui.pushButton.clicked.connect(self.encrypt_text)     # Encrypt
        self.ui.pushButton_2.clicked.connect(self.decrypt_text)   # Decrypt
        self.ui.pushButton_3.clicked.connect(self.sign_text)      # Sign
        self.ui.pushButton_4.clicked.connect(self.verify_signature)  # Verify
        
        # Đặt tiêu đề cho cửa sổ
        self.setWindowTitle("RSA Cipher")
        
    def generate_key(self):
        """Xử lý sự kiện khi nhấn nút Generate Key"""
        try:
            # Tạo cặp khóa mới
            public_key, private_key = self.cipher.generate_key()
            
            # Hiển thị thông tin khóa
            key_info = f"Public Key (n,e): ({public_key[0]}, {public_key[1]})\n"
            key_info += f"Private Key (n,d): ({private_key[0]}, {private_key[1]})"
            self.ui.plainTextEdit_2.setPlainText(key_info)
            
        except Exception as e:
            QtWidgets.QMessageBox.warning(
                self,
                "Lỗi",
                f"Không thể tạo khóa: {str(e)}"
            )
    
    def encrypt_text(self):
        """Xử lý sự kiện khi nhấn nút Encrypt"""
        try:
            # Lấy văn bản cần mã hóa
            plaintext = self.ui.plainTextEdit.toPlainText()
            if not plaintext:
                raise ValueError("Vui lòng nhập văn bản cần mã hóa")
                
            # Mã hóa văn bản
            ciphertext = self.cipher.encrypt(plaintext)
            
            # Hiển thị kết quả
            self.ui.plainTextEdit_3.setPlainText(ciphertext)
            
        except Exception as e:
            QtWidgets.QMessageBox.warning(
                self,
                "Lỗi",
                f"Không thể mã hóa: {str(e)}"
            )
    
    def decrypt_text(self):
        """Xử lý sự kiện khi nhấn nút Decrypt"""
        try:
            # Lấy văn bản cần giải mã
            ciphertext = self.ui.plainTextEdit_3.toPlainText()
            if not ciphertext:
                raise ValueError("Vui lòng nhập văn bản cần giải mã")
                
            # Giải mã văn bản
            plaintext = self.cipher.decrypt(ciphertext)
            
            # Hiển thị kết quả
            self.ui.plainTextEdit.setPlainText(plaintext)
            
        except Exception as e:
            QtWidgets.QMessageBox.warning(
                self,
                "Lỗi",
                f"Không thể giải mã: {str(e)}"
            )
    
    def sign_text(self):
        """Xử lý sự kiện khi nhấn nút Sign"""
        try:
            # Lấy văn bản cần ký
            message = self.ui.plainTextEdit.toPlainText()
            if not message:
                raise ValueError("Vui lòng nhập văn bản cần ký")
                
            # Tạo chữ ký
            signature = self.cipher.sign(message)
            
            # Hiển thị chữ ký
            self.ui.plainTextEdit_4.setPlainText(signature)
            
        except Exception as e:
            QtWidgets.QMessageBox.warning(
                self,
                "Lỗi",
                f"Không thể tạo chữ ký: {str(e)}"
            )
    
    def verify_signature(self):
        """Xử lý sự kiện khi nhấn nút Verify"""
        try:
            # Lấy văn bản và chữ ký
            message = self.ui.plainTextEdit.toPlainText()
            signature = self.ui.plainTextEdit_4.toPlainText()
            
            if not message or not signature:
                raise ValueError("Vui lòng nhập đầy đủ văn bản và chữ ký")
                
            # Xác thực chữ ký
            is_valid = self.cipher.verify(message, signature)
            
            # Hiển thị kết quả
            if is_valid:
                QtWidgets.QMessageBox.information(
                    self,
                    "Kết quả",
                    "Chữ ký hợp lệ!"
                )
            else:
                QtWidgets.QMessageBox.warning(
                    self,
                    "Kết quả",
                    "Chữ ký không hợp lệ!"
                )
                
        except Exception as e:
            QtWidgets.QMessageBox.warning(
                self,
                "Lỗi",
                f"Không thể xác thực chữ ký: {str(e)}"
            )

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = RSAApp()
    window.show()
    sys.exit(app.exec_()) 