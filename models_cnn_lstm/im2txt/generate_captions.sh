#!/bin/bash

IM2TXT_DIR=/scratch/tkhunkhe/MemeCaptcha/models/im2txt

# Path to checkpoint file or a directory containing checkpoint files. Passing
# a directory will only work if there is also a file named 'checkpoint' which
# lists the available checkpoints in the directory. It will not work if you
# point to a directory with just a copy of a model checkpoint: in that case,
# you will need to pass the checkpoint path explicitly.
CHECKPOINT_PATH="${IM2TXT_DIR}/im2txt/model/train"

# Vocabulary file generated by the preprocessing script.
VOCAB_FILE="${IM2TXT_DIR}/im2txt/data/mscoco/word_counts.txt"

# JPEG image file to caption.
IMAGE_FILE="${IM2TXT_DIR}/im2txt/data/mscoco/raw-data/val2014/COCO_val2014_000000224477.jpg"

# Build the inference binary.
bazel build -c opt im2txt/run_inference

# Ignore GPU devices (only necessary if your GPU is currently memory
# constrained, for example, by running the training script).
export CUDA_VISIBLE_DEVICES=""

# Run inference to generate captions.
bazel-bin/im2txt/run_inference \
  --checkpoint_path=${CHECKPOINT_PATH} \
  --vocab_file=${VOCAB_FILE} \
  --input_files=${IMAGE_FILE}
