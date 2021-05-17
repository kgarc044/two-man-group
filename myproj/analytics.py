import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
import numpy as np
from io import BytesIO
import base64
import datetime
from multiprocessing import Process, Pipe
import time
from color import color_css
import os

### cache_* functions build cache
### all caches are dictionaries with label as key (region for prc_distro_rgn) and list [sum, count], [sum, count, min, max], or [prices] as value

### *_avg is used for all but prc_rng_ng, and prc_distro-rgn
def add_avg(cache, label, val):
    if label not in cache:

        cache[label] = [val, 1]
    else:
        cache[label][0] += val
        cache[label][1] += 1

def remove_avg(cache, label, val):
    cache[label][0] -= val
    cache[label][1] -= 1

def modify_avg(cache, label, new_val, old_val):
    cache[label][0] += new_val - old_val
    # count stays the same

### for prc_rng_ng
def add_rng(cache, label, val):
    if label not in cache:
        cache[label] = [val, 1, val, val]
    else:
        cache[label][0] += val
        cache[label][1] += 1
        if val > cache[label][2]: # extra logic for max, min
            cache[label][2] = val
        elif val < cache[label][3]:
            cache[label][3] = val

### harder to do, has to actually check full list, but function is at least lighter weight; needs to be called after the full record is updated
def remove_rng(cache, data, label, val):
    cache[label][0] -= val
    cache[label][1] -= 1

    # check max, min
    vals = [float(d['price']) for d in data['listings'] if d['neighbourhood_group'] == label] # get prices that are part of ng

    if val > max(vals): # val was max
        cache[label][2] = max(vals)
    elif val < min(vals): # val was min
        cache[label][3] = min(vals)

def modify_rng(cache, data, label, new_val, old_val):
    cache[label][0] += new_val - old_val
    # count stays the same
    
    # check max, min
    vals = [float(d['price']) for d in data['listings'] if d['neighbourhood_group'] == label] # get prices that are part of ng; might have to use this syntax in the cache fn...

    if old_val > max(vals): # old_val was max
        if new_val > old_val: # new_val is new max
            cache[label][2] = new_val
        else: # get new max
            cache[label][2] = max(vals)
    elif old_val < min(vals): # old_val was min
        if new_val < old_val: # new_val is new min
            cache[label][2] = new_val
        else: # get new min
            cache[label][3] = min(vals)

### for prc_distro_rgn
def add_distro(cache, label, val):
    if label not in cache:
        cache[label] = [val]
    else:
        cache[label].append(val)
        cache[label].sort()

def remove_distro(cache, label, val):
    cache[label].remove(val)

def modify_distro(cache, label, new_val, old_val):

    cache[label].remove(old_val)
    cache[label].append(new_val)
    cache[label].sort()
    
def add_new_distro(cache, files, label):
    cache = cache_prc_distro_rgn(files, label)

### -------------------------------------------------------
### Functions for caching and plotting
### -------------------------------------------------------

### average availability functions
### I wrote this set as an example

def cache_avg_avail(files):

    data = files['listings'] # new function is passed all of files and gets listings here, for consistant args to all cache_* functions
    groups = {} # this is returned at the end
    
    for entry in data:
        group = entry['neighbourhood_group']
        avail = int(entry['availability_365'])

        if group not in groups: # add new group
            groups[group] = [avail, 1]
            continue
        # else
        groups[group][0] += avail
        groups[group][1] += 1

    return groups # return dictionary as cache

