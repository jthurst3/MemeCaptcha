#!/bin/bash
#SBATCH -p gpu
#SBATCH -N 1
#SBATCH --mem-per-cpu=1GB
#SBATCH -t 10:00:00
#SBATCH -o slurm_logs/tensorboard_min1.out
#SBATCH -e slurm_logs/tensorboard_min1.err
#SBATCH -J tensorboard
#SBATCH --mail-type=all

IM2TXT_DIR=/public/jthurst3/MemeCaptcha

MODEL_DIR="${IM2TXT_DIR}/models/im2txt_min_1"

# Run a TensorBoard server.
tensorboard --logdir="${MODEL_DIR}"
