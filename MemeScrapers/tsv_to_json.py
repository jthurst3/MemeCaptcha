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

directory = '/public/jthurst3/MemeCaptcha/data'
output_file = '/public/jthurst3/MemeCaptcha/cleaned_data/first_100.json'

special = 'memegenerator_first_100.tsv'

# gets a set of all TSV files in a directory, excluding the special one
def get_files(direc):
	files = os.listdir(direc)
	tsv = set([f for f in files if f.endswith('.tsv')])
	if special in tsv:
		tsv.remove(special)
	return tsv

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
	f = open(path, 'r')
	reader = csv.reader(f, delimiter='\t')
	for row in reader:
		jo = {}
		jo['image_id'] = get_id(row[0])
		jo['top_text'] = top_text(row[1])
		jo['bottom_text'] = bottom_text(row[2])
		memes.append(jo)
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
	# files = get_files(directory)
	# testing
	files = [os.path.join(directory, special)]
	for f in files:
		append_entries(j, f)
	json.dump(j, out)
	
if __name__ == '__main__':
	create_JSON()


