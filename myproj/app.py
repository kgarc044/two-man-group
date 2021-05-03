from flask import Flask, render_template, request, session
#from flask_wtf import FlaskForm
#from wtforms import StringField, SubmitField
from time import time
import re
import glob
import os

import matplotlib.pyplot as plt
import numpy as np
from io import BytesIO
import base64

from parse_json import read_json # Tristan's parse_json functions
from parse_json import dict_to_json
from analyzer import a1

app = Flask(__name__)
app.secret_key = 'super secret key'

rMsg = "Hello from Server!"
arr = ['']
pattern = r",(?=(?:[^\"]*\"[^\"]*\")*[^\"]*$)"


# load JSON files to dict of lists of dict; need to check if JSON or CSV is faster. CSV is smaller
path = os.path.join(os.path.curdir, r'data')

cal = read_json(os.path.join(path, r'calendar.json'))
lst = read_json(os.path.join(path, r'listings.json'))
nhd = read_json(os.path.join(path, r'neighbourhoods.json'))
rev = read_json(os.path.join(path, r'reviews.json'))

files = {'calendar' : cal,\
    'listings' : lst,\
    'neighbourhoods' : nhd,\
    'reviews' : rev}


#file_name = []
#files = {}
#file_list = glob.glob('data\*.json')
#for f in file_list:
#    print(f)
#json_path = []
#for i in file_list:
#    json_path.append(i)
#for i in file_list:
#    file_name.append(re.findall('(?<=\\\\).*?(?=\.)',i))
#for x,i in enumerate(file_name):
#    files[i[0]] = read_json(json_path[x])

#listings_detailed = read_json('data/listings_detailed.json')
#reviews_detailed = read_json('data/reviews_detailed.json')


@app.route('/')
def index():
    f_name_list = files.keys()
    session.clear()
    return render_template('index.html',f_name_list=f_name_list, enumerate=enumerate)#, menu=menu)

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
        title=title, num_title=num_title, arr=arr, num_list=num_list, num_total=num_total, enumerate=enumerate) 

@app.route('/search', methods = ['POST'])
def key_Search():
    f_name_list = files.keys()
    arr=[]
    file = session.get('file',None)
    title = list(files[file][0].keys()) # get keys from first entry
    word = request.form['w']
    select = request.form['sel']
    num_title = range(len(title))

    for i in range(len(files[file])):
        if word in files[file][i][select]:
            arr.append((list(files[file][i].values()), i))

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
         word=word, title=title, num_title=num_title, arr=arr, num_list=num_list, num_total=num_total, enumerate=enumerate)   

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

    # print(files[file][int(test[0])])
    # print(arr[int(test[1])])

    for i in range(int(test[1]),session.get('num_total', None)):
        arr[i] = (arr[i][0], int(arr[i][1]) - 1)

    del files[file][int(test[0])]
    del arr[int(test[1])]

    session['num_total'] = session.get('num_total', None) -1
    
    return render_template('searching.html', f_name_list = f_name_list, file=file, arr=arr,
        title=title, num_title=num_title, num_list=num_list, num_total=num_total, index=index, enumerate=enumerate)

@app.route('/edit', methods = ['POST'])
def edit():
    f_name_list = files.keys()
    arr = session.get('arr', None)
    file = session.get('file', None)
    num_list = range(session.get('num_list', None))
    num_total = range(session.get('num_total', None))
    title = list(files[file][0].keys())
    num_title = range(len(title))

    fields=[]
    index=int(request.values['row'])
    temp = dict(zip(title, arr[index][0]))
    for i in num_title:
        fields.append(request.form['h'+str(i)])
        arr[index][0][i] = request.form['h'+str(i)]
        
    file_index = files[file].index(temp)
    temp2 = dict(zip(title, fields))
    # print(temp2)
    # print(file_index)
    files[file][file_index] = temp2
    
    # for i in num_title:
    #     fields.append(request.form['h'+str(i)])
    #     arr[index1][0][i] = request.form['h'+str(i)]
    #     files[file][index1][title[i]] = request.form['h'+str(i)]
    
    # print(files[file].index(temp))
    
    session['arr'] = arr

    return render_template('searching.html', f_name_list = f_name_list, file=file, arr=arr, index1=index,
        title=title, num_title=num_title, num_list=num_list, num_total=num_total, enumerate=enumerate)
    # return render_template('searching.html', f_name_list=f_name_list, enumerate=enumerate)

@app.route('/export', methods = ['POST'])
def export():
    f_name_list = files.keys()
    for file in f_name_list:
        dict_to_json(file, 'data/' + file + '.json')
    return render_template('searching.html', f_name_list=f_name_list)

@app.route('/backup', methods = ['POST'])
def backupFunction():
    global files
    file = session.get('file',None)
    f_name_list = files.keys()
    title = list(files[file][0].keys()) # get keys from first entry
    dict_to_json(files[file],"data/"+file+"-backup.json")
    BackUpMsg = "New "+file+" has been backed up!!!"
    files[file+"-backup"]=read_json("data/"+file+"-backup.json")
    return render_template('index.html',BackUpMsg=BackUpMsg, f_name_list=f_name_list,title=title, enumerate=enumerate)

@app.route('/insert', methods = ['POST'])
def insert():
    f_name_list = files.keys()
    arr = session.get('arr', None)
    file = session.get('file', None)
    num_list = range(session.get('num_list', None))
    num_total = range(session.get('num_total', None))
    title = list(files[file][0].keys())
    num_title = range(len(title))

    fields = []
    for i in num_title:
        fields.append(request.form['h'+str(i)])
    arr.append(((fields[0], fields[1]), len(arr)))

    temp = dict(zip(title, fields))

    files[file].append(temp)

    return render_template('searching.html', f_name_list = f_name_list, file=file, arr=arr,
        title=title, num_title=num_title, num_list=num_list, num_total=num_total, enumerate=enumerate)

@app.route('/analyzer')
def analyzer():
    data = a1()
    return render_template('analyzer.html',data=data)

if __name__ == "__main__":
    app.run(debug=True)
