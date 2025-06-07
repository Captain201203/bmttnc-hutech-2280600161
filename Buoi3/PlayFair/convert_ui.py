import os
import sys
from PyQt5 import uic

# Chuyển đổi file UI thành file Python
with open('ui/playfair.ui', 'r', encoding='utf-8') as ui_file:
    with open('ui/playfair.py', 'w', encoding='utf-8') as py_file:
        uic.compileUi(ui_file, py_file)
print("Đã chuyển đổi thành công file playfair.ui thành playfair.py") 