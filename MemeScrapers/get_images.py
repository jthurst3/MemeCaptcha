#!/usr/bin/env python

# given a txt file containing JSON output from memegenerator.net,
# downloads all images referenced in the .txt file to the images/ folder,
# and prints out a TSV-formatted output where each line contains an image url,
# top text, and bottom text.

# To run: $ ./get_images.py <json_file> <image_folder> <tsv_file>, where
#   - <json_file> is a txt file containing JSON output from memegenerator.net
#   - <image_folder> is the folder where you want to store the images
#   - <tsv_file> is the output file you want to have TSV data stored
# e.g.    $ ./get_images.py ../scrape_output/memes_id.txt ../images ../scrape_output/memes_id.tsv

import sys
import json
import os

# from http://stackoverflow.com/questions/196345/how-to-check-if-a-string-in-python-is-in-ascii
def is_ascii(s):
    if s:
        return all(ord(c) < 128 for c in s)
    return True

def get_images(filename, folder, tsvfile, dry_run=False):
    memes = {}
    with open(filename, 'r') as f:
        for line in f:
            j = json.loads(line)
            url = j['imageUrl']
            top = j['text0']
            bottom = j['text1']
            # quick "english" check
            if url and is_ascii(top) and is_ascii(bottom):
                if url not in memes:
                    memes[url] = []
                memes[url].append([(top or '(no top text)'), (bottom or '(no bottom text')])

    # list of images already gotten (check by filename)
    existing_images = os.listdir(folder)
    with open(tsvfile, 'w') as f:
        for meme in memes:
            # get meme from online and put it in images/ folder
            if image_filename(meme) not in existing_images:
                if not dry_run:
                    get_image(meme)
                print meme
                sys.stdout.flush()
            for text in memes[meme]:
                f.write(meme + '\t' + text[0] + '\t' + text[1] + '\n')

def image_filename(image):
    return image.split('/')[-1]

def get_image(url):
    filename = image_filename(url)
    os.system('curl ' + url + ' >> ' + folder + filename + ' 2>/dev/null')

if __name__ == '__main__':
    datafile = sys.argv[1]
    folder = sys.argv[2]
    if not folder.endswith('/'):
        folder += '/'
    tsvfile = sys.argv[3]
    dry_run = False
    if len(sys.argv) == 5 and sys.argv[4] == '--dry-run':
        dry_run = True
    if not os.path.exists(folder):
        os.mkdir(folder)
    get_images(datafile, folder, tsvfile, dry_run=dry_run)
