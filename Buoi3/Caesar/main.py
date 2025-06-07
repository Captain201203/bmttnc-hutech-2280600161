import sys
from PyQt5 import QtWidgets
from ui.caesar import Ui_Form
from platform.caesar_cipher import CaesarCipher

class CaesarCipherApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.cipher = CaesarCipher()
        
        # Kết nối các nút với hàm xử lý
        self.ui.pushButton.clicked.connect(self.encrypt_text)
        self.ui.pushButton_2.clicked.connect(self.decrypt_text)
        
        # Đặt tiêu đề cho cửa sổ
        self.setWindowTitle("Caesar Cipher")
        
    def encrypt_text(self):
        """Xử lý sự kiện khi nhấn nút Encrypt"""
        try:
            # Lấy văn bản và khóa từ giao diện
            plaintext = self.ui.plainTextEdit.toPlainText()
            key = int(self.ui.plainTextEdit_2.toPlainText())
            
            # Mã hóa văn bản
            ciphertext = self.cipher.encrypt(plaintext, key)
            
            # Hiển thị kết quả
            self.ui.plainTextEdit_3.setPlainText(ciphertext)
            
        except ValueError:
            QtWidgets.QMessageBox.warning(
                self,
                "Lỗi",
                "Vui lòng nhập khóa là một số nguyên!"
            )
    
    def decrypt_text(self):
        """Xử lý sự kiện khi nhấn nút Decrypt"""
        try:
            # Lấy văn bản và khóa từ giao diện
            ciphertext = self.ui.plainTextEdit_3.toPlainText()  # Lấy từ ô ciphertext
            key = int(self.ui.plainTextEdit_2.toPlainText())
            
            # Giải mã văn bản
            plaintext = self.cipher.decrypt(ciphertext, key)
            
            # Hiển thị kết quả vào ô plaintext
            self.ui.plainTextEdit.setPlainText(plaintext)
            
        except ValueError:
            QtWidgets.QMessageBox.warning(
                self,
                "Lỗi",
                "Vui lòng nhập khóa là một số nguyên!"
            )

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = CaesarCipherApp()
    window.show()
    sys.exit(app.exec_()) 