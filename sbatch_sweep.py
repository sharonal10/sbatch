import argparse
import os
import subprocess
import sys

SBATCH_SCRIPT_DIR = '/viscam/u/<username>/data/sbatch_sweep_out'


def call_and_wait(cmd, verbose=False, dry=False, skip_wait=False):
    if dry:
        print(cmd)
        return
    if verbose:
        print(cmd)

    p = subprocess.Popen(cmd, shell=True)

    if skip_wait:
        return
    try:
        p.wait()
    except KeyboardInterrupt:
        try:
            print("terminating")
            p.terminate()
        except OSError:
            print("os error!")
            pass
        p.wait()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--dry', action='store_true', help='dry run')
    parser.add_argument('--job', type=str, default='sbatch_sweep', help='gpu type constraints')
    # resources
    parser.add_argument('--partition', type=str, default='viscam', help='viscam | svl')
    parser.add_argument('--time', type=str, default='4-00', help='gpu type constraints')
    parser.add_argument('--cpus_per_task', type=int, default=4, help='gpu type constraints')
    parser.add_argument('--gpu_type', type=str, default=None, help='gpu type constraints')
    parser.add_argument('--num_gpus', type=int, default=1, help='gpu type constraints')
    parser.add_argument('--mem', type=str, default='16G', help='total memory to allocate')
    # setup
    parser.add_argument('--source', type=str, default='/sailhome/<username>/.bashrc')
    parser.add_argument('--conda_env', type=str, required=True, help='conda environment')
    parser.add_argument('--proj_dir', type=str, required=True)
    # srun command
    parser.add_argument('--env_vars', type=str, default='DUMMY=0', help='environment variables')
    parser.add_argument('--command', type=str, default='', help='conda environment')

    # args, unknown = parser.parse_known_args()
    parser.add_argument("opts", nargs=argparse.REMAINDER)
    args = parser.parse_args()

    if args.cpus_per_task < 2:
        # with cpus_per_task = 1, if not specifying --ntasks=1, --nodes=1 in sbatch template,
        # will run 2 tasks in one job, leading to data race
        raise RuntimeError('cpus per task', args.cpus_per_task)

    # template_file = os.path.join(os.path.dirname(__file__), 'template.sh')
    template_file = os.path.join(os.path.dirname(__file__), 'template_v2.sh')
    with open(template_file, "r") as f:
        text = f.read()

    text = text.replace("XX_JOB", args.job)
    text = text.replace("XX_PARTITION", args.partition)
    text = text.replace("XX_ACCOUNT", 'viscam')# if args.partition == 'viscam' else 'vision')
    text = text.replace('XX_TIME', args.time)
    text = text.replace("XX_CPUS_PER_TASK", str(args.cpus_per_task))
    if args.num_gpus == 0:
        text = text.replace("XX_GRES", "")
    elif args.gpu_type is None:
        text = text.replace("XX_GRES", f"gpu:{args.num_gpus}")
    else:
        text = text.replace("XX_GRES", f"gpu:{args.gpu_type}:{args.num_gpus}")
    text = text.replace("XX_MEM", args.mem)
    text = text.replace("XX_EXTRA", "" if len(args.opts) == 0 else " --".join(["#SBATCH"] + args.opts))

    if ',' in args.conda_env:
        # expect format 3090:cu110,titanrtx:py39
        # assume args.gpu_type is a valid key
        conda_env = None
        for this_conda_env in args.conda_env.split(','):
            gpu_type, this_conda_env = this_conda_env.split(':')
            if gpu_type == args.gpu_type:
                conda_env = this_conda_env

        if conda_env is None:
            raise RuntimeError('conda env for gpu type not found', args.conda_env, args.gpu_type)
    else:
        conda_env = args.conda_env
    text = text.replace('XX_SOURCE', args.source)
    text = text.replace('XX_CONDA_ENV', conda_env)
    text = text.replace('XX_PROJ_DIR', args.proj_dir)
    text = text.replace('XX_PROJ_DIR', args.proj_dir)

    text = text.replace('XX_ENV_VARS', args.env_vars)
    text = text.replace("XX_COMMAND", args.command)

    print(text)

    # save (temporary) script
    assert os.path.exists(SBATCH_SCRIPT_DIR), SBATCH_SCRIPT_DIR
    script_fn = f"{args.job}.sh"
    script_file = os.path.join(SBATCH_SCRIPT_DIR, script_fn)
    with open(script_file, "w") as f:
        f.write(text)

    call_and_wait(f"sbatch {script_file}", dry=args.dry)

    sys.exit(0)
