from Crypto.Hash import SHA3_256
import tkinter as tk
from tkinter import messagebox

def calculate_sha3():
    text = entry.get()
    if not text:
        messagebox.showwarning("Cảnh báo", "Vui lòng nhập chuỗi cần hash!")
        return
    sha3_hash = SHA3_256.new()
    sha3_hash.update(text.encode('utf-8'))
    result = sha3_hash.hexdigest()
    result_label.config(text=f"SHA3-256: {result}")

root = tk.Tk()
root.title("SHA3-256 Hash GUI")
root.geometry("600x200")

tk.Label(root, text="Nhập chuỗi cần hash:").pack(pady=10)
entry = tk.Entry(root, width=60)
entry.pack(pady=5)

tk.Button(root, text="Tính SHA3-256", command=calculate_sha3).pack(pady=10)
result_label = tk.Label(root, text="SHA3-256: ")
result_label.pack(pady=10)

root.mainloop()