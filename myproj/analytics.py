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
    vals = [d['price'] for d in data['listings'] if d['neighbourhood_group'] == label] # get prices that are part of ng

    if val > vals.max(): # val was max
        cache[label][2] = vals.max()
    elif val < vals.min(): # val was min
        cache[label][3] = vals.min()

def modify_rng(cache, data, label, new_val, old_val):
    cache[label][0] += new_val - old_val
    # count stays the same
    
    # check max, min
    vals = [d['price'] for d in data['listings'] if d['neighbourhood_group'] == label] # get prices that are part of ng; might have to use this syntax in the cache fn...

    if old_val > vals.max(): # old_val was max
        if new_val > old_val: # new_val is new max
            cache[label][2] = new_val
        else: # get new max
            cache[label][2] = vals.max()
    elif old_val < vals.min(): # old_val was min
        if new_val < old_val: # new_val is new min
            cache[label][2] = new_val
        else: # get new min
            cache[label][3] = vals.min()

### for prc_distro_rgn
def add_distro(cache, label, val):
    cache[label].append(val)
    cache[label].sort()

def remove_distro(cache, label, val):
    cache[label].remove(val)

def modify_distro(cache, label, new_val, old_val):
    cache[label].remove(old_val)
    cache[label].append(new_val)
    cache[label].sort()

def add_new_distro(cache, files, label):
    cache = cache_prc_distro_rgn(cache, files, label)

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

def cache_avg_dow(files):
    pass

def plot_avg_dow(cache, img_path):
    pass


### price range by neighbourhood group functions

def cache_prc_rng_ng(files):
    pass

def plot_prc_rng_ng(cache, img_path):
    pass


### price distribution by region functions

def cache_prc_distro_rgn(cache, files, region):

    data = files['listings']
    group = []

    for entry in data:
        if entry[r'neighbourhood'] == region:
            group.append(int(entry[r'price']))
    
    group.sort()

    cache[region] = group

    return cache


def plot_prc_distro_rgn(cache, region, img_path):

    fig, ax = plt.subplots(figsize = (10, 4))
    print(cache[region])
    # n, bins, patches = ax.hist(cache[region], bins=[0,10,20,30,40,50,60,70,80,90,100,120,140,160,180,200,250,300,400,500,600,700,800,900,1000])
    n, bins, patches = ax.hist(cache[region])
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
    pass

def plot_avg_prc_min_nts(cache, img_path):
    pass


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

