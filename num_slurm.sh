#!/bin/bash

GPU_INFO="--partition viscam --account viscam --gpu_type 3090 --cpus_per_task 8 --num_gpus 1 --mem 100G"
# GPU_INFO="--partition viscam --account viscam --gpu_type a5000 --cpus_per_task 8 --num_gpus 1 --mem 64G"
# GPU_INFO="--partition viscam --account viscam --gpu_type titanrtx --cpus_per_task 8 --num_gpus 1 --mem 64G"

# GPU_INFO="--partition svl --account viscam --gpu_type titanrtx --cpus_per_task 8 --num_gpus 1 --mem 64G"

EXTRA_GPU_INFO="exclude=viscam1,viscam5,viscam7,svl[1-6],svl[8-10]"

num=1


# python -m sbatch_sweep --time 96:00:00 \
# --proj_dir /viscam/projects/image2Blender/differentiable_engine --conda_env diff_engine \
# --job "07-07-test-chair" --command "python training/training_transform.py --initial_xml initial_xmls/table.xml --target_image ref_imgs/basic_table.png --output_dir logs/2024-07-04-transform-with-angle4 --num_epochs 1000" $GPU_INFO "$EXTRA_GPU_INFO"


