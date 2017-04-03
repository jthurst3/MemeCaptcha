#!/usr/bin/env python

import sys
import json
import os

# from http://stackoverflow.com/questions/196345/how-to-check-if-a-string-in-python-is-in-ascii
def is_ascii(s):
    return all(ord(c) < 128 for c in s)


def get_images(filename):
    memes = {}
    with open(filename, 'r') as f:
        for line in f:
            j = json.loads(line)
            url = j['imageUrl']
            top = j['text0']
            bottom = j['text1']
            # quick "english" check
            if is_ascii(top) and is_ascii(bottom):
                if url not in memes:
                    memes[url] = []
                memes[url].append([top, bottom])

    # list of images already gotten (check by filename)
    existing_images = os.listdir('../images/')
    for meme in memes:
        # get meme from online and put it in images/ folder
        if image_filename(meme) not in existing_images:
            get_image(meme)
        for text in memes[meme]:
            print meme + '\t' + text[0] + '\t' + text[1]

def image_filename(image):
    return image.split('/')[-1]

def get_image(url):
    filename = image_filename(url)
    os.system('curl ' + url + ' >> ../images/' + filename)

if __name__ == '__main__':
    if 'images' not in os.listdir('..'):
        os.mkdir('../images')
    get_images(sys.argv[1])
