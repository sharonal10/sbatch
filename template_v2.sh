#!/bin/bash

#SBATCH --time=XX_TIME
#SBATCH --cpus-per-task=XX_CPUS_PER_TASK
#SBATCH --gres=XX_GRES
#SBATCH --mem=XX_MEM
#SBATCH --ntasks=1
#SBATCH --nodes=1-1
XX_EXTRA

#SBATCH --job-name="XX_JOB"
#SBATCH --output=/viscam/u/<username>/data/sbatch_sweep_out/%A_%a_%j_%x.log

#SBATCH --account=XX_ACCOUNT
#SBATCH --partition=XX_PARTITION
#SBATCH --mail-user=<username>@stanford.edu
#SBATCH --mail-type=END,FAIL

echo "SLURM_JOBID=$SLURM_JOBID"
echo "SLURM_ARRAY_TASK_ID=$SLURM_ARRAY_TASK_ID"
echo "SLURM_JOB_NODELIST=$SLURM_JOB_NODELIST"
echo "SLURM_NNODES=$SLURM_NNODES"

source XX_SOURCE
#conda deactivate
# actenv XX_CONDA_ENV
conda activate XX_CONDA_ENV

cd XX_PROJ_DIR || exit

XX_ENV_VARS XX_COMMAND

echo "sbatch job done"
