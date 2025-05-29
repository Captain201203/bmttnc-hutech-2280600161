from flask import Blueprint, render_template, request
from .rail_fence_cipher import RailFenceCipher

railfence_bp = Blueprint('railfence', __name__, template_folder='templates')

@railfence_bp.route('/railfence', methods=['GET'])
def railfence():
    return render_template('rail_fence.html')

@railfence_bp.route('/railfence/encrypt', methods=['POST'])
def railfence_encrypt():
    text = request.form['inputPlaintext']
    key = int(request.form['inputKeyPlain'])
    rf_cipher = RailFenceCipher()
    encrypted_text = rf_cipher.encrypt(text, key)
    return f"text: {text}, key: {key}, encrypted text: {encrypted_text}"

@railfence_bp.route('/railfence/decrypt', methods=['POST'])
def railfence_decrypt():
    text = request.form['inputCiphertext']
    key = int(request.form['inputKeyCipher'])
    rf_cipher = RailFenceCipher()
    decrypted_text = rf_cipher.decrypt(text, key)
    return f"text: {text}, key: {key}, decrypted text: {decrypted_text}" 