import re # regexs
import json
import ujson
import tarfile

#pattern = r",(?=(?:[^\"]*\"[^\"]*\")*[^\"]*$)" # listings.csv
pattern = r",|,\$" # calendar.csv

# read csv file and return list of dict
# tool, not used in code
def csv_to_dict(in_file, comma_regex):
    
    f = open(in_file, 'r')
    
    fieldnames = f.readline().rstrip().split(',')
    lines = f.readlines()
    
    f.close
    
    entries = []

    for line in lines:
        element = {}
        fields = re.split(comma_regex, line.rstrip())
        for i in range(len(fieldnames)):
            element[fieldnames[i]] = fields[i]
        entries.append(element)
    
    return entries

# list-of-dict to json
# used to re-write data back to json, might replace with write to CSV for size
def dict_to_json(data, out_file):
    
    # open file as append
    f = open(out_file, 'w')
    
    for entry in data:   
        json.dump(entry, f)
        f.write('\n')
    
    f.close()

# reads given JSON file to list of dict
def read_json(file):
    f = open(file, 'r')
    
    entries = []
    for line in f:
        entries.append(ujson.loads(line))
    
    return entries

# json.tar.gz to list-of-dict
# not used, can't find how to re-compress files, just read from *.json
def read_compressed_json(tarball, file):
    
    # open file to read
    f = tarfile.open(tarball, 'r:gz').extractfile(file)
    
    entries = []

    for line in f:
        entries.append(json.loads(line))
    
    f.close()

    return entries
