# converts TSV files containing meme URLs and captions to a JSON file consistent
# with that downloaded/pruned by Tensorflow from the MSCOCO dataset. Structure
# of JSON output: Contains one key 'memes', which contains array of JSON
# objects, each one as follows:
#	'image_id': ID of the image downloaded
#	'top_text': top text of meme
#	'bottom_text': bottom text of meme

import csv
import json
import os
import sys

directory = '/public/jthurst3/MemeCaptcha/data/sharded'
output_file = '/public/jthurst3/MemeCaptcha/cleaned_data/memes.json'

bad_files = ['memegenerator_first_100.tsv',
'memegenerator_armstrong_22000000_23000000aa',
'memegenerator_marshall_29000000_30000000ai',
]
# special = 'memegenerator_armstrong_22000000_23000000.tsv'

# gets a set of all TSV files in a directory, excluding the special one
def get_files(direc):
	files = os.listdir(direc)
	tsv = set(files)
	return tsv.difference(bad_files)

# gets an image ID from its memegenerator URL
def get_id(url):
	return url.split('/')[-1].split('.')[0]

# gets top text
def top_text(t):
	if t == '(no top text)':
		return ""
	return t

# gets bottom text
def bottom_text(t):
	# note no closing parenthesis because I was stupid when downloading and
	# parsing memes to TSV. See GitHub issue #5.
	if t == '(no bottom text':
		return ""
	return t

# given a TSV file, appends entries to the big JSON object j
# assumes f is a file path, so we need to open it.
def append_entries(j, path):
	memes = j['memes']
	f = open(path, 'rU')
	reader = csv.reader(f, delimiter='\t')
	counter = 0
	badcounter = 0
	for row in reader:
		counter += 1
		if len(row) < 3:
			# print("ROW SMALL", row)
			badcounter += 1
			continue
		jo = {}
		jo['image_id'] = get_id(row[0])
		jo['top_text'] = top_text(row[1])
		jo['bottom_text'] = bottom_text(row[2])
		memes.append(jo)
	print("finished appending from ", path, "bad entries", badcounter,
			"total entries", counter, "success",
			float(counter-badcounter)/counter)
	return j

# main method: create JSON file
def create_JSON():
	# warn user if we already created JSON file
	if os.path.exists(output_file):
		print('Output file exists. Please remove before running.')
		sys.exit(1)
	# otherwise, continue
	out = open(output_file, 'w')
	j = {}
	j['memes'] = []
	files = [os.path.join(directory, f) for f in get_files(directory)]
	# testing
	files = [os.path.join(directory, 'memegenerator_marshall_29000000_30000000aa')]
	for f in files:
		print("starting from ", f)
		append_entries(j, f)
	json.dump(j, out)
	
if __name__ == '__main__':
	create_JSON()


