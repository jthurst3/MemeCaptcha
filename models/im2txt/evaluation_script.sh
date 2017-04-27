#!/bin/bash
#SBATCH -p gpu
#SBATCH -N 2
#SBATCH --mem-per-cpu=1GB
#SBATCH -t 10:00:00
#SBATCH -o slurm_logs/first_evaluation.out
#SBATCH -e slurm_logs/first_evaluation.err
#SBATCH -J first_evaluation
#SBATCH --mail-type=all

IM2TXT_DIR=/scratch/jthurst3/MemeCaptcha/models/im2txt

MEME_DIR="${IM2TXT_DIR}/im2txt/data"
MODEL_DIR="${IM2TXT_DIR}/im2txt/model"

# Ignore GPU devices (only necessary if your GPU is currently memory
# constrained, for example, by running the training script).
#export CUDA_VISIBLE_DEVICES=""

# TODO: take this out, only for making sure we have data before evaluating
sleep 60

# Run the evaluation script. This will run in a loop, periodically loading the
# latest model checkpoint file and computing evaluation metrics.
bazel-bin/im2txt/evaluate \
  --input_file_pattern="${IM2TXT_DIR}/val-?????-of-00004" \
  --checkpoint_dir="${MODEL_DIR}/train" \
  --eval_dir="${MODEL_DIR}/eval"
