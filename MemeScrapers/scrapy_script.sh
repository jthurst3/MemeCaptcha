#!/bin/bash

dir=/scratch/MemeCaptcha
base="$dir/data/memegenerator_$3_$1_$2"
txtfile="$base.txt"
tsvfile="$base.tsv"
picturefile="$base.pictures"

scrapy crawl memegenerator -a lower=$1 -a upper=$2 -a filename=$txtfile
./get_images.py $txtfile "$dir/images" $tsvfile > $picturefile
xz $txtfile
/usr/sbin/sendmail jthurst3@u.rochester.edu <<-EOF
subject:[MemeCaptcha automatic message] Scrape status for $3:
from:scrapy@$3.csug.rochester.edu
Done getting images and compressing for $3.
EOF


