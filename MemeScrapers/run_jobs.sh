#!/bin/bash -i

computers="blake cascade colden macomb marcy nye phelps porter sawteeth seward tabletop algonquin armstrong cliff colvin gothics haystack hough iroquois marshall panther redfield skylight whiteface wright"
lower=35000000
size=1000000

for c in $computers; do
	upper=$(($lower + size))
	echo $c $lower $upper

	ssh -t $c "cd Courses/298/MemeCaptcha/MemeScrapers; ./scrape.sh $lower $upper $c" < /dev/tty
	if [ $? -eq 0 ]; then
		echo "$c $lower $upper" >> current_run.txt
	else
		echo "$c $lower $upper FAILED TO START" >> current_run.txt
	fi

	lower=$(($lower + size))
done

