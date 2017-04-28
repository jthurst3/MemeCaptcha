#!/bin/bash
#SBATCH -p standard
#SBATCH -N 1
#SBATCH -a 1-25
#SBATCH -t 10:00:00
#SBATCH --mem-per-cpu=50GB
#SBATCH  --ntasks-per-node 4
#SBATCH -o extract_text_features_reduced.log
#SBATCH -e extract_text_features_reduced.error
#SBATCH -J extract_text_features_reduced
#SBATCH --mail-type=all


# ./setup_env_for_mvn.sh
# mvn package

######### same as in create_top_bottom_files.sh ######### 
# FILES=/public/jthurst3/MemeCaptcha/data/*.tsv
# for f in $FILES
# do
#   echo "Processing $f file..."
#   # take action on each file. $f store current file name
#   f2=$(echo $f | grep -oE "[^/]+$")
#   topfile="${f2//.tsv/_top.tsv}" 
#   awk 'BEGIN{FS="\t"}{print $2}' $f > "data/$topfile"
#   bottomfile="${f2//.tsv/_bottom.tsv}"
#   awk 'BEGIN{FS="\t"}{print $2}' $f > "data/$bottomfile"
#   echo "/public/tkhunkhe/MemeCaptcha/FeatureExtraction/text-features/data/$topfile" >> topfileList.txt
#   echo "/public/tkhunkhe/MemeCaptcha/FeatureExtraction/text-features/data/$bottomfile" >> bottomfileList.txt
# #/public/jthurst3/MemeCaptcha/data/memegenerator_algonquin_21000000_22000000.tsv
# done

module load java # this is very important for some parsers to work
module load python


topfile=$(sed "${SLURM_ARRAY_TASK_ID}q;d" "topfileList.txt")
tf2=$(echo $topfile | grep -oE "[^/]+$")
topfile2="${tf2//.tsv/_features_reduced.tsv}" 
bottomfile=$(sed "${SLURM_ARRAY_TASK_ID}q;d" "bottomfileList.txt")
bf2=$(echo $bottomfile | grep -oE "[^/]+$")
bottomfile2="${bf2//.tsv/_features_reduced.tsv}"
 
echo "-------- processing $topfile ----------" 
python extract_text_features_reduced.py ${topfile} "results/$topfile2"
echo "-------- processing $bottomfile ----------" 
python extract_text_features_reduced.py ${bottomfile} "results/$bottomfile2"
bothfile="${topfile2//_top.tsv/_both_features_reduced.tsv}" 
paste "results/$topfile2" "results/$bottomfile2" > "results/$bothfile"


