import base64
import json
from dataclasses import dataclass
from datetime import datetime

from Crypto.Hash import SHA256
from Crypto.PublicKey import ECC
from Crypto.Signature import DSS
from flask import Flask, render_template, request

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'

DB = []


@dataclass
class CallbackItem:
    signature: str
    message: str
    datetime: datetime


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


@app.route('/callbacks', methods=('GET', 'POST'))
def callback():
    if request.method == 'POST':
        signature = request.headers.get("x-opendsr-signature")
        message = request.stream.read()
        message = message.decode("utf-8")

        print(signature)
        print(message)

        DB.append(CallbackItem(
            message=message,
            signature=signature,
            datetime=datetime.utcnow(),

        ))
        return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}

    return render_template('callbacks.html', request=request, database=reversed(DB))


if __name__ == '__main__':
    app.run()
