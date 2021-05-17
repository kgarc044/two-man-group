from analytics import * # we need all the functions
from parse_json import read_json
import os


files = {"listings" : read_json(os.path.join(os.path.curdir, 'data', 'test_listings.json')), "calendar" : read_json(os.path.join(os.path.curdir, 'data', 'test_calendar.json'))}

# print("Testing average_availability")

avg_prc_ssn_cache = cache_avg_prc_ssn(files)
plot_avg_prc_ssn(avg_prc_ssn_cache, os.path.join('test_images', 'avg_prc_ssn_0.png'))
print(avg_prc_ssn_cache)

add_avg(avg_prc_ssn_cache, 'Winter', 5000)
plot_avg_prc_ssn(avg_prc_ssn_cache, os.path.join('test_images', 'avg_prc_ssn_1.png'))
print(avg_prc_ssn_cache)

modify_avg(avg_prc_ssn_cache, 'Winter', 10000, 5000)
plot_avg_prc_ssn(avg_prc_ssn_cache, os.path.join('test_images', 'avg_prc_ssn_2.png'))
print(avg_prc_ssn_cache)

remove_avg(avg_prc_ssn_cache, 'Winter', 10000)
plot_avg_prc_ssn(avg_prc_ssn_cache, os.path.join('test_images', 'avg_prc_ssn_3.png'))
print(avg_prc_ssn_cache)

# prc_distro_cache = {}
# prc_distro_cache = cache_prc_distro_rgn(prc_distro_cache, files, 'Universidad')
# plot_prc_distro_rgn(prc_distro_cache, 'Universidad', os.path.join('test_images', 'avg_distro_rng_0.png'))
# print(prc_distro_cache)

# add_distro(prc_distro_cache, 'Universidad', 500)
# plot_prc_distro_rgn(prc_distro_cache, 'Universidad', os.path.join('test_images', 'avg_distro_rng_1.png'))
# print(prc_distro_cache)

# add_distro(prc_distro_cache, 'Universidad', 50)
# plot_prc_distro_rgn(prc_distro_cache, 'Universidad', os.path.join('test_images', 'avg_distro_rng_2.png'))
# print(prc_distro_cache)

# add_new_distro(prc_distro_cache, files, 'Palacio')
# plot_prc_distro_rgn(prc_distro_cache, 'Palacio', os.path.join('test_images', 'avg_distro_rng_3.png'))
# print(prc_distro_cache)

# modify_distro(prc_distro_cache, 'Palacio', 500, 40)
# plot_prc_distro_rgn(prc_distro_cache, 'Palacio', os.path.join('test_images', 'avg_distro_rng_4.png'))
# print(prc_distro_cache)

# remove_distro(prc_distro_cache, 'Universidad', 500)
# plot_prc_distro_rgn(prc_distro_cache, 'Universidad', os.path.join('test_images', 'avg_distro_rng_5.png'))
# print(prc_distro_cache)

# create cache
# avg_avail_cache = cache_avg_avail(files)

# # initial plot
# plot_avg_avail(avg_avail_cache, os.path.join('test_images', 'avg_avail_0.png'))


# # add high number entry and re-plot
# add_avg(avg_avail_cache, "Arganzuela", 2000)

# plot_avg_avail(avg_avail_cache, os.path.join('test_images', 'avg_avail_1.png'))


# # replace high number entry with larger and re-plot
# modify_avg(avg_avail_cache, "Arganzuela", 5000, 2000)

# plot_avg_avail(avg_avail_cache, os.path.join('test_images', 'avg_avail_2.png'))


# # remove high number and re-plot; should match avg_avail_0.png
# remove_avg(avg_avail_cache, "Arganzuela", 5000)

# plot_avg_avail(avg_avail_cache, os.path.join('test_images', 'avg_avail_3.png'))
