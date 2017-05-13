#!/bin/bash
#SBATCH -p gpu
#SBATCH -N 1
#SBATCH --mem-per-cpu=1GB
#SBATCH -t 10:00:00
#SBATCH -o slurm_logs/char_im2txt_tensorboard1.out
#SBATCH -e slurm_logs/char_im2txt_tensorboard1.err
#SBATCH -J tensorboard
#SBATCH --mail-type=all

IM2TXT_DIR=/public/jthurst3/MemeCaptcha

MODEL_DIR="${IM2TXT_DIR}/models/char_im2txt"

#module load tensorflow

# Run a TensorBoard server.
tensorboard --logdir="${MODEL_DIR}"
