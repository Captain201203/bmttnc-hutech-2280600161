from flask import Blueprint, render_template, request
from .vigenere_cipher import VigenereCipher

vigenere_bp = Blueprint('vigenere', __name__, template_folder='templates')

@vigenere_bp.route('/vigenere', methods=['GET'])
def vigenere():
    return render_template('vigenere.html')

@vigenere_bp.route('/vigenere/encrypt', methods=['POST'])
def vigenere_encrypt():
    text = request.form['inputPlaintext']
    key = request.form['inputKeyPlaintext']
    Vigenere = VigenereCipher()
    encrypt_text = Vigenere.encrypt(text, key)
    return f"text: {text}, key: {key}, encrypted text: {encrypt_text}"

@vigenere_bp.route('/vigenere/decrypt', methods=['POST'])
def vigenere_decrypt():
    text = request.form['inputCiphertext']
    key = request.form['inputKeyCiphertext']
    Vigenere = VigenereCipher()
    decrypt_text = Vigenere.decrypt(text, key)
    return f"text: {text}, key: {key}, decrypted text: {decrypt_text}"
