from flask import Flask, request
import hmac

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    print(type(request.get_data()))
    return '1'


app.run(port=18000)