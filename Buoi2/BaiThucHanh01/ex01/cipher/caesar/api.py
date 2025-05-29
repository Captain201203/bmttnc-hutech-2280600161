from flask import Blueprint, render_template, request
from .caesar_cipher import CaesarCipher

caesar_bp = Blueprint('caesar', __name__, template_folder='templates')

@caesar_bp.route('/caesar', methods=['GET'])
def caesar():
    return render_template('caesar.html')

@caesar_bp.route('/caesar/encrypt', methods=['POST'])
def caesar_encrypt():
    text = request.form['inputPlaintext']
    key = int(request.form['inputKeyPlain'])
    Caesar = CaesarCipher()
    encrypt_text = Caesar.encrypt(text, key)
    return f"text: {text}, key: {key}, encrypted text: {encrypt_text}"

@caesar_bp.route('/caesar/decrypt', methods=['POST'])
def caesar_decrypt():
    text = request.form['inputCiphertext']
    key = int(request.form['inputKeyCipher'])
    Caesar = CaesarCipher()
    decrypt_text = Caesar.decrypt(text, key)
    return f"text: {text}, key: {key}, decrypted text: {decrypt_text}" 