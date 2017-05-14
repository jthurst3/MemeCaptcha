#!/bin/bash
#SBATCH -p gpu
#SBATCH -N 1
#SBATCH --mem=16GB
#SBATCH -t 10:00:00
#SBATCH -o slurm_logs/evaluate_im2txt_min_1.out
#SBATCH -e slurm_logs/evaluate_im2txt_min_1.err
#SBATCH -J evaluate_min1
#SBATCH --mail-type=all

IM2TXT_DIR=/public/jthurst3/MemeCaptcha

MEME_DIR="${IM2TXT_DIR}/tensorflow_input_data_min1"
MODEL_DIR="${IM2TXT_DIR}/models/im2txt_min_1"

# Ignore GPU devices (only necessary if your GPU is currently memory
# constrained, for example, by running the training script).
#export CUDA_VISIBLE_DEVICES=""

# modified from https://superuser.com/questions/878640/unix-script-wait-until-a-file-exists
until [ -f "${MODEL_DIR}/train/checkpoint" ]; do
	sleep 60
done

# Run the evaluation script. This will run in a loop, periodically loading the
# latest model checkpoint file and computing evaluation metrics.
bazel-bin/im2txt/evaluate \
  --input_file_pattern="${MEME_DIR}/val-?????-of-00004" \
  --checkpoint_dir="${MODEL_DIR}/train" \
  --eval_dir="${MODEL_DIR}/eval" \
  --min_global_step="500" \
