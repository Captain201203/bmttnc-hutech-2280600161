import sys
from PyQt5 import QtWidgets
from ui.railfence import Ui_Form
from platform.railfence_cipher import RailFenceCipher

class RailFenceApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.cipher = RailFenceCipher()
        
        self.ui.pushButton.clicked.connect(self.encrypt_text)
        self.ui.pushButton_2.clicked.connect(self.decrypt_text)
        self.setWindowTitle("Rail Fence Cipher")

    def encrypt_text(self):
        try:
            plaintext = self.ui.plainTextEdit.toPlainText()
            num_rail = self.ui.lineEdit.text().strip()
            if not plaintext:
                raise ValueError("Vui lòng nhập văn bản cần mã hóa")
            if not num_rail.isdigit() or int(num_rail) < 2:
                raise ValueError("Số lượng rail phải là số nguyên >= 2")
            ciphertext = self.cipher.encrypt(plaintext, int(num_rail))
            self.ui.plainTextEdit_2.setPlainText(ciphertext)
        except Exception as e:
            QtWidgets.QMessageBox.warning(self, "Lỗi", f"Không thể mã hóa: {str(e)}")

    def decrypt_text(self):
        try:
            ciphertext = self.ui.plainTextEdit_2.toPlainText()
            num_rail = self.ui.lineEdit.text().strip()
            if not ciphertext:
                raise ValueError("Vui lòng nhập văn bản cần giải mã")
            if not num_rail.isdigit() or int(num_rail) < 2:
                raise ValueError("Số lượng rail phải là số nguyên >= 2")
            plaintext = self.cipher.decrypt(ciphertext, int(num_rail))
            self.ui.plainTextEdit.setPlainText(plaintext)
        except Exception as e:
            QtWidgets.QMessageBox.warning(self, "Lỗi", f"Không thể giải mã: {str(e)}")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = RailFenceApp()
    window.show()
    sys.exit(app.exec_()) 