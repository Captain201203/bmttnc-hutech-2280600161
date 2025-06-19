import hashlib
import tkinter as tk
from tkinter import messagebox

def calculate_sha256():
    text = entry.get()
    if not text:
        messagebox.showwarning("Cảnh báo", "Vui lòng nhập chuỗi cần hash!")
        return
    sha256_hash = hashlib.sha256()
    sha256_hash.update(text.encode('utf-8'))
    result = sha256_hash.hexdigest()
    result_label.config(text=f"SHA-256: {result}")

root = tk.Tk()
root.title("SHA-256 Hash GUI")
root.geometry("600x200")

tk.Label(root, text="Nhập chuỗi cần hash:").pack(pady=10)
entry = tk.Entry(root, width=60)
entry.pack(pady=5)

tk.Button(root, text="Tính SHA-256", command=calculate_sha256).pack(pady=10)
result_label = tk.Label(root, text="SHA-256: ")
result_label.pack(pady=10)

root.mainloop()