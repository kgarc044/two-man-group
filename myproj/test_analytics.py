from analyzer import *
from analytics import * # we need all the functions
from parse_json import read_json
import os
import time
import matplotlib.pyplot as plt


files = {"listings" : read_json(os.path.join(os.path.curdir, 'data', 'listings.json')), "calendar" : read_json(os.path.join(os.path.curdir, 'data', 'calendar.json'))}


print("Average Availability")
tick0 = time.perf_counter()
average_availability(files['listings'])
tock0 = time.perf_counter()

tick1 = time.perf_counter()
avg_avail_cache = cache_avg_avail(files)
plot_avg_avail(avg_avail_cache, "test_images/img.png")
tock1 = time.perf_counter()

tick2 = time.perf_counter()
add_avg(avg_avail_cache, "Centro", 123)
plot_avg_avail(avg_avail_cache, "test_images/img.png")
tock2 = time.perf_counter()

tick3 = time.perf_counter()
modify_avg(avg_avail_cache, "Centro", 456, 123)
plot_avg_avail(avg_avail_cache, "test_images/img.png")
tock3 = time.perf_counter()

tick4 = time.perf_counter()
remove_avg(avg_avail_cache, "Centro", 123)
plot_avg_avail(avg_avail_cache, "test_images/img.png")
tock4 = time.perf_counter()

otime = tock0 - tick0
ctime = tock1 - tick1
atime = tock2 - tick2
mtime = tock3 - tick3
rtime = tock4 - tick4

plt.close('all')

print(f'\tOriginal Function (eval and print): {otime:0.4f}')
print(f'\tNew Functions (eval + print):       {ctime:0.4f} (original {ctime - otime:+0.4f})')
print(f'\tNew Function (add + print):         {atime:0.4f} (original {atime - otime:+0.4f})')
print(f'\tNew Function (modify + print):      {mtime:0.4f} (original {mtime - otime:+0.4f})')
print(f'\tNew Function (remove + print):      {rtime:0.4f} (original {rtime - otime:+0.4f})')


print("Average Price by Day of Week")
tick0 = time.perf_counter()
average_dow_p(files['calendar'])
tock0 = time.perf_counter()

tick1 = time.perf_counter()
avg_dow_cache = cache_avg_dow(files)
plot_avg_dow(avg_dow_cache, "test_images/img.png")
tock1 = time.perf_counter()

tick2 = time.perf_counter()
add_avg(avg_dow_cache, "Monday", 123)
plot_avg_dow(avg_dow_cache, "test_images/img.png")
tock2 = time.perf_counter()

tick3 = time.perf_counter()
modify_avg(avg_dow_cache, "Monday", 456, 123)
plot_avg_dow(avg_dow_cache, "test_images/img.png")
tock3 = time.perf_counter()

tick4 = time.perf_counter()
remove_avg(avg_dow_cache, "Monday", 456)
plot_avg_dow(avg_dow_cache, "test_images/img.png")
tock4 = time.perf_counter()

otime = tock0 - tick0
ctime = tock1 - tick1
atime = tock2 - tick2
mtime = tock3 - tick3
rtime = tock4 - tick4

plt.close('all')

print(f'\tOriginal Function (eval and print): {otime:0.4f}')
print(f'\tNew Functions (eval + print):       {ctime:0.4f} (original {ctime - otime:+0.4f})')
print(f'\tNew Function (add + print):         {atime:0.4f} (original {atime - otime:+0.4f})')
print(f'\tNew Function (modify + print):      {mtime:0.4f} (original {mtime - otime:+0.4f})')
print(f'\tNew Function (remove + print):      {rtime:0.4f} (original {rtime - otime:+0.4f})')

print("Price range by Neighbourhood Group")
tick0 = time.perf_counter()
price_range_ng(files['listings'])
tock0 = time.perf_counter()

tick1 = time.perf_counter()
prc_rng_ng_cache = cache_prc_rng_ng(files)
plot_prc_rng_ng(prc_rng_ng_cache, "test_images/img.png")
tock1 = time.perf_counter()

tick2 = time.perf_counter()
add_rng(prc_rng_ng_cache, "Centro", 123)
plot_prc_rng_ng(prc_rng_ng_cache, "test_images/img.png")
tock2 = time.perf_counter()

tick3 = time.perf_counter()
modify_rng(prc_rng_ng_cache, files, "Centro", 456, 123)
plot_prc_rng_ng(prc_rng_ng_cache, "test_images/img.png")
tock3 = time.perf_counter()

tick4 = time.perf_counter()
remove_rng(prc_rng_ng_cache, files, "Centro", 456)
plot_prc_rng_ng(prc_rng_ng_cache, "test_images/img.png")
tock4 = time.perf_counter()

otime = tock0 - tick0
ctime = tock1 - tick1
atime = tock2 - tick2
mtime = tock3 - tick3
rtime = tock4 - tick4

plt.close('all')

print(f'\tOriginal Function (eval and print): {otime:0.4f}')
print(f'\tNew Functions (eval + print):       {ctime:0.4f} (original {ctime - otime:+0.4f})')
print(f'\tNew Function (add + print):         {atime:0.4f} (original {atime - otime:+0.4f})')
print(f'\tNew Function (modify + print):      {mtime:0.4f} (original {mtime - otime:+0.4f})')
print(f'\tNew Function (remove + print):      {rtime:0.4f} (original {rtime - otime:+0.4f})')

