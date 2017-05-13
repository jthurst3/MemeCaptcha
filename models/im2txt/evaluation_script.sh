#!/bin/bash
#SBATCH -p gpu
#SBATCH -N 1
#SBATCH --mem=16GB
#SBATCH -t 24:00:00
#SBATCH -o slurm_logs/char_im2txt_evaluation1.out
#SBATCH -e slurm_logs/char_im2txt_evaluation1.err
#SBATCH -J evaluation_im2txt_min_1
#SBATCH --mail-type=all

IM2TXT_DIR=/public/jthurst3/MemeCaptcha

MEME_DIR="${IM2TXT_DIR}/character_input_data"
MODEL_DIR="${IM2TXT_DIR}/models/char_im2txt"

# Ignore GPU devices (only necessary if your GPU is currently memory
# constrained, for example, by running the training script).
#export CUDA_VISIBLE_DEVICES=""

# modified from https://superuser.com/questions/878640/unix-script-wait-until-a-file-exists
until [ -f "${MODEL_DIR}/train/checkpoint" ]; do
	sleep 60
done

#module load tensorflow

# Run the evaluation script. This will run in a loop, periodically loading the
# latest model checkpoint file and computing evaluation metrics.
bazel-bin/im2txt/evaluate \
  --input_file_pattern="${MEME_DIR}/val-?????-of-00004" \
  --checkpoint_dir="${MODEL_DIR}/train" \
  --eval_dir="${MODEL_DIR}/eval"
