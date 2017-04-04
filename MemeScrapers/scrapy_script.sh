#!/bin/bash

dir=/scratch/MemeCaptcha
base="$dir/data/memegenerator_$3_$1_$2"
txtfile="$base.txt"
tsvfile="$base.tsv"
picturefile="$base.pictures"

scrapy crawl memegenerator -a lower=$1 -a upper=$2 -a filename=$txtfile
./get_images.py $txtfile "$dir/images" $tsvfile > $picturefile
xz $txtfile