print("Price Distribution by Region")
tick0 = time.perf_counter()
price_distribution_region(files['listings'], "Centro")
tock0 = time.perf_counter()

tick1 = time.perf_counter()
prc_distro_rgn_cache = cache_prc_distro_rgn(files)
plot_prc_distro_rgn(prc_distro_rgn_cache, "Cortes", "test_images/img.png")
tock1 = time.perf_counter()

tick2 = time.perf_counter()
add_distro(prc_distro_rgn_cache, "Cortes", 123)
plot_prc_distro_rgn(prc_distro_rgn_cache, "Cortes", "test_images/img.png")
tock2 = time.perf_counter()

tick3 = time.perf_counter()
modify_distro(prc_distro_rgn_cache, "Cortes", 456, 123)
plot_prc_distro_rgn(prc_distro_rgn_cache, "Cortes", "test_images/img.png")
tock3 = time.perf_counter()

tick4 = time.perf_counter()
remove_distro(prc_distro_rgn_cache, "Cortes", 123)
plot_prc_distro_rgn(prc_distro_rgn_cache, "Cortes", "test_images/img.png")
tock4 = time.perf_counter()

otime = tock0 - tick0
ctime = tock1 - tick1
atime = tock2 - tick2
mtime = tock3 - tick3
rtime = tock4 - tick4

plt.close('all')

print(f'\tOriginal Function (eval and print): {otime:0.4f}')
print(f'\tNew Functions (eval + print):       {ctime:0.4f} (original {ctime - otime:+0.4f})')
print(f'\tNew Function (add + print):         {atime:0.4f} (original {atime - otime:+0.4f})')
print(f'\tNew Function (modify + print):      {mtime:0.4f} (original {mtime - otime:+0.4f})')
print(f'\tNew Function (remove + print):      {rtime:0.4f} (original {rtime - otime:+0.4f})')

print("Average Price by Minimum Nights")
tick0 = time.perf_counter()
average_price_for_min_nights(files['listings'])
tock0 = time.perf_counter()

tick1 = time.perf_counter()
avg_prc_min_nts_cache = cache_avg_prc_min_nts(files)
plot_avg_prc_min_nts(avg_prc_min_nts_cache, "test_images/img.png")
tock1 = time.perf_counter()

tick2 = time.perf_counter()
add_avg(avg_prc_min_nts_cache, "1", 123)
plot_avg_prc_min_nts(avg_prc_min_nts_cache, "test_images/img.png")
tock2 = time.perf_counter()

tick3 = time.perf_counter()
modify_avg(avg_prc_min_nts_cache, "1", 456, 123)
plot_avg_prc_min_nts(avg_prc_min_nts_cache, "test_images/img.png")
tock3 = time.perf_counter()

tick4 = time.perf_counter()
remove_avg(avg_prc_min_nts_cache, "1", 456)
plot_avg_prc_min_nts(avg_prc_min_nts_cache, "test_images/img.png")
tock4 = time.perf_counter()

otime = tock0 - tick0
ctime = tock1 - tick1
atime = tock2 - tick2
mtime = tock3 - tick3
rtime = tock4 - tick4

plt.close('all')

print(f'\tOriginal Function (eval and print): {otime:0.4f}')
print(f'\tNew Functions (eval + print):       {ctime:0.4f} (original {ctime - otime:+0.4f})')
print(f'\tNew Function (add + print):         {atime:0.4f} (original {atime - otime:+0.4f})')
print(f'\tNew Function (modify + print):      {mtime:0.4f} (original {mtime - otime:+0.4f})')
print(f'\tNew Function (remove + print):      {rtime:0.4f} (original {rtime - otime:+0.4f})')

print("Average Price by Season")
tick0 = time.perf_counter()
average_price_season(files['calendar'])
tock0 = time.perf_counter()

tick1 = time.perf_counter()
avg_prc_ssn_cache = cache_avg_prc_ssn(files)
plot_avg_prc_ssn(avg_prc_ssn_cache, "test_images/img.png")
tock1 = time.perf_counter()

tick2 = time.perf_counter()
add_avg(avg_prc_ssn_cache, "Winter", 123)
plot_avg_prc_ssn(avg_prc_ssn_cache, "test_images/img.png")
tock2 = time.perf_counter()

tick3 = time.perf_counter()
modify_avg(avg_prc_ssn_cache, "Winter", 456, 123)
plot_avg_prc_ssn(avg_prc_ssn_cache, "test_images/img.png")
tock3 = time.perf_counter()

tick4 = time.perf_counter()
remove_avg(avg_prc_ssn_cache, "Winter", 456)
plot_avg_prc_ssn(avg_prc_ssn_cache, "test_images/img.png")
tock4 = time.perf_counter()

otime = tock0 - tick0
ctime = tock1 - tick1
atime = tock2 - tick2
mtime = tock3 - tick3
rtime = tock4 - tick4

plt.close('all')

print(f'\tOriginal Function (eval and print): {otime:0.4f}')
print(f'\tNew Functions (eval + print):       {ctime:0.4f} (original {ctime - otime:+0.4f})')
print(f'\tNew Function (add + print):         {atime:0.4f} (original {atime - otime:+0.4f})')
print(f'\tNew Function (modify + print):      {mtime:0.4f} (original {mtime - otime:+0.4f})')
print(f'\tNew Function (remove + print):      {rtime:0.4f} (original {rtime - otime:+0.4f})')
