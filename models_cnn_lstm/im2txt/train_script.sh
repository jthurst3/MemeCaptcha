#!/bin/bash
#SBATCH -p gpu
#SBATCH -N 2
#SBATCH --mem=10GB
#SBATCH -t 10:00:00
#SBATCH -o slurm_logs/first_train.out
#SBATCH -e slurm_logs/first_train.err
#SBATCH -J first_train
#SBATCH --mail-type=all

module load caffe
IM2TXT_DIR=/public/jthurst3/MemeCaptcha

# Directory containing preprocessed meme data.
MEME_DIR="${IM2TXT_DIR}/tensorflow_input_data"

# Inception v3 checkpoint file.
INCEPTION_CHECKPOINT="${IM2TXT_DIR}/checkpoints/inception_v3.ckpt"

# Directory to save the model.
MODEL_DIR="${IM2TXT_DIR}/models/cnn_lstm_run1"

# Build the model.
module load bazel
bazel build -c opt im2txt/...

echo $IM2TXT_DIR $MEME_DIR $INCEPTION_CHECKPOINT $MODEL_DIR

#cd im2txt

# Run the training script. Not training inception.
#python im2txt/train.py \
bazel-bin/im2txt/train \
  --input_file_pattern="${MEME_DIR}/train-?????-of-00256" \
  --inception_checkpoint_file="${INCEPTION_CHECKPOINT}" \
  --train_dir="${MODEL_DIR}/train" \
  --train_inception=false \
  --number_of_steps=1000000

#training inception.
# bazel-bin/im2txt/train \
#   --input_file_pattern="${MEME_DIR}/train-?????-of-00256" \
#   --train_dir="${MODEL_DIR}/train" \
#   --train_inception=true \
#   --number_of_steps=10000
