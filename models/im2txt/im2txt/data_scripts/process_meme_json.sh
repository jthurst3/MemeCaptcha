#!/bin/bash
# Copyright 2016 The TensorFlow Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

# Script to download and preprocess the MSCOCO data set.
#
# The outputs of this script are sharded TFRecord files containing serialized
# SequenceExample protocol buffers. See build_mscoco_data.py for details of how
# the SequenceExample protocol buffers are constructed.
#
# usage:
#  ./process_meme_json.sh
set -e

if [ -z "$1" ]; then
  echo "usage process_meme_json.sh [data dir]"
  exit
fi

# Create the output directories.
OUTPUT_DIR="${1%/}"
SCRATCH_DIR="${OUTPUT_DIR}"
mkdir -p "${OUTPUT_DIR}"
mkdir -p "${SCRATCH_DIR}"
CURRENT_DIR=$(pwd)
WORK_DIR="$0.runfiles/im2txt/im2txt"

cd ${SCRATCH_DIR}

TRAIN_IMAGE_DIR="/public/jthurst3/MemeCaptcha/images"
TRAIN_CAPTIONS_FILE="${SCRATCH_DIR}/memes_armstrong_aa.json"

# Build TFRecords of the image data.
cd "${CURRENT_DIR}"
#BUILD_SCRIPT="${WORK_DIR}/build_mscoco_data"
BUILD_SCRIPT="/scratch/jthurst3/MemeCaptcha/models/im2txt/bazel-bin/im2txt/build_meme_data"
"${BUILD_SCRIPT}" \
  --train_image_dir="${TRAIN_IMAGE_DIR}" \
  --train_captions_file="${TRAIN_CAPTIONS_FILE}" \
  --output_dir="${OUTPUT_DIR}" \
  --word_counts_output_file="${OUTPUT_DIR}/word_counts.txt" \
