# splits data into training and validation sets.

import json
import os
import random
import sys

# percent of images to be in the training set
train_percent = 0.66

base_directory = '/public/jthurst3/MemeCaptcha'
image_directory = base_directory + '/images'
input_directory = base_directory + '/cleaned_data'
output_directory = base_directory + '/tensorflow_input_data'

# gets all files in a directory that end with something
def get_files(direc, end):
	files = os.listdir(direc)
	return [f for f in files if f.endswith(end)]

# splits images up into a set of training ones and a set of validation ones
def split_images(image_dir):
	images = get_files(image_dir, '.json')
	# shuffle the images
	random.shuffle(images)
	cutoff = int(len(images)*train_percent)
	train_images = images[:cutoff]
	val_images = images[cutoff:]
	return set(train_images), set(val_images)

# given a set of images, writes a JSON object to a file with all image-caption pairs that
# contain images in the set, from an original list of JSON files.
def write_JSON(image_set, input_json_files, filename):
	j = {}
	j['memes'] = []
	j['images'] = list(image_set)
	memes = j['memes']
	for jfile in json_files:
		with open(os.path.join(input_directory, jfile), 'r') as f:
			# each input JSON file will be in the same format as the
			# output JSON file
			caption_data = json.load(f)
			caption_memes = caption_data['memes']
			for meme in caption_memes:
				if meme['image_url'] in image_set:
					memes.append(meme)
	# write it to the output file
	with open(filename, 'w') as f:
		json.dump(j, f)

# main method: partition data set
def partition_dataset():
	# check if either output file exists. Return an error message if so.
	train_file = os.path.join(output_directory, "train.json")
	validation_file = os.path.join(output_directory, "val.json")
	for f in [train_file, validation_file]:
		if os.path.exists(f):
			print("File ", f, "already exists. Please remove \
			before running.")
			sys.exit(1)
	train_images, val_images = split_images(image_directory)
	input_files = get_files(input_directory, '.json')
	write_JSON(train_images, input_files, 'train.json')
	write_JSON(val_images, input_files, 'val.json')

if __name__ == '__main__':
	partition_dataset()


