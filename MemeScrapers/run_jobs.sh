#!/bin/bash -i

computers="phelps porter colden"
lower=10000000
size=200

for c in $computers; do
	upper=$(($lower + size))
	echo $lower $upper $c

	ssh -t $c "cd Courses/298/MemeCaptcha/MemeScrapers; ./scrape.sh $lower $upper $c" < /dev/tty

	lower=$(($lower + size))
done

