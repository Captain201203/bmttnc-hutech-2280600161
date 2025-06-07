import sys
from PyQt5 import QtWidgets
from ui.ecc import Ui_Form
from platform.ecc_cipher import ECCCipher

class ECCApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.cipher = ECCCipher()
        
        # Kết nối các nút với hàm xử lý
        self.ui.pushButton_3.clicked.connect(self.generate_key)  # generate key
        self.ui.pushButton.clicked.connect(self.sign_text)       # Sign
        self.ui.pushButton_2.clicked.connect(self.verify_signature)  # Verify
        
        # Đặt tiêu đề cho cửa sổ
        self.setWindowTitle("ECC Cipher")
        
    def generate_key(self):
        """Xử lý sự kiện khi nhấn nút generate key"""
        try:
            # Tạo cặp khóa mới
            private_key, public_key = self.cipher.generate_key()
            
            # Hiển thị thông tin khóa
            key_info = f"Private Key: {private_key}\n"
            key_info += f"Public Key: {public_key}"
            self.ui.plainTextEdit.setPlainText(key_info)
            
        except Exception as e:
            QtWidgets.QMessageBox.warning(
                self,
                "Lỗi",
                f"Không thể tạo khóa: {str(e)}"
            )
    
    def sign_text(self):
        """Xử lý sự kiện khi nhấn nút Sign"""
        try:
            # Lấy văn bản cần ký từ ô Information
            message = self.ui.plainTextEdit.toPlainText()
            if not message:
                raise ValueError("Vui lòng nhập văn bản cần ký")
                
            # Tạo chữ ký
            signature = self.cipher.sign(message)
            
            # Hiển thị chữ ký
            signature_str = f"r: {signature[0]}\ns: {signature[1]}"
            self.ui.plainTextEdit_2.setPlainText(signature_str)
            
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
            signature_str = self.ui.plainTextEdit_2.toPlainText()
            
            if not message or not signature_str:
                raise ValueError("Vui lòng nhập đầy đủ văn bản và chữ ký")
            
            # Phân tích chữ ký từ chuỗi
            try:
                r_str, s_str = signature_str.split('\n')
                r = int(r_str.split(': ')[1])
                s = int(s_str.split(': ')[1])
                signature = (r, s)
            except:
                raise ValueError("Định dạng chữ ký không hợp lệ")
                
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
    window = ECCApp()
    window.show()
    sys.exit(app.exec_()) 