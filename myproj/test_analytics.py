from analytics import * # we need all the functions
from parse_json import read_json
import os


files = {"listings" : read_json(os.path.join(os.path.curdir, 'data', 'test_listings.json')), "calendar" : read_json(os.path.join(os.path.curdir, 'data', 'test_calendar.json'))}


print("Testing Average Availability")

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



print("Testing Average DoW")

avg_dow_cache = cache_avg_dow(files)

# initial plot
plot_avg_dow(avg_dow_cache, os.path.join('test_images', 'avg_dow_0.png'))

# add high number
add_avg(avg_dow_cache, "Wednesday", 2000)

plot_avg_dow(avg_dow_cache, os.path.join('test_images', 'avg_dow_1.png'))

# replace high number with higher number
modify_avg(avg_dow_cache, "Wednesday", 10000, 2000)

plot_avg_dow(avg_dow_cache, os.path.join('test_images', 'avg_dow_2.png'))

remove_avg(avg_dow_cache, "Wednesday", 10000)

plot_avg_dow(avg_dow_cache, os.path.join('test_images', 'avg_dow_3.png'))


print("Testing Price Range by NG")

prc_rng_ng_cache = cache_prc_rng_ng(files)

# initial plot
plot_prc_rng_ng(prc_rng_ng_cache, os.path.join('test_images', 'prc_rng_ng_0.png'))

# add high number
add_rng(prc_rng_ng_cache, "Arganzuela", 2000)

plot_prc_rng_ng(prc_rng_ng_cache, os.path.join('test_images', 'prc_rng_ng_1.png'))

# replace high number with higher number
modify_rng(prc_rng_ng_cache, files, "Arganzuela", 10000, 2000)

plot_prc_rng_ng(prc_rng_ng_cache, os.path.join('test_images', 'prc_rng_ng_2.png'))

remove_rng(prc_rng_ng_cache, files, "Arganzuela", 10000)

plot_prc_rng_ng(prc_rng_ng_cache, os.path.join('test_images', 'prc_rng_ng_3.png'))


print("Testing Average Price by Min Nights")

# create cache
avg_prc_min_nts_cache = cache_avg_prc_min_nts(files)

# initial plot
plot_avg_prc_min_nts(avg_prc_min_nts_cache, os.path.join('test_images', 'avg_prc_min_nts_0.png'))


# add high number entry and re-plot
add_avg(avg_prc_min_nts_cache, "5", 2000)

plot_avg_prc_min_nts(avg_prc_min_nts_cache, os.path.join('test_images', 'avg_prc_min_nts_1.png'))


# replace high number entry with larger and re-plot
modify_avg(avg_prc_min_nts_cache, "5", 5000, 2000)

plot_avg_prc_min_nts(avg_prc_min_nts_cache, os.path.join('test_images', 'avg_prc_min_nts_2.png'))


# remove high number and re-plot; should match avg_prc_min_nts_0.png
remove_avg(avg_prc_min_nts_cache, "5", 5000)

plot_avg_prc_min_nts(avg_prc_min_nts_cache, os.path.join('test_images', 'avg_prc_min_nts_3.png'))
