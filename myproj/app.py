from flask import Flask, render_template, request, session
#from flask_wtf import FlaskForm
#from wtforms import StringField, SubmitField
import time
import re
import os
import matplotlib.pyplot as plt
import numpy as np
from io import BytesIO
import base64
from parse_json import read_json # Tristan's parse_json functions
from parse_json import dict_to_json
from analyzer import average_availability,price_range_ng,average_dow_p,price_distribution_region,average_price_for_min_nights,average_price_season

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.secret_key = 'super secret key'

rMsg = "Hello from Server!"
arr = ['']
pattern = r",(?=(?:[^\"]*\"[^\"]*\")*[^\"]*$)"


# load JSON files to dict of lists of dict; need to check if JSON or CSV is faster. CSV is smaller
files = {}
entries = os.path.abspath(os.path.dirname(__file__))
json_path = os.listdir(os.path.join(entries, 'data'))
listing = []
for i in json_path:
    if i.endswith(".json"):
        listing.append(i.replace(".json",""))
for i in listing:
    #tic = time.perf_counter()
    files[i] = read_json(os.path.join(entries,'data',i + '.json'))
    #toc = time.perf_counter()
    #print("Reading json "+i+f" in {toc - tic:0.4f} seconds")


# TODO add caches for analytics here


# read cached analytics images
# TODO This will have to be replaced so we can make the initial caches
data1 = os.path.join("static","images","price_range_ng.png")
data2 = os.path.join("static","images","average_availability.png")
data3 = os.path.join("static","images","average_dow_p.png")
data4 = os.path.join("static","images","price_distribution_region.png")
data5 = os.path.join("static","images","average_price_for_min_nights.png")
data6 = os.path.join("static","images","average_price_season.png")

neighborhood_name_list = []
for entry in files['neighbourhoods']:
    n = entry[r'neighbourhood']
    if n not in neighborhood_name_list:
        neighborhood_name_list.append(n)

@app.route('/')
def index():
    f_name_list = files.keys()
    session.clear()
    '''tic = time.perf_counter()
    price_range_ng(files['listings'])
    toc = time.perf_counter()
    print(f"Downloaded the listings in {toc - tic:0.4f} seconds")
    average_availability(files['listings'])
    tic = time.perf_counter()
    average_dow_p(files['calendar'])
    toc = time.perf_counter()
    print(f"Downloaded the calendar in {toc - tic:0.4f} seconds")
    session['neighbor'] = 'Hispanoam\u00e9rica'
    price_distribution_region(files['listings'], 'Hispanoam\u00e9rica')
    average_price_for_min_nights(files['listings'])
    average_price_season(files['calendar'])'''
    return render_template('index.html',f_name_list=f_name_list, neighborhood_name_list=neighborhood_name_list, data1=data1, data2=data2, data3=data3, 
    data4=data4, data5=data5, data6=data6, enumerate=enumerate)#, menu=menu)

@app.route('/region', methods = ['POST'])
def region():
    f_name_list = files.keys()
    neighbor = request.form['neighbor_name']
    session['neighbor'] = neighbor
    
    print(neighbor)
    price_distribution_region(files['listings'], neighbor)
    data4 = os.path.join("static","images","price_distribution_region.png")

    return render_template('index.html', f_name_list=f_name_list, neighborhood_name_list=neighborhood_name_list, data1=data1, data2=data2, data3=data3, 
    data4=data4, data5=data5, data6=data6, enumerate=enumerate)

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
    return render_template('searching.html',f_name_list=f_name_list, file=file, neighborhood_name_list=neighborhood_name_list,
        title=title, num_title=num_title, arr=arr, num_list=num_list, num_total=num_total, 
        data1=data1, data2=data2, data3=data3, data4=data4, data5=data5, data6=data6, enumerate=enumerate) 

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

    return render_template('searching.html',f_name_list=f_name_list, file=file, select= select, neighborhood_name_list=neighborhood_name_list,
         word=word, title=title, num_title=num_title, arr=arr, num_list=num_list, num_total=num_total,
         data1=data1, data2=data2, data3=data3, data4=data4, data5=data5, data6=data6, enumerate=enumerate)   

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
<<<<<<< HEAD
    '''price_range_ng(files['listings'])
=======
    # TODO each of these will be replaced with the appropriate file-change checks, cache updates, and redraws
    price_range_ng(files['listings'])
>>>>>>> 4883a2fea513e4c3b3ff36deb893f72cb04395ea
    average_availability(files['listings'])
    average_dow_p(files['calendar'])
    neighbor = session.get('neighbor', None)
    price_distribution_region(files['listings'], neighbor)
    average_price_for_min_nights(files['listings'])
    average_price_season(files['calendar'])'''

    return render_template('searching.html', f_name_list = f_name_list, file=file, arr=arr, neighborhood_name_list=neighborhood_name_list,
        title=title, num_title=num_title, num_list=num_list, num_total=num_total, index=index,
        data1=data1, data2=data2, data3=data3, data4=data4, data5=data5, data6=data6, enumerate=enumerate)

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
<<<<<<< HEAD
    '''price_range_ng(files['listings'])
=======
    # TODO each of these will be replaced with the appropriate file-change checks, cache updates, and redraws
    price_range_ng(files['listings'])
>>>>>>> 4883a2fea513e4c3b3ff36deb893f72cb04395ea
    average_availability(files['listings'])
    average_dow_p(files['calendar'])
    neighbor = session.get('neighbor', None)
    price_distribution_region(files['listings'], neighbor)
    average_price_for_min_nights(files['listings'])
    average_price_season(files['calendar'])'''

    return render_template('searching.html', f_name_list = f_name_list, file=file, arr=arr, index1=index,
        title=title, num_title=num_title, num_list=num_list, num_total=num_total, neighborhood_name_list=neighborhood_name_list,
        data1=data1, data2=data2, data3=data3, data4=data4, data5=data5, data6=data6, enumerate=enumerate)
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
    '''price_range_ng(files['listings'])
    average_availability(files['listings'])
    average_dow_p(files['calendar'])
    neighbor = session.get('neighbor', None)
    price_distribution_region(files['listings'], neighbor)
    average_price_for_min_nights(files['listings'])
    average_price_season(files['calendar'])'''
    return render_template('index.html',BackUpMsg=BackUpMsg, f_name_list=f_name_list,title=title, neighborhood_name_list=neighborhood_name_list,
    data1=data1, data2=data2, data3=data3, data4=data4, data5=data5, data6=data6, enumerate=enumerate)

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
<<<<<<< HEAD
    '''price_range_ng(files['listings'])
=======
    # TODO each of these will be replaced with the appropriate file-change checks, cache updates, and redraws
    price_range_ng(files['listings'])
>>>>>>> 4883a2fea513e4c3b3ff36deb893f72cb04395ea
    average_availability(files['listings'])
    average_dow_p(files['calendar'])
    neighbor = session.get('neighbor', None)
    price_distribution_region(files['listings'], neighbor)
    average_price_for_min_nights(files['listings'])
    average_price_season(files['calendar'])'''

    return render_template('searching.html', f_name_list = f_name_list, file=file, arr=arr,
        title=title, num_title=num_title, num_list=num_list, num_total=num_total, neighborhood_name_list=neighborhood_name_list,
        data1=data1, data2=data2, data3=data3, data4=data4, data5=data5, data6=data6, enumerate=enumerate)

@app.after_request
def add_header(response):
    # response.cache_control.no_store = True
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '-1'
    return response

if __name__ == "__main__":
    app.run(debug=True)
