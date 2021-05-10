import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
import numpy as np
from io import BytesIO
import base64
import datetime
from multiprocessing import Process, Pipe
import time
from color import color_css
# takes listings
# returns plot of neighbourhood group average availability
def average_availability(data):
    
    groups = {}
    # for each entry
    for entry in data:
        # get neighbourhood group and avaiablility
        group = entry[r'neighbourhood_group']
        avail = int(entry[r'availability_365'])

        # if group not counted yet, add group, else add availability
        if group not in groups:
            groups[group] = [avail, 1]
            continue
        groups[group][0] = groups[group][0] + avail
        groups[group][1] = groups[group][1] + 1

    # average availability per group
    labels = []
    vals = []
    for k, v in groups.items():
        avg = v[0] / v[1]
        labels.append(k)
        vals.append(avg)

    # make plot
    fig, ax = plt.subplots(figsize=(10,4))

    total_color = len(groups)
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
    fig.savefig('static/images/average_availability.png', format='png',bbox_extra_artists=(lg,text),bbox_inches='tight') 
    #fig.savefig(buf, format='png',bbox_extra_artists=(lg,text),bbox_inches='tight') 
    #data = base64.b64encode(buf.getbuffer()).decode("ascii")
    #return data


# helper for average_dow_p
def avg_helper(entries, pipe):
    days =  [0,0,0,0,0,0,0] # Mon - Sun
    count = [0,0,0,0,0,0,0]
    
    for entry in entries:
        day = entry[r'date'].split(r'-')
        day_i = datetime.date(int(day[0]), int(day[1]), int(day[2])).weekday()
            
        days[day_i] += float(entry[r'price'])
        count[day_i] += 1

    pipe.send((days, count))
    pipe.close()


# takes calendar
# returns plot of average price by day of week
# parallelized
def average_dow_p(data):

    days =  [0,0,0,0,0,0,0] # Mon - Sun
    count = [0,0,0,0,0,0,0]

    processes = []
    pipes = []
    
    s = 0
    l = int(len(data) / 4) # found more than 4 processes does not benefit
    e = l
    for _ in range(4-1):
        parent, child = Pipe()
        p = Process(target=avg_helper, args=[data[s:e], child])
        s = e
        e += l
        p.start()
        processes.append(p)
        pipes.append(parent)

    parent, child = Pipe()
    p = Process(target=avg_helper, args=[data[s:], child])
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
    vals = [0, 0, 0, 0, 0, 0, 0]
    for i in [6,0,1,2,3,4,5]:
        avg = days[i] / count[i]
        vals[i] = avg

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
    fig.savefig('static/images/average_dow_p.png', format='png',bbox_extra_artists=(lg,text),bbox_inches='tight') 
    #fig.savefig(buf, format='png',bbox_extra_artists=(lg,text),bbox_inches='tight') 
    #data = base64.b64encode(buf.getbuffer()).decode("ascii")
    #return data

'''
# takes calendar
# returns plot of price per day of week
# serial
def average_dow(data):
    days =  [0,0,0,0,0,0,0] # Mon - Sun
    count = [0,0,0,0,0,0,0]
    
    for entry in data:
        day = entry[r'date'].split(r'-')
        day_index = datetime.date(int(day[0]), int(day[1]), int(day[2])).weekday()
        
        days[day_index] += float(entry[r'price'])
        count[day_index] += 1
    

    labels = [r'Sunday', r'Monday', r'Tuesday', r'Wednesday', r'Thursday', r'Friday', r'Saturday']
    vals = [0, 0, 0, 0, 0, 0, 0]
    for i in [6,0,1,2,3,4,5]:
        avg = days[i] / count[i]
        vals[i] = avg

    # make plot
    fig, ax = plt.subplots(figsize=(10,4))

    # setup
    plt.bar(labels, vals, color='maroon', width = 0.6)
    plt.title('Average Price by Day of the Week')
    plt.xlabel('Day')
    plt.ylabel('Daily Price')
    
    # save
    buf = BytesIO()
    #fig.savefig('graph.png', format='png') # currently saves to file for testing
    fig.savefig(buf, format="PNG")
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return data
'''
'''
# takes listings
# returns plot of average price per neighbourhood group
def average_price_ng(data):
    
    groups = {}
    # for each entry
    for entry in data:
        # get neighbourhood group and avaiablility
        group = entry[r'neighbourhood_group']
        price = int(entry[r'price'])

        # if group not counted yet, add group, else add price
        if group not in groups:
            groups[group] = [price, 1]
            continue
        groups[group][0] = groups[group][0] + price
        groups[group][1] = groups[group][1] + 1

    # average availability per group
    labels = []
    vals = []
    for k, v in groups.items():
        avg = v[0] / v[1]
        labels.append(k)
        vals.append(avg)

    # make plot
    fig, ax = plt.subplots(figsize=(10,4))

    # setup
    plt.bar(labels, vals, color='maroon', width = 0.6)
    plt.title('Average Price of each Neighbourhood Group')
    plt.xlabel('Neighbourhood Group')
    plt.ylabel('Daily Price')
    plt.setp(ax.get_xticklabels(), rotation = 20, horizontalalignment='right')
    fig.subplots_adjust(bottom=0.25)
    
    # save
    buf = BytesIO()
    fig.savefig('graph.png', format='png') # currently saves to file for testing
    fig.savefig(buf, format="PNG")
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return data
'''
# takes listings
# returns plot of average price per neighbourhood group
def price_range_ng(data):
    
    groups = {}
    # for each entry
    for entry in data:
        # get neighbourhood group and avaiablility
        group = entry[r'neighbourhood_group']
        price = float(entry[r'price'])
        # if price >= 400:
        #     continue 
        # if group not counted yet, add group, else add price
        if group not in groups:
            groups[group] = [price, 1, price, price]
            continue
        groups[group][0] = groups[group][0] + price
        groups[group][1] = groups[group][1] + 1
        if price < groups[group][2]: # new min
            groups[group][2] = price
        if price > groups[group][3]: # new max
            groups[group][3] = price

    # average availability per group
    labels = []
    _fil = []
    _upp = []
    _low = []
    for k, v in groups.items():
        avg = (v[0] / v[1]) - v[2]
        labels.append(k)
        _low.append(avg)
        _fil.append(v[2])
        top = v[3] - avg
        _upp.append(int(top))
    
    fil=np.array(_fil)
    upp=np.array(_upp)
    low=np.array(_low)
    # make plot
    fig, ax = plt.subplots(figsize=(10,4))
    # setup
    plt.barh(labels, fil, color='black', height= 0.6) # fill up to bottom 
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
    fig.savefig('static\images\price_range_ng.png', format='png',bbox_extra_artists=(lg,),bbox_inches='tight') # currently saves to file for testing
    #fig.savefig(buf, format='png',bbox_extra_artists=(lg,text),bbox_inches='tight') 
    #data = base64.b64encode(buf.getbuffer()).decode("ascii")
    #return data

