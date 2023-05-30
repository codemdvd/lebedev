from flask import Flask, session, redirect, render_template, url_for, request

app = Flask(__name__)

@app.route('/')
def auth():
     return render_template('auth.html')




if __name__ == '__main__':
    app.run()