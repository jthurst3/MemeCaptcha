# converts TXT files containing JSON downloaded from memegenerator.net API to a JSON file consistent
# with that downloaded/pruned by Tensorflow from the MSCOCO dataset. Structure
# of JSON output: Contains one key 'memes', which contains array of JSON
# objects, each one as follows:
#	'id': ID of the meme (directly taken from memegenerator, unique)
#	'image_id': ID of the image downloaded
#	'top_text': top text of meme
#	'bottom_text': bottom text of meme
#	'upvotes': number of upvotes (measure of popularity)

import csv
import json
import os
import subprocess
import sys
import traceback

data_directory = '/public/jthurst3/MemeCaptcha/data'
output_directory = '/public/jthurst3/MemeCaptcha/new_cleaned_data'

required_keys = ['text0','text1','instanceID','imageUrl']

# special = 'memegenerator_armstrong_22000000_23000000.tsv'

# returns true if all characters in a string are ascii
# from http://stackoverflow.com/questions/196345/how-to-check-if-a-string-in-python-is-in-ascii
def is_ascii(s):
    if s:
        return all(ord(c) < 128 for c in s)
    return True

# gets a set of all TSV files in a directory, excluding the special one
def get_files(direc):
	files = os.listdir(direc)
	files = set([f for f in files if f.endswith('.txt.xz')])
	return files

# gets an image ID from its memegenerator URL
def get_image_id(url):
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

# returns a big JSON object j corresponding to the entries in the text file f
# assumes f is a File, already opened.
def get_entries(f):
	j = {}
	j['memes'] = []
	memes = j['memes']
	counter = 0
	badcounter = 0
	for row in f:
		counter += 1
		row = json.loads(row)
		if any([key not in row for key in required_keys]):
			print("ROW INVALID", row)
			badcounter += 1
			continue
		if not is_ascii(row['text0']) or not is_ascii(row['text1']):
			badcounter += 1
			continue
		jo = {}
		jo['id'] = row['instanceID']
		jo['image_id'] = get_image_id(row['imageUrl'])
		jo['top_text'] = row['text0'] or ''
		jo['bottom_text'] = row['text1'] or ''
		if 'totalVotesScore' not in row:
			jo['upvotes'] = 0
		else:
			jo['upvotes'] = int(row['totalVotesScore'])
		memes.append(jo)
	print("finished appending from ", f, "bad entries", badcounter,
			"total entries", counter, "success",
			float(counter-badcounter)/counter)
	return j

# main method: create JSON file
def create_JSON():
	# warn user if we already created JSON file
	# if os.path.exists(output_file):
		# print('Output file exists. Please remove before running.')
		# sys.exit(1)
	# otherwise, continue
	# files = [os.path.join(directory, f) for f in get_files(directory)]
	files = get_files(data_directory)
	output_files = [f.split('.txt.xz')[0]+'.json' for f in files]
	iters = 0
	for (infile, outfile) in zip(files, output_files):
		if infile.count('tabletop') > 0:
			continue
		iters += 1
		print(infile, outfile)
		infile = os.path.join(data_directory, infile)
		outfile = os.path.join(output_directory, outfile)
		if os.path.exists(outfile):
			continue
		try:
			subprocess.call(['xz','-d', infile])
			print("decompressed", infile)
			f = open(infile.split('.xz')[0], 'rU')
			out = open(outfile, 'w')
			j = get_entries(f)
			json.dump(j, out)
			print("dumped to output file", outfile)
		except:
			print("failed to parse file", f)
			print(sys.exc_info())
			traceback.print_tb(sys.exc_info()[2])
		finally:
			subprocess.call(['xz','-T0',infile.split('.xz')[0]])
			print("compressed", infile)

	
if __name__ == '__main__':
	create_JSON()


