from flask import Blueprint, render_template, request
from .transposition_cipher import TranspositionCipher

transposition_bp = Blueprint('transposition', __name__, template_folder='templates')

@transposition_bp.route('/transposition', methods=['GET'])
def transposition():
    return render_template('transposition.html')

@transposition_bp.route('/transposition/encrypt', methods=['POST'])
def transposition_encrypt():
    text = request.form['inputPlaintext']
    try:
        key = int(request.form['inputKeyPlain'])
    except ValueError:
        return "Invalid key. Key must be an integer."

    tc_cipher = TranspositionCipher()
    encrypted_text = tc_cipher.encrypt(text, key)
    return f"text: {text}, key: {key}, encrypted text: {encrypted_text}"

@transposition_bp.route('/transposition/decrypt', methods=['POST'])
def transposition_decrypt():
    text = request.form['inputCiphertext']
    try:
        key = int(request.form['inputKeyCipher'])
    except ValueError:
        return "Invalid key. Key must be an integer."

    tc_cipher = TranspositionCipher()
    decrypted_text = tc_cipher.decrypt(text, key)
    return f"text: {text}, key: {key}, decrypted text: {decrypted_text}"

# Các route /transposition/encrypt và /transposition/decrypt sẽ thêm sau 