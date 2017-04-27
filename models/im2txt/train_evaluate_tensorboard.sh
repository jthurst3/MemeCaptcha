#!/bin/bash

jid1text=$(sbatch train_script.sh)
jid1=$(echo $jid2text | awk -F' ' '{print $4}')

#jid2text=$(sbatch --dependency=after:"$jid1" evaluation_script.sh)
echo "sbatch --dependency=after:$jid1 evaluation_script.sh"
jid2=$(echo $jid2text | awk -F' ' '{print $4}')
echo $jid2

#sbatch tensorboard_server.sh

#jid3text=$(sbatch --dependency=after:"$jid1" evaluation_script.sh)
#jid3=$(echo $jid2text | awk -F' ' '{print $4}')

