#!/bin/bash -i

computers="blake cascade colden macomb marcy nye phelps porter sawteeth seward tabletop algonquin armstrong cliff colvin gothics haystack hough iroquois marshall panther redfield skylight whiteface wright"
lower=10000000
size=1000000

for c in $computers; do
	upper=$(($lower + size))
	echo $lower $upper $c

	ssh -t $c "cd Courses/298/MemeCaptcha/MemeScrapers; ./scrape.sh $lower $upper $c" < /dev/tty

	lower=$(($lower + size))
done

