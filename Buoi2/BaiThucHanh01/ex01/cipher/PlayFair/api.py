from flask import Blueprint, render_template, request
from .playfair_cipher import PlayfairCipher

playfair_bp = Blueprint('playfair', __name__, template_folder='templates')

@playfair_bp.route('/playfair', methods=['GET'])
def playfair():
    return render_template('playfair.html')

@playfair_bp.route('/playfair/encrypt', methods=['POST'])
def playfair_encrypt():
    text = request.form['inputPlaintext']
    key = request.form['inputKeyPlaintext']
    pf_cipher = PlayfairCipher()
    encrypted_text = pf_cipher.encrypt(text, key)
    return f"text: {text}, key: {key}, encrypted text: {encrypted_text}"

@playfair_bp.route('/playfair/decrypt', methods=['POST'])
def playfair_decrypt():
    text = request.form['inputCiphertext']
    key = request.form['inputKeyCiphertext']
    pf_cipher = PlayfairCipher()
    decrypted_text = pf_cipher.decrypt(text, key)
    return f"text: {text}, key: {key}, decrypted text: {decrypted_text}" 