import sys
from PyQt5 import QtWidgets
from ui.playfair import Ui_Form
from platform.playfair_cipher import PlayfairCipher

class PlayfairApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.cipher = PlayfairCipher()
        
        self.ui.pushButton.clicked.connect(self.encrypt_text)
        self.ui.pushButton_2.clicked.connect(self.decrypt_text)
        self.setWindowTitle("Playfair Cipher")

    def encrypt_text(self):
        try:
            plaintext = self.ui.plainTextEdit.toPlainText()
            key = self.ui.lineEdit.text().strip()
            if not plaintext:
                raise ValueError("Vui lòng nhập văn bản cần mã hóa")
            if not key:
                raise ValueError("Vui lòng nhập khóa mã hóa")
            ciphertext = self.cipher.encrypt(plaintext, key)
            self.ui.plainTextEdit_2.setPlainText(ciphertext)
        except Exception as e:
            QtWidgets.QMessageBox.warning(self, "Lỗi", f"Không thể mã hóa: {str(e)}")

    def decrypt_text(self):
        try:
            ciphertext = self.ui.plainTextEdit_2.toPlainText()
            key = self.ui.lineEdit.text().strip()
            if not ciphertext:
                raise ValueError("Vui lòng nhập văn bản cần giải mã")
            if not key:
                raise ValueError("Vui lòng nhập khóa giải mã")
            plaintext = self.cipher.decrypt(ciphertext, key)
            self.ui.plainTextEdit.setPlainText(plaintext)
        except Exception as e:
            QtWidgets.QMessageBox.warning(self, "Lỗi", f"Không thể giải mã: {str(e)}")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = PlayfairApp()
    window.show()
    sys.exit(app.exec_()) 