def plot_avg_avail(cache, img_path):
    labels = [] # break cache into lists of labels and averages of data
    vals = []
    
    for k,v in cache.items():
        labels.append(k)
        vals.append(v[0] / v[1])

    # copy plotting code from old fn, except added img_path to path; change groups to cache
        
    # make plot
    fig, ax = plt.subplots(figsize=(10,4))

    total_color = len(cache)
    arr_color = color_css()
    # setup
    
    for i in range(len(labels)):
        plt.bar(labels[i], vals[i], color=arr_color[i], edgecolor = "black" , width = 0.6 , label = labels[i])
    lg = ax.legend(fontsize='small', bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0., ncol=2)
    text = ax.text(-0.2,1.05," ", transform=ax.transAxes)
    ax.axes.xaxis.set_visible(False)
    plt.tight_layout()
    plt.title('Average Availability of each Neighbourhood Group')
    plt.xlabel('Neighbourhood Group')
    plt.ylabel('Days in the Year')
    #plt.setp(ax.get_xticklabels(), rotation = 20, horizontalalignment='right')
    #fig.subplots_adjust(bottom=0.25)
    # save
    buf = BytesIO()
    os_path = os.path.abspath(os.path.dirname(__file__))
    fig.savefig(os.path.join(os_path, img_path), format='png',bbox_extra_artists=(lg,text),bbox_inches='tight') # used os.path.join for consistancy with other code; should really join '.png' not make part of img_path


### average day of week functions

# helper for average_dow_p
def avg_dow_helper(entries, pipe):
    days =  [0,0,0,0,0,0,0] # Mon - Sun
    count = [0,0,0,0,0,0,0]
    
    for entry in entries:
        day = entry[r'date'].split(r'-')
        day_i = datetime.date(int(day[0]), int(day[1]), int(day[2])).weekday()
            
        days[day_i] += float(entry[r'price'])
        count[day_i] += 1

    pipe.send((days, count))
    pipe.close()


def cache_avg_dow(files):
    
    data = files['calendar']

    days =  [0,0,0,0,0,0,0] # Mon - Sun
    count = [0,0,0,0,0,0,0]

    processes = []
    pipes = []
    
    s = 0
    l = int(len(data) / 4) # found more than 4 processes does not benefit
    e = l
    for _ in range(3):
        parent, child = Pipe()
        p = Process(target=avg_dow_helper, args=[data[s:e], child])
        s = e
        e += l
        p.start()
        processes.append(p)
        pipes.append(parent)

    parent, child = Pipe()
    p = Process(target=avg_dow_helper, args=[data[s:], child])
    p.start()
    processes.append(p)
    pipes.append(parent)

    for p in range(len(processes)):
        processes[p].join()
        result = pipes[p].recv()
        for i in range(7):
            days[i] += result[0][i]
            count[i] += result[1][i]
    
    labels = [r'Sunday', r'Monday', r'Tuesday', r'Wednesday', r'Thursday', r'Friday', r'Saturday']
    ret_val = {}
    for i in range(7):
        ret_val[labels[i]] = [days[i], count[i]]

    return ret_val


def plot_avg_dow(cache, img_path):

    labels = []
    vals = []
    for k, v in cache.items():
        labels.append(k)
        vals.append(v[0] / v[1])

    # make plot
    fig, ax = plt.subplots(figsize=(10,4))

    total_color = len(labels)
    arr_color = color_css()

    # setup
    for i in range(len(labels)):
        plt.bar(labels[i], vals[i], color=arr_color[i+10], width = 0.6, label = labels[i])
    lg = ax.legend(fontsize='small', bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0., ncol=2)
    text = ax.text(-0.2,1.05," ", transform=ax.transAxes)
    ax.axes.xaxis.set_visible(False)
    plt.tight_layout()
    plt.title('Average Price by Day of the Week')
    plt.xlabel('Day')
    plt.ylabel('Daily Price')
    
    # save
    buf = BytesIO()
    os_path = os.path.abspath(os.path.dirname(__file__))
    fig.savefig(os.path.join(os_path, img_path), format='png',bbox_extra_artists=(lg,text),bbox_inches='tight') 


### price range by neighbourhood group functions

