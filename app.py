from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField

app = Flask(__name__)

rMsg = "Hello from Server!"

@app.route('/', methods = ['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/response', methods = ['GET', 'POST'])
def res():  
    print('Request recieved!!')
    return render_template('response.html')

if __name__ == "__main__":
    app.run(debug = True)