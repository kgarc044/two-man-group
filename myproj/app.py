from flask import Flask, render_template, request, session
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from time import time
import re

from parse_json import read_json # Tristan's parse_json functions

app = Flask(__name__)
app.secret_key = 'super secret key'

rMsg = "Hello from Server!"
arr = ['']
pattern = r",(?=(?:[^\"]*\"[^\"]*\")*[^\"]*$)"

# load JSON files to dict of lists of dict; need to check if JSON or CSV is faster. CSV is smaller
files = {'calendar' : read_json(r'E:\CS180\Web\myproj\data\calendar.json'),\
    'listings' : read_json(r'E:\CS180\Web\myproj\data\listings.json'),\
    'neighbourhoods' : read_json(r'E:\CS180\Web\myproj\data\neighbourhoods.json'),\
    'reviews' : read_json(r'E:\CS180\Web\myproj\data\reviews.json')}

#listings_detailed = read_json('data/listings_detailed.json')
#reviews_detailed = read_json('data/reviews_detailed.json')

@app.route('/')
def index():
    f_name_list = files.keys()
    return render_template('searching.html',f_name_list=f_name_list)#, menu=menu)
@app.route('/update', methods =['POST'])
def update():
    f_name_list = files.keys()
    arr = []
    file = request.form['fname']
    session['file'] = file
    title = list(files[file][0].keys()) # get keys from first entry
    num_title = range(len(title))
    for entry in files[file]:#[file]:
        arr.append(list(entry.values()))
    if not arr:
        num_list = 0
    else:
        num_list = range(len(arr[0]))
    num_total = range(min(len(arr),40))
    return render_template('searching.html',f_name_list=f_name_list, file=file, 
        title=title, num_title=num_title, arr=arr, num_list=num_list, num_total=num_total)   
@app.route('/search', methods = ['POST'])
def key_Search():

    f_name_list = files.keys()
    arr=[]
    file = session.get('file',None)
    title = list(files[file][0].keys()) # get keys from first entry
    word = request.form['w']
    select = request.form['sel']

    num_title = range(len(title))
    print(num_title)
    for entry in files[file]:
        if word in entry[select]:
            arr.append(list(entry.values()))
    if not arr:
        num_list = 0
    else:
        num_list = range(len(arr[0]))
    num_total = range(min(len(arr),40))
    return render_template('searching.html',f_name_list=f_name_list, file=file, select= select,
         word=word, title=title, num_title=num_title, arr=arr, num_list=num_list, num_total=num_total)   


if __name__ == "__main__":
    app.run(debug=True)