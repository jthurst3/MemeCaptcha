#!/bin/bash
#SBATCH -p gpu
#SBATCH -N 2
#SBATCH --mem=24GB
#SBATCH -t 10:00:00
#SBATCH -o slurm_logs/train_im2txt_min_1.out
#SBATCH -e slurm_logs/train_im2txt_min_1.err
#SBATCH -J train_min1
#SBATCH --mail-type=all

IM2TXT_DIR=/public/jthurst3/MemeCaptcha

# Directory containing preprocessed meme data.
MEME_DIR="${IM2TXT_DIR}/tensorflow_input_data_min1"

# Inception v3 checkpoint file.
INCEPTION_CHECKPOINT="/scratch/jthurst3/MemeCaptcha/models/im2txt/im2txt/data/inception_v3.ckpt"

# Directory to save the model.
MODEL_DIR="${IM2TXT_DIR}/models/im2txt_min_1"

# Build the model.
module load bazel
bazel build -c opt im2txt/...

echo $IM2TXT_DIR $MEME_DIR $INCEPTION_CHECKPOINT $MODEL_DIR

#cd im2txt

# Run the training script.
#python im2txt/train.py \
bazel-bin/im2txt/train \
  --input_file_pattern="${MEME_DIR}/train-?????-of-00256" \
  --inception_checkpoint_file="${INCEPTION_CHECKPOINT}" \
  --train_dir="${MODEL_DIR}/train" \
  --train_inception=false \
  --max_checkpoints_to_keep=1000000 \
  --number_of_steps=1000000
