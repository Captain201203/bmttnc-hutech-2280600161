import sys
from PyQt5 import QtWidgets
from ui.vigenere import Ui_Form
from platform.vigenere_cipher import VigenereCipher

class VigenereApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.cipher = VigenereCipher()
        
        # Kết nối các nút với hàm xử lý
        self.ui.pushButton.clicked.connect(self.encrypt_text)    # Encrypt
        self.ui.pushButton_2.clicked.connect(self.decrypt_text)  # Decrypt
        
        # Đặt tiêu đề cho cửa sổ
        self.setWindowTitle("Vigenere Cipher")
        
    def encrypt_text(self):
        """Xử lý sự kiện khi nhấn nút Encrypt"""
        try:
            # Lấy văn bản và khóa từ giao diện
            plaintext = self.ui.textEdit.toPlainText()
            key = self.ui.lineEdit.text().strip()
            
            if not plaintext:
                raise ValueError("Vui lòng nhập văn bản cần mã hóa")
            if not key:
                raise ValueError("Vui lòng nhập khóa mã hóa")
            
            # Mã hóa văn bản
            ciphertext = self.cipher.encrypt(plaintext, key)
            
            # Hiển thị kết quả
            self.ui.plainTextEdit.setPlainText(ciphertext)
            
        except Exception as e:
            QtWidgets.QMessageBox.warning(
                self,
                "Lỗi",
                f"Không thể mã hóa: {str(e)}"
            )
    
    def decrypt_text(self):
        """Xử lý sự kiện khi nhấn nút Decrypt"""
        try:
            # Lấy văn bản và khóa từ giao diện
            ciphertext = self.ui.plainTextEdit.toPlainText()
            key = self.ui.lineEdit.text().strip()
            
            if not ciphertext:
                raise ValueError("Vui lòng nhập văn bản cần giải mã")
            if not key:
                raise ValueError("Vui lòng nhập khóa giải mã")
            
            # Giải mã văn bản
            plaintext = self.cipher.decrypt(ciphertext, key)
            
            # Hiển thị kết quả
            self.ui.textEdit.setPlainText(plaintext)
            
        except Exception as e:
            QtWidgets.QMessageBox.warning(
                self,
                "Lỗi",
                f"Không thể giải mã: {str(e)}"
            )

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = VigenereApp()
    window.show()
    sys.exit(app.exec_()) 