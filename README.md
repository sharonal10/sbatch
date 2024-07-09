Replace <username> with your username before running ./num_slurm.sh

Use for loops in num_slurm.sh to run multiples of the same job, but make sure the job name (`--job`) is different for each iteration, otherwise the job logs may overwrite each other.

Job logs can be found in /viscam/u/<username>/data/sbatch_sweep_out
