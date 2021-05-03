import matplotlib.pyplot as plt
import numpy as np
from io import BytesIO
import base64
import datetime
from multiprocessing import Process, Pipe

def a1():
    labels = ['G1', 'G2', 'G3', 'G4', 'G5']
    men_means = [20, 34, 30, 35, 27]
    women_means = [25, 32, 34, 20, 25]
    
    x = np.arange(len(labels))  # the label locations
    width = 0.35  # the width of the bars

    fig, ax = plt.subplots()
    rects1 = ax.bar(x - width/2, men_means, width, label='Men')
    rects2 = ax.bar(x + width/2, women_means, width, label='Women')

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('Scores')
    ax.set_title('Scores by group and gender')
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend()
    ax.bar_label(rects1, padding=3)
    ax.bar_label(rects2, padding=3)
    buf = BytesIO() 
    fig.savefig(buf,format="png")
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return data


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

    # setup
    plt.bar(labels, vals, color='maroon', width = 0.6)
    plt.title('Average Availability of each Neighbourhood Group')
    plt.xlabel('Neighbourhood Group')
    plt.ylabel('Days in the Year')
    plt.setp(ax.get_xticklabels(), rotation = 20, horizontalalignment='right')
    fig.subplots_adjust(bottom=0.25)
    
    # save
    buf = BytesIO()
    fig.savefig('graph.png', format='png') # currently saves to file for testing
    fig.savefig(buf, format="PNG")
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return data



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
def average_dow_p(data, i):

    days =  [0,0,0,0,0,0,0] # Mon - Sun
    count = [0,0,0,0,0,0,0]

    processes = []
    pipes = []
    
    s = 0
    l = int(len(data) / i) # found more than 4 processes does not benefit
    e = l
    for _ in range(i-1):
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

# *** BROKEN ***
# takes listings
# returns plot of average price per neighbourhood group
def price_range_ng(data):
    
    groups = {}
    # for each entry
    for entry in data:
        # get neighbourhood group and avaiablility
        group = entry[r'neighbourhood_group']
        price = float(entry[r'price'])

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
    fil = []
    upp = []
    low = []
    for k, v in groups.items():
        print(v)
        avg = (v[0] / v[1]) - v[2]
        labels.append(k)
        low.append(avg)
        fil.append(v[2])
        top = v[3] - avg
        upp.append(top)

    # make plot
    fig, ax = plt.subplots(figsize=(10,4))

    # setup
    plt.bar(labels, fil, color='white', width = 0.6) # fill up to bottom
    plt.bar(labels, low, color='maroon', width = 0.6, bottom = fil)
    plt.bar(labels, upp, color='forestgreen', width = 0.6, bottom = low+fil)
    plt.title('Price Range of each Neighbourhood Group')
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
