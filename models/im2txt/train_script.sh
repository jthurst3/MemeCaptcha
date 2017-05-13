#!/bin/bash
#SBATCH -p gpu
#SBATCH -N 2
#SBATCH --mem=24GB
#SBATCH -t 24:00:00
#SBATCH -o slurm_logs/char_im2txt_train2.out
#SBATCH -e slurm_logs/char_im2txt_train2.err
#SBATCH -J train_char_im2txt
#SBATCH --mail-type=all

IM2TXT_DIR=/public/jthurst3/MemeCaptcha

# Directory containing preprocessed meme data.
MEME_DIR="${IM2TXT_DIR}/character_input_data"

# Inception v3 checkpoint file.
INCEPTION_CHECKPOINT="/scratch/jthurst3/MemeCaptcha/models/im2txt/im2txt/data/inception_v3.ckpt"

# Directory to save the model.
MODEL_DIR="${IM2TXT_DIR}/models/char_im2txt"

# Build the model.
module load tensorflow
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
  --number_of_steps=10000
