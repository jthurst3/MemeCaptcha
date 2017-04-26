#!/bin/bash

IM2TXT_DIR=/scratch/jthurst3/MemeCaptcha/models/im2txt

MODEL_DIR="${IM2TXT_DIR}/im2txt/model"

# Run a TensorBoard server.
tensorboard --logdir="${MODEL_DIR}"
