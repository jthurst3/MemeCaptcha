#!/bin/bash -i

tmux new-session -s scrape -d
tmux send -t scrape.0 "cd ~/Courses/298/MemeCaptcha/MemeScrapers" ENTER
tmux send -t scrape.0 "./scrapy_script.sh $1 $2 $3" ENTER

