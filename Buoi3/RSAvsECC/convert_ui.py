import os
import sys
from PyQt5 import uic

# Chuyển đổi file UI thành file Python
with open('ui/rsa_ecc.ui', 'r', encoding='utf-8') as ui_file:
    with open('ui/rsa_ecc.py', 'w', encoding='utf-8') as py_file:
        uic.compileUi(ui_file, py_file)
print("Đã chuyển đổi thành công file rsa_ecc.ui thành rsa_ecc.py") 