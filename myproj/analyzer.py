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

# draw graph
def bar_graph(data_in, title, y_label, x_label):
    # extract data and labels
    labels = []
    data = []
    for d in data_in:
        labels.append(d[0])
        data.append(d[1])
    
    # create plot
    fig, ax = plt.subplots()
    # position bars
    x = np.arange(len(labels))
    
    # add bars
    width = .5
    bars = ax.bar(x, data, width)

    # label axes
    ax.set_title(title)
    ax.set_ylabel(y_label)
    ax.set_xlabel(x_label)
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    plt.setp(ax.get_xticklabels(), rotation=30, horizontalalignment='right')
    # save
    buf = BytesIO()
    fig.savefig('graph.png', format='png') # currently saves to file for testing
    fig.savefig(buf, format="PNG")
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return data



# takes correct file array
# returns list of pairs; neighbourhood group and availability, could generalize to average x per y by replacing availability_365 and neighbourhood group with arguments

def average_availability(data):
    
    groups = {}
    result = []
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
    for k, v in groups.items():
        avg = v[0] / v[1]
        result.append((k, avg))

    return result



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


# takes correct file array
# returns list of pairs, (day, average price)
# parallel version

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
    
    names = [r'Monday', r'Tuesday', r'Wednesday', r'Thursday', r'Friday', r'Saturday', r'Sunday']
    result = []
    for i in [6,1,2,3,4,5]:
        result.append((names[i], days[i] / count[i])) # store as ('-day', average) Mon-Fri

    return result


# takes correct file array
# returns list of pairs (day, average price)
# simple version

def average_dow(data):
    days =  [0,0,0,0,0,0,0] # Mon - Sun
    count = [0,0,0,0,0,0,0]
    
    for entry in data:
        day = entry[r'date'].split(r'-')
        day_index = datetime.date(int(day[0]), int(day[1]), int(day[2])).weekday()
        
        days[day_index] += float(entry[r'price'])
        count[day_index] += 1
    
    names = [r'Monday', r'Tuesday', r'Wednesday', r'Thursday', r'Friday', r'Saturday', r'Sunday']
    result = []
    for i in range(7):
        result[(i + 6) % 7] = (names[i], days[i] / count[i]) # store as ('-day', average) Mon-Fri

    return result
