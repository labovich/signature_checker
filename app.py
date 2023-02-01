import base64

from Crypto.Hash import SHA256
from Crypto.PublicKey import ECC
from Crypto.Signature import DSS
from flask import Flask, render_template, request, flash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'


@app.route('/', methods=('GET', 'POST'))
def create():
    success = False

    if request.method == 'POST':
        raw_certificate = request.form['certificate']
        raw_signature = request.form['signature']
        raw_message = request.form['message']

        certificate = raw_certificate.strip()
        message = raw_message.strip()
        message = message.encode("utf-8")
        signature = raw_signature.strip()
        signature = base64.b64decode(signature.encode("utf-8"))

        print(certificate)
        print(message)
        print(signature)

        key = ECC.import_key(certificate)
        h = SHA256.new(message)
        verifier = DSS.new(key, "fips-186-3")
        try:
            verifier.verify(h, signature)
            success = True
        except:
            pass

    return render_template('index.html', request=request, success=success)

if __name__ == '__main__':
    app.run()
