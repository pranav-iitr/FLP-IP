from flask import Flask

app = Flask(__name__)

print("hi")

@app.route('/')
def hello():
    return '<h1>Hello, World!</h1>'