import streamlit as st
import base64
import hashlib
import time
from PIL import Image
import os

st.title('Mô phỏng các thuật toán mã hóa')

tabs = st.tabs(["Base64", "Blockchain", "Ẩn tin trong ảnh"])

with tabs[0]:
    st.header("Mã hóa/Giải mã Base64")
    st.write("Mô phỏng mã hóa và giải mã base64 cho chuỗi hoặc file.")

    input_string = st.text_input("Nhập thông tin cần mã hóa:")
    if st.button("Mã hóa và lưu vào data.txt"):
        if input_string:
            encoded_bytes = base64.b64encode(input_string.encode('utf-8'))
            encoded_string = encoded_bytes.decode('utf-8')
            with open('base64/data.txt', 'w') as file:
                file.write(encoded_string)
            st.success(f"Đã mã hóa và ghi vào base64/data.txt: {encoded_string}")
        else:
            st.warning("Vui lòng nhập thông tin để mã hóa.")

    if st.button("Giải mã từ data.txt"):
        try:
            with open('base64/data.txt', 'r') as file:
                encoded_string = file.read().strip()
            decoded_bytes = base64.b64decode(encoded_string)
            decoded_string = decoded_bytes.decode('utf-8')
            st.success(f"Thông tin đã giải mã: {decoded_string}")
        except Exception as e:
            st.error(f"Có lỗi xảy ra: {e}")

with tabs[1]:
    st.header("Blockchain")
    st.write("Mô phỏng tạo block, xem chuỗi block và kiểm tra tính hợp lệ của blockchain.")

    # Khởi tạo blockchain (dùng session_state để giữ blockchain khi reload)
    class Block:
        def __init__(self, index, previous_hash, timestamp, transactions, proof):
            self.index = index
            self.previous_hash = previous_hash
            self.timestamp = timestamp
            self.transactions = transactions
            self.proof = proof
            self.hash = self.calculate_hash()
        def calculate_hash(self):
            data = str(self.index) + str(self.previous_hash) + str(self.timestamp) + str(self.transactions) + str(self.proof)
            return hashlib.sha256(data.encode()).hexdigest()

    class Blockchain:
        def __init__(self):
            self.chain = []
            self.current_transactions = []
            self.create_block(proof=1, previous_hash='0')
        def create_block(self, proof, previous_hash):
            block = Block(len(self.chain) + 1, previous_hash, time.time(), self.current_transactions, proof)
            self.current_transactions = []
            self.chain.append(block)
            return block
        def get_previous_block(self):
            return self.chain[-1]
        def proof_of_work(self, previous_proof):
            new_proof = 1
            check_proof = False
            while not check_proof:
                hash_operation = hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest()
                if hash_operation[:4] == '0000':
                    check_proof = True
                else:
                    new_proof += 1
            return new_proof
        def add_transaction(self, sender, receiver, amount):
            self.current_transactions.append({'sender': sender, 'receiver': receiver, 'amount': amount})
            return self.get_previous_block().index + 1
        def is_chain_valid(self, chain):
            previous_block = chain[0]
            block_index = 1
            while block_index < len(chain):
                block = chain[block_index]
                if block.previous_hash != previous_block.hash:
                    return False
                previous_proof = previous_block.proof
                proof = block.proof
                hash_operation = hashlib.sha256(str(proof**2 - previous_proof**2).encode()).hexdigest()
                if hash_operation[:4] != '0000':
                    return False
                previous_block = block
                block_index += 1
            return True

    if 'blockchain' not in st.session_state:
        st.session_state.blockchain = Blockchain()

    st.subheader("Thêm giao dịch mới")
    sender = st.text_input("Người gửi", key="sender")
    receiver = st.text_input("Người nhận", key="receiver")
    amount = st.number_input("Số tiền", min_value=0.0, step=1.0, key="amount")
    if st.button("Thêm giao dịch"):
        if sender and receiver and amount > 0:
            st.session_state.blockchain.add_transaction(sender, receiver, amount)
            st.success("Đã thêm giao dịch vào block hiện tại.")
        else:
            st.warning("Vui lòng nhập đầy đủ thông tin giao dịch.")

    if st.button("Tạo block mới"):
        previous_block = st.session_state.blockchain.get_previous_block()
        previous_proof = previous_block.proof
        proof = st.session_state.blockchain.proof_of_work(previous_proof)
        previous_hash = previous_block.hash
        block = st.session_state.blockchain.create_block(proof, previous_hash)
        st.success(f"Đã tạo block mới với index {block.index}.")

    st.subheader("Chuỗi blockchain hiện tại")
    for block in st.session_state.blockchain.chain:
        st.json({
            'index': block.index,
            'previous_hash': block.previous_hash,
            'timestamp': block.timestamp,
            'transactions': block.transactions,
            'proof': block.proof,
            'hash': block.hash
        })

    if st.button("Kiểm tra tính hợp lệ của blockchain"):
        if st.session_state.blockchain.is_chain_valid(st.session_state.blockchain.chain):
            st.success("Blockchain hợp lệ!")
        else:
            st.error("Blockchain không hợp lệ!")

