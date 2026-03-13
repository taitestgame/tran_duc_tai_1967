from flask import Flask, render_template, request
from cipher.caesar import CaesarCipher
from cipher.vigenere import VigenereCipher
from cipher.playfair import PlayFairCipher 
from cipher.railfence import RailFenceCipher
from cipher.transposition import TranspositionCipher

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

# --- CAESAR ---
@app.route("/caesar")
def caesar():
    return render_template("caesar.html")

@app.route("/caesar/encrypt", methods=["POST"])
def caesar_encrypt():
    text = request.form.get("inputPlainText")
    key = int(request.form.get("inputKeyPlain"))
    Caesar = CaesarCipher()
    encrypted_text = Caesar.encrypt_text(text, key)
    return render_template("caesar.html", outputCipher=encrypted_text)

@app.route("/caesar/decrypt", methods=["POST"])
def caesar_decrypt():
    text = request.form.get("inputCipherText")
    key = int(request.form.get("inputKeyCipher"))
    Caesar = CaesarCipher()
    decrypted_text = Caesar.decrypt_text(text, key)
    return render_template("caesar.html", outputPlain=decrypted_text)

# --- VIGENERE ---
@app.route("/vigenere")
def vigenere_page():
    return render_template('vigenere.html')

@app.route("/vigenere/encrypt", methods=['POST'])
def vigenere_encrypt():
    text = request.form.get('inputPlainText')
    key = request.form.get('inputKeyPlain')
    if text and key:
        cipher = VigenereCipher()
        result = cipher.vigenere_encrypt(text, key) 
        return render_template('vigenere.html', outputCipher=result)
    return render_template('vigenere.html')

@app.route("/vigenere/decrypt", methods=['POST'])
def vigenere_decrypt():
    text = request.form.get('inputCipherText')
    key = request.form.get('inputKeyCipher')
    if text and key:
        cipher = VigenereCipher()
        result = cipher.vigenere_decrypt(text, key)
        return render_template('vigenere.html', outputPlain=result)
    return render_template('vigenere.html')

# --- PLAYFAIR ---
@app.route("/playfair")
def playfair_page():
    return render_template('playfair.html')

@app.route("/playfair/encrypt", methods=['POST'])
def playfair_encrypt():
    text = request.form.get('inputPlainText')
    key = request.form.get('inputKeyPlain')
    if text and key:
        cipher = PlayFairCipher() 
        matrix = cipher.create_playfair_matrix(key)
        result = cipher.playfair_encrypt(text, matrix)
        return render_template('playfair.html', outputCipher=result)
    return render_template('playfair.html')

@app.route("/playfair/decrypt", methods=['POST'])
def playfair_decrypt():
    text = request.form.get('inputCipherText')
    key = request.form.get('inputKeyCipher')
    if text and key:
        cipher = PlayFairCipher()
        matrix = cipher.create_playfair_matrix(key)
        result = cipher.playfair_decrypt(text, matrix)
        return render_template('playfair.html', outputPlain=result)
    return render_template('playfair.html')


@app.route("/railfence")
def railfence_page():
    return render_template('railfence.html')

@app.route("/railfence/encrypt", methods=['POST'])
def railfence_encrypt():
    text = request.form.get('inputPlainText')
    key_str = request.form.get('inputKeyPlain')
    if text and key_str:
        key = int(key_str)
        cipher = RailFenceCipher()

        result = cipher.rail_fence_encrypt(text, key) 
        return render_template('railfence.html', outputCipher=result)
    return render_template('railfence.html')

@app.route("/railfence/decrypt", methods=['POST'])
def railfence_decrypt():
    text = request.form.get('inputCipherText')
    key_str = request.form.get('inputKeyCipher')
    if text and key_str:
        key = int(key_str)
        cipher = RailFenceCipher()
        result = cipher.rail_fence_decrypt(text, key)
        return render_template('railfence.html', outputPlain=result)
    return render_template('railfence.html')


@app.route("/transposition")
def transposition_page():
    return render_template('transposition.html')

@app.route("/transposition/encrypt", methods=['POST'])
def transposition_encrypt():
    text = request.form.get('inputPlainText')
    key_str = request.form.get('inputKeyPlain')
    
    if text and key_str:
        key = int(key_str) 
        cipher = TranspositionCipher()
       
        result = cipher.encrypt(text, key)
        return render_template('transposition.html', outputCipher=result)
    return render_template('transposition.html')

@app.route("/transposition/decrypt", methods=['POST'])
def transposition_decrypt():
    text = request.form.get('inputCipherText')
    key_str = request.form.get('inputKeyCipher')
    
    if text and key_str:
        key = int(key_str)
        cipher = TranspositionCipher()
       
        result = cipher.decrypt(text, key)
        return render_template('transposition.html', outputPlain=result)
    return render_template('transposition.html')

if __name__ == "__main__":
    app.run(debug=True)