import hashlib
import tkinter as tk
from tkinter import scrolledtext, messagebox, filedialog

class HashApp:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Ứng dụng Hash")
        self.window.geometry("800x600")
        
        # Tạo giao diện
        self.create_widgets()
        
    def create_widgets(self):
        # Frame chính
        main_frame = tk.Frame(self.window)
        main_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        
        # Frame nhập liệu
        input_frame = tk.Frame(main_frame)
        input_frame.pack(padx=5, pady=5, fill=tk.X)
        
        # Label và Entry cho text
        tk.Label(input_frame, text="Nhập text:").pack(side=tk.LEFT, padx=5)
        self.text_entry = tk.Entry(input_frame)
        self.text_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        # Nút chọn file
        file_button = tk.Button(input_frame, text="Chọn File", command=self.select_file)
        file_button.pack(side=tk.LEFT, padx=5)
        
        # Frame chọn thuật toán
        algo_frame = tk.Frame(main_frame)
        algo_frame.pack(padx=5, pady=5, fill=tk.X)
        
        # Radio buttons cho các thuật toán
        self.algo_var = tk.StringVar(value="md5")
        algorithms = [
            ("MD5", "md5"),
            ("SHA-256", "sha256"),
            ("SHA-3", "sha3_256"),
            ("BLAKE2", "blake2b")
        ]
        
        for text, value in algorithms:
            tk.Radiobutton(algo_frame, text=text, value=value, 
                          variable=self.algo_var).pack(side=tk.LEFT, padx=5)
        
        # Nút tính hash
        hash_button = tk.Button(algo_frame, text="Tính Hash", command=self.calculate_hash)
        hash_button.pack(side=tk.RIGHT, padx=5)
        
        # Khu vực hiển thị kết quả
        result_frame = tk.Frame(main_frame)
        result_frame.pack(padx=5, pady=5, fill=tk.BOTH, expand=True)
        
        tk.Label(result_frame, text="Kết quả:").pack(anchor=tk.W)
        self.result_area = scrolledtext.ScrolledText(result_frame, wrap=tk.WORD, height=10)
        self.result_area.pack(padx=5, pady=5, fill=tk.BOTH, expand=True)
        self.result_area.config(state=tk.DISABLED)
        
    def select_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.text_entry.delete(0, tk.END)
            self.text_entry.insert(0, file_path)
            
    def calculate_hash(self):
        text = self.text_entry.get()
        if not text:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập text hoặc chọn file!")
            return
            
        try:
            # Lấy thuật toán được chọn
            algo = self.algo_var.get()
            
            # Tính hash
            if algo == "md5":
                hash_obj = hashlib.md5()
            elif algo == "sha256":
                hash_obj = hashlib.sha256()
            elif algo == "sha3_256":
                hash_obj = hashlib.sha3_256()
            elif algo == "blake2b":
                hash_obj = hashlib.blake2b()
                
            # Nếu là file
            if text.endswith(('.txt', '.pdf', '.doc', '.docx', '.jpg', '.png')):
                with open(text, 'rb') as f:
                    for chunk in iter(lambda: f.read(4096), b''):
                        hash_obj.update(chunk)
            else:
                hash_obj.update(text.encode())
                
            # Hiển thị kết quả
            result = hash_obj.hexdigest()
            self.result_area.config(state=tk.NORMAL)
            self.result_area.delete(1.0, tk.END)
            self.result_area.insert(tk.END, f"Thuật toán: {algo.upper()}\n")
            self.result_area.insert(tk.END, f"Input: {text}\n")
            self.result_area.insert(tk.END, f"Hash: {result}\n")
            self.result_area.config(state=tk.DISABLED)
            
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể tính hash: {str(e)}")
            
    def run(self):
        self.window.mainloop()
        
if __name__ == "__main__":
    app = HashApp()
    app.run()