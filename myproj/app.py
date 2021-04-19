from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from time import time
import re
app = Flask(__name__)

rMsg = "Hello from Server!"
arr = ['']
pattern = r",(?=(?:[^\"]*\"[^\"]*\")*[^\"]*$)"

@app.route('/')
def index():
#   menu= {'a','b','c','d'}
    return render_template('index.html')#, menu=menu)
start = time()
@app.route('/', methods = ['POST'])
def key_Search():
    word = request.form['w']
    arr=[]
    f = open(r'E:\CS180\Web\csv\listings.csv','r',encoding='utf-8')
    title = (f.readline().replace("\n",'').split(','))
    num_title = range(len(title))
    for value in f:
        if word in value:
            arr.append(re.split(pattern,value.replace("\n"," ")))
    f.close()
    if not arr:
        num_list = 0
    else:
        num_list = range(len(arr[0]))
    num_total = range(min(len(arr),40))
    return render_template('searching.html', word=word, title=title,
    num_title=num_title, arr=arr, num_list=num_list, num_total=num_total)

if __name__ == "__main__":
    app.run(debug=True)