def price_distribution_region(data, region):
    
    group = []

    for entry in data:
        if entry[r'neighbourhood'] == region:
            group.append(int(entry[r'price']))
    
    group.sort()

    fig, ax = plt.subplots(figsize = (10, 4))

    n, bins, patches = ax.hist(group, bins=[0,10,20,30,40,50,60,70,80,90,100,120,140,160,180,200,250,300,400,500,600,700,800,900,1000])

    plt.tight_layout()
    plt.title('Price Distribution for ' + region)
    plt.xlabel('Price')
    plt.ylabel('Frequency')
    plt.xlim(0, 1000)
    buf = BytesIO()
    fig.savefig('static/images/price_distribution_region.png', format='png', bbox_inches='tight')

    print(group)

def add_list(l, p, v):
    size = len(l)
    if p < size: # l[p] is already allocated
        l[p] += v
        return
    # else need to extend list to p - 1 elements
    l += [0] * (p - size)
    l.append(v)

def average_price_for_min_nights(data):
    days = []
    count = []

    for entry in data:
        min_night = int(entry[r'minimum_nights'])
        price = float(entry[r'price'])
        #outliers removed
        if price > 400 or min_night > 50:
            continue
        add_list(days, min_night, price)
        add_list(count, min_night, 1)

    for i in range(len(days)):
        if count[i] > 0:
            days[i] /= count[i]

    fig, ax = plt.subplots(figsize = (10, 4))

    # ax = fig.add_axes([0, 0, 1, 1])
    label = []
    for i in range(len(days)):
        label.append(i)
    ax.bar(label, days)

    # fig = plt.plot(range(len(days)), days)
    plt.tight_layout()
    plt.title('Average Price Per Minimum Nights')
    plt.xlabel('Minimum Nights')
    plt.ylabel('Average Price')

    plt.savefig('static/images/average_price_for_min_nights.png', format='png', bbox_inches='tight')


def average_helper_year(entries, pipe):

    years = [0, 0, 0, 0, 0, 0, 0]
    count = [0, 0, 0, 0, 0, 0, 0]
    # test = [0, 0, 0, 0, 0, 0, 0]
    
    for entry in entries:
        year = entry[r'date'].split(r'-')
        year_i = int(year[0]) % 2015
        # print(year[0], int(year[0]) % 2015)
            
        years[year_i] += float(entry[r'price'])
        count[year_i] += 1

    pipe.send((years, count))
    pipe.close()


def average_price_year(data):

    years = [0, 0, 0, 0, 0, 0, 0]
    count = [0, 0, 0, 0, 0, 0, 0]

    processes = []
    pipes = []
    
    s = 0
    l = int(len(data) / 4) # found more than 4 processes does not benefit
    e = l
    for _ in range(4-1):
        parent, child = Pipe()
        p = Process(target=average_helper_year, args=[data[s:e], child])
        s = e
        e += l
        p.start()
        processes.append(p)
        pipes.append(parent)

    parent, child = Pipe()
    p = Process(target=average_helper_year, args=[data[s:], child])
    p.start()
    processes.append(p)
    pipes.append(parent)

    for p in range(len(processes)):
        processes[p].join()
        result = pipes[p].recv()
        for i in range(len(years)):
            years[i] += result[0][i]
            count[i] += result[1][i]
    
    print(years)
    print(count)

    labels = [r'2015', r'2016', r'2017', r'2018', r'2019', r'2020', r'2021']
    vals = [0, 0, 0, 0, 0, 0, 0]
    for i in range(len(count)):
        if count[i] == 0:
            count[i] = 1
    for i in range(len(labels)):
        avg = years[i] / count[i]
        vals[i] = avg
    
    print(vals)

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
    plt.title('Average Price by Year')
    plt.xlabel('Year')
    plt.ylabel('Yearly Price')
    
    # save
    buf = BytesIO()
    fig.savefig('static/images/average_price_year.png', format='png',bbox_extra_artists=(lg,text),bbox_inches='tight') 

