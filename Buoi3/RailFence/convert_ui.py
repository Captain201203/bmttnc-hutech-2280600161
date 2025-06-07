import os
import sys
from PyQt5 import uic

# Chuyển đổi file UI thành file Python
with open('ui/railfence.ui', 'r', encoding='utf-8') as ui_file:
    with open('ui/railfence.py', 'w', encoding='utf-8') as py_file:
        uic.compileUi(ui_file, py_file)
print("Đã chuyển đổi thành công file railfence.ui thành railfence.py") 