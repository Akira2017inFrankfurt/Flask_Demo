from flask import Flask, make_response, redirect, abort

app = Flask(__name__)


@app.route('/')
def index():
    res = make_response('<h1>This document carries a cookie!</h1>')
    res.set_cookie('answer', '42')
    return res
    return redirect('google.com')


if __name__ == '__main__':
    app.run()
