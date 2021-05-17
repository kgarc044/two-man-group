from analytics import * # we need all the functions
from parse_json import read_json
import os


files = {"listings" : read_json(os.path.join(os.path.curdir, 'data', 'test_listings.json')), "calendar" : read_json(os.path.join(os.path.curdir, 'data', 'test_calendar.json'))}

print("Testing average_availability")


# create cache
avg_avail_cache = cache_avg_avail(files)

# initial plot
plot_avg_avail(avg_avail_cache, os.path.join('test_images', 'avg_avail_0.png'))


# add high number entry and re-plot
add_avg(avg_avail_cache, "Arganzuela", 2000)

plot_avg_avail(avg_avail_cache, os.path.join('test_images', 'avg_avail_1.png'))


# replace high number entry with larger and re-plot
modify_avg(avg_avail_cache, "Arganzuela", 5000, 2000)

plot_avg_avail(avg_avail_cache, os.path.join('test_images', 'avg_avail_2.png'))


# remove high number and re-plot; should match avg_avail_0.png
remove_avg(avg_avail_cache, "Arganzuela", 5000)

plot_avg_avail(avg_avail_cache, os.path.join('test_images', 'avg_avail_3.png'))
