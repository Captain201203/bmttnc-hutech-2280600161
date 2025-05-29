from flask import Blueprint, render_template, request, jsonify
from .rsa_cipher import RSACipher, generate_keypair

rsa_bp = Blueprint('rsa', __name__, template_folder='templates')

@rsa_bp.route('/rsa', methods=['GET'])
def rsa_page():
    return render_template('rsa.html')

@rsa_bp.route('/rsa/generate_keys', methods=['POST'])
def generate_rsa_keys():
    try:
        p = int(request.form['inputPrimeP'])
        q = int(request.form['inputPrimeQ'])
        
        # Generate keypair using the function from rsa_cipher.py
        keys = generate_keypair(p, q)
        
        # Check if generate_keypair returned an error message
        if isinstance(keys, tuple) and len(keys) == 3 and keys[1] is None:
             error_message = keys[0]
             return jsonify({'error': error_message}), 400

        public_key, private_key = keys
        
        return jsonify({
            'public_key': public_key,
            'private_key': private_key
        })
    except ValueError:
        return jsonify({'error': 'Invalid input. Please enter integer prime numbers.'}), 400
    except Exception as e:
         return jsonify({'error': f'An error occurred: {e}'}), 500

@rsa_bp.route('/rsa/encrypt', methods=['POST'])
def rsa_encrypt():
    try:
        plaintext = request.form['inputPlaintext']
        e = int(request.form['inputPublicE'])
        n = int(request.form['inputPublicN'])
        public_key = (e, n)
        
        rsa_cipher = RSACipher()
        ciphertext = rsa_cipher.encrypt(plaintext, public_key)
        
        # Return ciphertext as a list of integers
        return jsonify({'ciphertext': ciphertext})
        
    except ValueError:
        return jsonify({'error': 'Invalid input. Please ensure key values are integers.'}), 400
    except Exception as e:
        return jsonify({'error': f'An error occurred: {e}'}), 500

@rsa_bp.route('/rsa/decrypt', methods=['POST'])
def rsa_decrypt():
    try:
        # Expect ciphertext as a comma-separated string of integers
        ciphertext_str = request.form['inputCiphertext']
        # Convert string of integers to list of integers
        ciphertext = [int(x.strip()) for x in ciphertext_str.split(',') if x.strip()]
        
        d = int(request.form['inputPrivateD'])
        n = int(request.form['inputPrivateN'])
        private_key = (d, n)
        
        rsa_cipher = RSACipher()
        plaintext = rsa_cipher.decrypt(ciphertext, private_key)
        
        # Check if decryption returned an error message string
        if isinstance(plaintext, str) and ("Invalid private key" in plaintext or "Decryption failed" in plaintext or "Invalid ciphertext" in plaintext):
             return jsonify({'error': plaintext}), 400

        return jsonify({'plaintext': plaintext})
        
    except ValueError:
        return jsonify({'error': 'Invalid input. Please ensure key and ciphertext values are integers.'}), 400
    except Exception as e:
        return jsonify({'error': f'An error occurred: {e}'}), 500 