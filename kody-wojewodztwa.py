import re
import csv
from sys import argv

"""
The aim of this little, but handy tool is to help a user that wants to map a polish zipcode to the name of a voivodship ( a polenglish name for a county).
MIT license applies (so feel free to do wtf you want with this)
The data about mapping between zipcodes and voivodships:
http://pl.wikisource.org/wiki/Kody_pocztowe_-_zredukowane_mapowanie_kod_-_wojew%C3%B3dztwo
"""



"""
This functions expects a zipcode and a list of mapping in a form of:
02-***
01-5**
And matches the FIRST regex spotted. So the sorting of a map file should begin with the most detailed cases, and go on till for example **-***, depending on the data
"""
def get_voiv(zipcode, mapping):
	voivodship = "unmatched"
	for regex in list(mapping):
		regex_str = re.sub('\*','[0-9]', regex)
		reg = re.compile(regex_str)
		if reg.match(zipcode):
			voivodship = mapping[regex]
			return voivodship
	return voivodship
"""
This just opens a mapfile and returns a dict (first row as a key, second as a value, so the example row looks like: '02-7**;mazowieckie')
"""
def read_mapping():
	mapfile = open("mapfile.csv","r")
	reader = csv.reader(mapfile,delimiter=",")
	map = dict()
	for row in reader:
		map[row[0]] = row[1]
	mapfile.close()
	return map


#script, filename, which_column = argv
"""
The "main" function: reads the mapping, the data file and iterating through each row, returns a matching voivodship
"""
def map_zipcodes(filename, which_column):
	try:
		which_column = int(which_column)
	except ValueError:
		print "A column should be an integer (0 - first column)"
	mapping = read_mapping()
	fileh = open(filename,"r")
	reader = csv.reader(fileh, delimiter=";")
	for row in reader:
		row.append(get_voiv(row[which_column], mapping))
		print ";".join(row)

"""
Starts it up.
"""
script, filename, which_column = argv
data = map_zipcodes(filename, which_column)



