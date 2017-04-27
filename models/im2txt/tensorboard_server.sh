#!/bin/bash
#SBATCH -p standard
#SBATCH -N 1
#SBATCH --mem-per-cpu=1GB
#SBATCH -t 10:00:00
#SBATCH -o slurm_logs/tensorboard.out
#SBATCH -e slurm_logs/tensorboard.err
#SBATCH -J tensorboard
#SBATCH --mail-type=all

IM2TXT_DIR=/scratch/jthurst3/MemeCaptcha/models/im2txt

MODEL_DIR="${IM2TXT_DIR}/im2txt/model"

# Run a TensorBoard server.
tensorboard --logdir="${MODEL_DIR}"
