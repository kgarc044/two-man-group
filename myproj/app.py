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
# files = {'calendar' : read_json(r'E:\CS180\Web\myproj\data\calendar.json'),\
#     'listings' : read_json(r'E:\CS180\Web\myproj\data\listings.json'),\
#     'neighbourhoods' : read_json(r'E:\CS180\Web\myproj\data\neighbourhoods.json'),\
#     'reviews' : read_json(r'E:\CS180\Web\myproj\data\reviews.json')}

files = {'listings' : read_json(r'data/listings.json'),\
    'neighbourhoods' : read_json(r'data/neighbourhoods.json'),\
    'reviews' : read_json(r'data/reviews.json')}

#listings_detailed = read_json('data/listings_detailed.json')
#reviews_detailed = read_json('data/reviews_detailed.json')

@app.route('/')
def index():
    f_name_list = files.keys()
    session.clear()
    return render_template('searching.html',f_name_list=f_name_list)#, menu=menu)
@app.route('/update', methods =['POST'])
def update():
    f_name_list = files.keys()
    arr = []
    file = request.form['fname']
    session['file'] = file
    title = list(files[file][0].keys()) # get keys from first entry
    num_title = range(len(title))
    # for entry in files[file]:#[file]:
    #     arr.append(list(entry.values()))
    for i in range(len(files[file])):
        arr.append((list(files[file][i].values()), i))
    if not arr:
        num_list = 0
    else:
        num_list = range(len(arr[0][0]))
    num_total = range(min(len(arr),40))
    arr2 = []
    for i in num_total:
        arr2.append(arr[i])
    session['arr'] = arr2
    if len(arr) == 0:
        session['num_list'] = 0
    else:
        session['num_list'] = len(arr[0][0])
    session['num_total'] = min(len(arr), 40)
    # session.clear()
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

    print(word)

    for i in range(len(files[file])):
        if word in files[file][i][select]:
            arr.append((list(files[file][i].values()), i))

    # print(arr[0])

    # for entry in files[file]:
    #     if word in entry[select]:
    #         arr.append(list(entry.values()))
    if len(arr) == 0:
        num_list = 0
    else:
        num_list = range(len(arr[0][0]))
    num_total = range(min(len(arr),40))
    arr2 = []
    for i in num_total:
        arr2.append(arr[i])
    session['arr'] = arr2
    if len(arr) == 0:
        session['num_list'] = 0
    else:
        session['num_list'] = len(arr[0][0])
    session['num_total'] = min(len(arr), 40)
    return render_template('searching.html',f_name_list=f_name_list, file=file, select= select,
         word=word, title=title, num_title=num_title, arr=arr, num_list=num_list, num_total=num_total)   

@app.route('/del', methods = ['POST'])
def delfunc():
    f_name_list = files.keys()
    arr = session.get('arr', None)
    file = session.get('file', None)
    num_list = range(session.get('num_list', None))
    num_total = range(session.get('num_total', None) - 1)
    title = list(files[file][0].keys())
    num_title = range(len(title))

    index = request.values['delete_row']

    index = index.replace('(', '')
    index = index.replace(')', '')
    test = index.split(', ')


    print(files[file][int(test[0])])
    print(arr[int(test[1])])

    for i in range(int(test[1]),session.get('num_total', None)):
        arr[i] = (arr[i][0], int(arr[i][1]) - 1)

    del files[file][int(test[0])]
    del arr[int(test[1])]

    session['num_total'] = session.get('num_total', None) - 1
    

    return render_template('searching.html', f_name_list = f_name_list, file=file, arr=arr,
        title=title, num_title=num_title, num_list=num_list, num_total=num_total, index=index)

@app.route('/edit', methods = ['POST'])
def edit():
    f_name_list = files.keys()
    arr = session.get('arr', None)
    file = session.get('file', None)
    num_list = range(session.get('num_list', None))
    num_total = range(session.get('num_total', None) - 1)
    title = list(files[file][0].keys())
    num_title = range(len(title))

    index = request.values['edit_row']

    index = index.replace('(', '')
    index = index.replace(')', '')
    test = index.split(', ')

    print(test)

    return render_template('searching.html', f_name_list = f_name_list, file=file, arr=arr,
        title=title, num_title=num_title, num_list=num_list, num_total=num_total, index=index)

@app.route('/export', methods = ['POST'])
def export():
    f_name_list = files.keys()
    for file in f_name_list
        dict_to_json(file, 'data/' + file + '.json')
    return render_template('searching.html', f_name_list=f_name_list)



if __name__ == "__main__":
    app.run(debug=True)
