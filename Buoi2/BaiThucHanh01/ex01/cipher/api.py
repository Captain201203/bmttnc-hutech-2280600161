from flask import Flask, render_template
from caesar.api import caesar_bp
from Vigenere.api import vigenere_bp
from RailFence.api import railfence_bp
from PlayFair.api import playfair_bp as playfair_blueprint
from Transposition.api import transposition_bp
from RSA.api import rsa_bp

app = Flask(__name__, template_folder='templates')

# Đăng ký blueprint
app.register_blueprint(caesar_bp)
app.register_blueprint(vigenere_bp)
app.register_blueprint(railfence_bp)
app.register_blueprint(playfair_blueprint)
app.register_blueprint(transposition_bp)
app.register_blueprint(rsa_bp)

@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5050, debug=True)

   