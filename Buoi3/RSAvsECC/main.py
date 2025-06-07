import sys
from PyQt5 import QtWidgets
from ui.rsa_ecc import Ui_Form
from platform.rsa_ecc import RSACipher, ECCCipher

class RSAvsECCApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.rsa = RSACipher()
        self.ecc = ECCCipher()
        self.rsa_private = ''
        self.rsa_public = ''
        self.ecc_private = ''
        self.ecc_public = ''
        
        self.ui.pushButton.clicked.connect(self.generate_key_rsa)
        self.ui.pushButton_2.clicked.connect(self.generate_key_ecc)
        self.ui.pushButton_3.clicked.connect(self.sign_rsa)
        self.ui.pushButton_4.clicked.connect(self.sign_ecc)
        self.ui.pushButton_5.clicked.connect(self.verify_rsa)
        self.ui.pushButton_6.clicked.connect(self.verify_ecc)
        self.setWindowTitle("RSA vs ECC Digital Signature")

    def generate_key_rsa(self):
        priv, pub = self.rsa.generate_key()
        self.rsa_private = priv
        self.rsa_public = pub
        self.ui.lineEdit.setText(pub)
        QtWidgets.QMessageBox.information(self, "RSA Key", "Đã sinh khóa RSA mới!")

    def generate_key_ecc(self):
        priv, pub = self.ecc.generate_key()
        self.ecc_private = priv
        self.ecc_public = pub
        self.ui.lineEdit_3.setText(pub)
        QtWidgets.QMessageBox.information(self, "ECC Key", "Đã sinh khóa ECC mới!")

    def sign_rsa(self):
        message = self.ui.plainTextEdit.toPlainText()
        if not self.rsa_private:
            QtWidgets.QMessageBox.warning(self, "Lỗi", "Chưa có khóa riêng RSA!")
            return
        if not message:
            QtWidgets.QMessageBox.warning(self, "Lỗi", "Vui lòng nhập văn bản cần ký!")
            return
        signature = self.rsa.sign(self.rsa_private, message)
        self.ui.lineEdit_2.setText(signature)
        QtWidgets.QMessageBox.information(self, "RSA Signature", "Đã ký số bằng RSA!")

    def sign_ecc(self):
        message = self.ui.plainTextEdit.toPlainText()
        if not self.ecc_private:
            QtWidgets.QMessageBox.warning(self, "Lỗi", "Chưa có khóa riêng ECC!")
            return
        if not message:
            QtWidgets.QMessageBox.warning(self, "Lỗi", "Vui lòng nhập văn bản cần ký!")
            return
        signature = self.ecc.sign(self.ecc_private, message)
        self.ui.lineEdit_4.setText(signature)
        QtWidgets.QMessageBox.information(self, "ECC Signature", "Đã ký số bằng ECC!")

    def verify_rsa(self):
        message = self.ui.plainTextEdit.toPlainText()
        signature = self.ui.lineEdit_2.text().strip()
        pub = self.ui.lineEdit.text().strip()
        if not pub or not signature or not message:
            QtWidgets.QMessageBox.warning(self, "Lỗi", "Vui lòng nhập đủ khóa công khai, chữ ký và văn bản!")
            return
        result = self.rsa.verify(pub, message, signature)
        if result:
            QtWidgets.QMessageBox.information(self, "RSA Verify", "Chữ ký hợp lệ!")
        else:
            QtWidgets.QMessageBox.warning(self, "RSA Verify", "Chữ ký KHÔNG hợp lệ!")

    def verify_ecc(self):
        message = self.ui.plainTextEdit.toPlainText()
        signature = self.ui.lineEdit_4.text().strip()
        pub = self.ui.lineEdit_3.text().strip()
        if not pub or not signature or not message:
            QtWidgets.QMessageBox.warning(self, "Lỗi", "Vui lòng nhập đủ khóa công khai, chữ ký và văn bản!")
            return
        result = self.ecc.verify(pub, message, signature)
        if result:
            QtWidgets.QMessageBox.information(self, "ECC Verify", "Chữ ký hợp lệ!")
        else:
            QtWidgets.QMessageBox.warning(self, "ECC Verify", "Chữ ký KHÔNG hợp lệ!")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = RSAvsECCApp()
    window.show()
    sys.exit(app.exec_()) 