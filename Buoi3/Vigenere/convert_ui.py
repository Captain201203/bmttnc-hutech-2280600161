import os
import sys
from PyQt5 import uic

# Chuyển đổi file UI thành file Python
with open('ui/vigenere.ui', 'r', encoding='utf-8') as ui_file:
    with open('ui/vigenere.py', 'w', encoding='utf-8') as py_file:
        uic.compileUi(ui_file, py_file)
print("Đã chuyển đổi thành công file vigenere.ui thành vigenere.py") 