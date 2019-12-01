from flask import Flask, request
app = Flask(__name__)

@app.route('/')
def test():
    name = request.args.get('name')
    return 'Hello, ' + name + '!'
