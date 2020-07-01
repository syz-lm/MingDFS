from flask import Flask, request
import hmac

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return hmac.request.get_data().decode()


app.run(port=18000)