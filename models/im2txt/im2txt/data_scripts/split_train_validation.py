# splits data into training and validation sets.

import json
import os
import random
import sys

# percent of images to be in the training set
train_percent = 0.66
# max number of captions per meme (ranked in order of popularity, ties broken
# arbitrarily
max_captions_per_meme = 5

base_directory = '/public/jthurst3/MemeCaptcha'
image_directory = base_directory + '/images'
input_directory = base_directory + '/new_cleaned_data'
output_directory = base_directory + '/tensorflow_input_data'

# gets all files in a directory that end with something
def get_files(direc, end):
	files = os.listdir(direc)
	return [f for f in files if f.endswith(end)]

# splits images up into a set of training ones and a set of validation ones
def split_images(image_dir):
	print("splitting images")
	images = get_files(image_dir, '.jpg')
	images = [i.split('.jpg')[0] for i in images]
	# shuffle the images
	random.shuffle(images)
	cutoff = int(len(images)*train_percent)
	train_images = images[:cutoff]
	val_images = images[cutoff:]
	return set(train_images), set(val_images)

# gets image split from train.images and val.images
def get_image_split(output_dir):
	print("getting existing split from train.images and val.images")
	train_images = set()
	val_images = set()
	with open(os.path.join(output_dir, 'train.images'), 'r') as f:
		train_images = set([s.strip() for s in f])
	with open(os.path.join(output_dir, 'val.images'), 'r') as f:
		val_images = set([s.strip() for s in f])
	return train_images, val_images


# given a set of images, writes a JSON object to a file with all image-caption pairs that
# contain images in the set, from an original list of JSON files.
# For each image, only take the 5-most highly ranked memes in the data set
def write_JSON(image_set, input_json_files, filename):
	j = {}
	j['memes'] = []
	j['images'] = list(image_set)
	memes = j['memes']
	# dictionary of image --> list<meme>. List can only be of length n,
	# where n is the maximum number of captions per image.
	top_n_meme_list = {}
	for image in image_set:
		top_n_meme_list[image] = []
	for jfile in input_json_files:
		print("on file", jfile)
		with open(os.path.join(input_directory, jfile), 'rU') as f:
			# each input JSON file will be in the same format as the
			# output JSON file
			caption_data = json.load(f)
			caption_memes = caption_data['memes']
			for meme in caption_memes:
				if meme['image_id'] in image_set:
					# append to top_n_meme_list in first
					# pass, then filter later
					top_n_meme_list[meme['image_id']].append(meme)
		print("finished reading from", jfile)
	# filter top_n_meme_list to only take max n captions per image
	for image in top_n_meme_list:
		meme_list = top_n_meme_list[image]
		meme_list.sort(key=lambda x: x['upvotes'], reverse=True)
		meme_list = meme_list[:max_captions_per_meme]
		memes.extend(meme_list)
	# write it to the output file
	with open(filename, 'w') as f:
		json.dump(j, f)

# main method: partition data set
def partition_dataset():
	# check if either output file exists. Return an error message if so.
	train_file = os.path.join(output_directory, "train.json")
	validation_file = os.path.join(output_directory, "val.json")
	train_images_file = os.path.join(output_directory, "train.images")
	validation_images_file = os.path.join(output_directory, "val.images")
	files_exist = False
	for f in [train_file, validation_file, train_images_file,
			validation_images_file]:
		if os.path.exists(f):
			files_exist = True
			# print("File ", f, "already exists. Please remove before running.")
			# sys.exit(1)
	if files_exist:
		train_images, val_images = get_image_split(output_directory)
	else:
		train_images, val_images = split_images(image_dir)
	input_files = get_files(input_directory, '.json')
	write_JSON(train_images, input_files, train_file)
	write_JSON(val_images, input_files, validation_file)
	# record image partition to files
	with open(train_images_file, 'w') as f:
		for image in train_images:
			f.write(image + '\n')
	with open(validation_images_file, 'w') as f:
		for image in val_images:
			f.write(image + '\n')

if __name__ == '__main__':
	partition_dataset()