with tabs[2]:
    st.header("Ẩn tin trong ảnh")
    st.write("Mô phỏng mã hóa và giải mã thông điệp ẩn trong ảnh.")

    def encode_image(image_path, message):
        img = Image.open(image_path)
        width, height = img.size
        binary_message = ''.join([format(ord(char), '08b') for char in message])
        binary_message += '1111111111111110'  # Đánh dấu kết thúc thông điệp
        data_index = 0
        for row in range(height):
            for col in range(width):
                pixel = list(img.getpixel((col, row)))
                for color_channel in range(3):
                    if data_index < len(binary_message):
                        pixel[color_channel] = int(format(pixel[color_channel], '08b')[:-1] + binary_message[data_index], 2)
                        data_index += 1
                img.putpixel((col, row), tuple(pixel))
                if data_index >= len(binary_message):
                    break
            if data_index >= len(binary_message):
                break
        encoded_image_path = "img-hidden/encoded_image.png"
        img.save(encoded_image_path)
        return encoded_image_path

    def decode_image(encoded_image_path):
        img = Image.open(encoded_image_path)
        width, height = img.size
        binary_message = ''
        for row in range(height):
            for col in range(width):
                pixel = img.getpixel((col, row))
                for color_channel in range(3):
                    binary_message += format(pixel[color_channel], '08b')[-1]
        # Tìm vị trí kết thúc thông điệp
        end_marker = '1111111111111110'
        end_idx = binary_message.find(end_marker)
        if end_idx != -1:
            binary_message = binary_message[:end_idx]
        message = ''
        for i in range(0, len(binary_message), 8):
            byte = binary_message[i:i+8]
            if len(byte) == 8:
                message += chr(int(byte, 2))
        return message

    st.subheader("Mã hóa thông điệp vào ảnh")
    message = st.text_input("Nhập thông điệp cần ẩn:")
    if st.button("Mã hóa vào ảnh gốc (image.jpg)"):
        if message:
            image_path = "img-hidden/image.jpg"
            if os.path.exists(image_path):
                encoded_path = encode_image(image_path, message)
                st.success(f"Đã mã hóa và lưu ảnh tại {encoded_path}")
                st.image(encoded_path, caption="Ảnh đã mã hóa")
            else:
                st.error("Không tìm thấy ảnh gốc img-hidden/image.jpg")
        else:
            st.warning("Vui lòng nhập thông điệp để mã hóa.")

    st.subheader("Giải mã thông điệp từ ảnh đã mã hóa")
    if st.button("Giải mã từ encoded_image.png"):
        encoded_path = "img-hidden/encoded_image.png"
        if os.path.exists(encoded_path):
            message = decode_image(encoded_path)
            st.success(f"Thông điệp đã giải mã: {message}")
            st.image(encoded_path, caption="Ảnh đã mã hóa")
        else:
            st.error("Không tìm thấy ảnh đã mã hóa img-hidden/encoded_image.png") 