def cache_prc_rng_ng(files):
    
    data = files['listings']

    groups = {}
    # for each entry
    for entry in data:
        # get neighbourhood group and avaiablility
        group = entry[r'neighbourhood_group']
        price = float(entry[r'price'])
        
        if group not in groups:
            groups[group] = [price, 1, price, price]
            continue
        # else
        groups[group][0] = groups[group][0] + price
        groups[group][1] = groups[group][1] + 1
        if price > groups[group][2]: # new max
            groups[group][2] = price
        if price < groups[group][3]: # new min
            groups[group][3] = price
    
    return groups


def plot_prc_rng_ng(cache, img_path):
    
    labels = [] # bar name
    filler = [] # minimum
    upper = []  # maximum
    lower = []  # average
    
    for k, v in cache.items():
        labels.append(k)
        filler.append(v[3])         # fill up to minimum
        avg = (v[0] / v[1]) - v[3]  # fill minimum up to avg
        lower.append(avg)           # "
        upper.append(v[2] - avg)    # fill average up to max

    fil=np.array(filler)
    upp=np.array(upper)
    low=np.array(lower)
    # make plot
    fig, ax = plt.subplots(figsize=(10,4))
    # setup
    plt.barh(labels, fil, color='lightgrey', height= 0.6) # fill up to bottom 
    plt.barh(labels, upp, color='forestgreen', height= 0.6, left = low+fil , label = "Above Average Price")
    plt.barh(labels, low, color='maroon', height= 0.6, left= fil, label = 'Below Average Price')
    lg = ax.legend(fontsize='small', bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)
    text = ax.text(-0.2,1.05," ", transform=ax.transAxes)
    #plt.setp(ax.get_xticklabels(), rotation = 90, horizontalalignment='right')
    #fig.subplots_adjust(bottom=0.25)
    #ax.axes.xaxis.set_visible(False)
    plt.tight_layout()
    plt.title('Price Range of each Neighbourhood Group')
    plt.xlabel('Neighbourhood Group')
    plt.ylabel('Daily Price')
 
    # save
    buf = BytesIO()
    os_path = os.path.abspath(os.path.dirname(__file__))
    fig.savefig(os.path.join(os_path, img_path), format='png',bbox_extra_artists=(lg,),bbox_inches='tight') # currently saves to file for testing


### price distribution by region functions

def cache_prc_distro_rgn(files):

    data = files['listings']
    ret_val = {}

    for entry in data:
        if entry[r'neighbourhood'] not in ret_val:
            ret_val[entry['neighbourhood']] = [int(entry['price'])]
            continue
        # else
        ret_val[entry['neighbourhood']].append(int(entry['price']))

    for _, v in ret_val.items():
        v.sort()

    return ret_val

def plot_prc_distro_rgn(cache, region, img_path):

    fig, ax = plt.subplots(figsize = (10, 4))
    n, bins, patches = ax.hist(cache[region], bins=[0,10,20,30,40,50,60,70,80,90,100,120,140,160,180,200,250,300,400,500,600,700,800,900,1000])
    #n, bins, patches = ax.hist(cache[region])
    plt.tight_layout()
    plt.title('Price Distribution for ' + region)
    plt.xlabel('Price')
    plt.ylabel('Frequency')
    plt.xlim(0, 1000)
    buf = BytesIO()
    os_path = os.path.abspath(os.path.dirname(__file__))
    fig.savefig(os.path.join(os_path, img_path), format='png', bbox_inches='tight')


### average price by minimum nights functions

def cache_avg_prc_min_nts(files):
    
    data = files['listings']

    days = {}
    
    for entry in data:
        min_night = entry['minimum_nights']
        price = float(entry['price'])
        # remove outliers
        if int(price) > 400 or int(min_night) > 50:
            continue
        # else
        if min_night not in days:
            days[min_night] = [price, 1]
            continue
        # else
        days[min_night][0] += price
        days[min_night][1] += 1

    return days

