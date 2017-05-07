#!/bin/bash
#SBATCH -p gpu
#SBATCH -N 2
#SBATCH --mem=10GB
#SBATCH -t 10:00:00
#SBATCH -o slurm_logs/first_evaluation.out
#SBATCH -e slurm_logs/first_evaluation.err
#SBATCH -J first_evaluation
#SBATCH --mail-type=all

module load caffe
IM2TXT_DIR=/public/jthurst3/MemeCaptcha

MEME_DIR="${IM2TXT_DIR}/tensorflow_input_data"
MODEL_DIR="${IM2TXT_DIR}/models/cnn_lstm_run1"

# Ignore GPU devices (only necessary if your GPU is currently memory
# constrained, for example, by running the training script).
#export CUDA_VISIBLE_DEVICES=""

# TODO: take this out, only for making sure we have data before evaluating
sleep 60

# Run the evaluation script. This will run in a loop, periodically loading the
# latest model checkpoint file and computing evaluation metrics.
bazel-bin/im2txt/evaluate \
  --input_file_pattern="${MEME_DIR}/val-?????-of-00004" \
  --checkpoint_dir="${MODEL_DIR}/train" \
  --eval_dir="${MODEL_DIR}/eval"