def plot_avg_prc_min_nts(cache, img_path):
    
    # convert string keys to int
    new_cache = {}
    for k, v in cache.items():
        new_cache[int(k)] = v

    fig, ax = plt.subplots(figsize = (10, 4))

    # ax = fig.add_axes([0, 0, 1, 1])
    label = []
    price = []
    for k, v in sorted(new_cache.items()):
        label.append(k)
        price.append(v[0] / v[1])
    ax.bar(label, price)

    # fig = plt.plot(range(len(days)), days)
    plt.tight_layout()
    plt.title('Average Price Per Minimum Nights')
    plt.xlabel('Minimum Nights')
    plt.ylabel('Average Price')
    os_path = os.path.abspath(os.path.dirname(__file__))
    plt.savefig(os.path.join(os_path, img_path), format='png', bbox_inches='tight')


### average price by season functions

def average_helper_season(data, pipe):

    groups = {}

    groups['Winter'] = [0, 0]
    groups['Spring'] = [0, 0]
    groups['Summer'] = [0, 0]
    groups['Autumn'] = [0, 0]

    for entry in data:
        year = entry[r'date'].split(r'-')
        month = int(year[1])
        if month in [12, 1, 2]:
            groups['Winter'][0] += float(entry[r'price'])
            groups['Winter'][1] += 1
        elif month in [3, 4, 5]:
            groups['Spring'][0] += float(entry[r'price'])
            groups['Spring'][1] += 1
        elif month in [6, 7, 8]:
            groups['Summer'][0] += float(entry[r'price'])
            groups['Summer'][1] += 1
        elif month in [9, 10, 11]:
            groups['Autumn'][0] += float(entry[r'price'])
            groups['Autumn'][1] += 1
    pipe.send(groups)
    pipe.close()

def cache_avg_prc_ssn(files):

    data = files['calendar']
    groups = {}

    groups['Winter'] = [0, 0]
    groups['Spring'] = [0, 0]
    groups['Summer'] = [0, 0]
    groups['Autumn'] = [0, 0]

    processes = []
    pipes = []
    
    s = 0
    l = int(len(data) / 4) # found more than 4 processes does not benefit
    e = l
    for _ in range(4-1):
        parent, child = Pipe()
        p = Process(target=average_helper_season, args=[data[s:e], child])
        s = e
        e += l
        p.start()
        processes.append(p)
        pipes.append(parent)

    parent, child = Pipe()
    p = Process(target=average_helper_season, args=[data[s:], child])
    p.start()
    processes.append(p)
    pipes.append(parent)


    for p in range(len(processes)):
        processes[p].join()
        result = pipes[p].recv()
        groups['Winter'][0] += result['Winter'][0]
        groups['Winter'][1] += result['Winter'][1]
        groups['Spring'][0] += result['Spring'][0]
        groups['Spring'][1] += result['Spring'][1]
        groups['Summer'][0] += result['Summer'][0]
        groups['Summer'][1] += result['Summer'][1]
        groups['Autumn'][0] += result['Autumn'][0]
        groups['Autumn'][1] += result['Autumn'][1]

    return groups


def plot_avg_prc_ssn(cache, img_path):

    labels = [] # break cache into lists of labels and averages of data
    vals = []
    
    for k,v in cache.items():
        labels.append(k)
        vals.append(v[0] / v[1])

    fig, ax = plt.subplots(figsize=(10,4))

    total_color = len(cache)
    arr_color = color_css()

    # setup
    for i in range(len(labels)):
        plt.bar(labels[i], vals[i], color=arr_color[i+10], width = 0.6, label = labels[i])
    lg = ax.legend(fontsize='small', bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0., ncol=2)
    text = ax.text(-0.2,1.05," ", transform=ax.transAxes)
    ax.axes.xaxis.set_visible(False)
    plt.tight_layout()
    plt.title('Average Price by Season')
    plt.xlabel('Season')
    plt.ylabel('Seasonal Price')
    
    # save
    buf = BytesIO()
    os_path = os.path.abspath(os.path.dirname(__file__))
    fig.savefig(os.path.join(os_path, img_path), format='png',bbox_extra_artists=(lg,text),bbox_inches='tight')

