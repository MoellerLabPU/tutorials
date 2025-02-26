# What is SLURM?

SLURM (Simple Linux Utility for Resource Management) is a workload manager and job scheduler designed for high-performance computing (HPC) clusters.

- **Job Scheduler**: When you submit jobs (i.e., tasks or commands you want to run), SLURM decides when and where they run based on available resources.
- **Resource Manager**: SLURM tracks how much CPU, memory, and GPU time each user consumes.

In essence, SLURM keeps everyone’s computations organized on a shared cluster, making sure resources are distributed fairly and efficiently.

# Why Should You Use SLURM Instead of Just Bash?

- **Resource Management**: Avoid conflicts and crashes from too many jobs running at the same time.
  - You can specify exactly how much memory, how many CPU cores, or which GPUs you need. This helps you avoid competing with others or overconsuming resources.
- **Automated Logging**: It captures standard output (stdout) and standard error (stderr) for each job, so you can debug or review logs later.
- **Parallelism & Scalability**: It allows you to run tasks in parallel on multiple machines or multiple CPUs.
- **Reproducible Workflows**: Job scripts capture all the important details: environment variables, modules loaded, resource requirements, and commands. SLURM can also send you notifications.

In short, SLURM helps you make the most of the cluster’s resources without stepping on your colleagues’ toes—or your own.

# Basic SLURM Commands

Here are some commonly used SLURM commands you’ll see:

- `sbatch`: Submits a job script for batch execution.
- `squeue`: Shows the status of submitted jobs (yours and possibly others).
- `scancel`: Cancels a job (or set of jobs).

## `sbatch`

- **Usage**: `sbatch <script_name>`
- **Purpose**: Submit a job script to the scheduler.
- **Behavior**: Once you run `sbatch`, SLURM will assign a job ID and place it in the queue.

Example:
`sbatch my_first_job.sh`

Upon submission, SLURM will return a Job ID—for example:

`Submitted batch job 123456`

## `squeue`

- **Usage**: `squeue`
- **Purpose**: Shows information about jobs in the queue (both running and pending).
- **Options**: `-u <username>` to filter by user.

Example:
`squeue` or `-u <username>`

## `scancel`

- **Usage**: `scancel <job_id>`
- **Purpose**: Cancel (kill) a job that is pending or running.

Example:

`scancel <JOB_ID>`. You can see the `<JOB_ID>` on running `squeue`.

You can calcel ALL the jobs that you're running using `scancel -u $USER`.


# Creating a Simple SLURM Job Script

A typical SLURM job script is a **Bash** script that includes special `#SBATCH` directives indicating resource requests and SLURM configuration parameters.

Below is a minimal example job script:

```bash

#!/bin/bash
#SBATCH --ntasks=1                  # Number of tasks (processes) to spawn
#SBATCH --nodes=1                   # node count
#SBATCH --output=my_first_job.out   # Where to save stdout (output)
#SBATCH --error=my_first_job.err    # Where to save stderr (error messages)
#SBATCH --time=00:05:00             # Total rutime (5 minutes) (HH:MM:SS)
#SBATCH --mem=4000                  # Memory in Mb
#SBATCH --cpus-per-task=1           # CPUs to use


# Optional: Email notifications
#SBATCH --mail-user=<YourNetID>@princeton.edu
#SBATCH --mail-type=BEGIN,END,FAIL, ALL     # send email when job begins, ends, fails or all three.

# Print some info about the job
echo "Running job ID: $SLURM_JOB_ID on node(s): $SLURM_NODELIST"
echo "Current working directory is $(pwd)"

# Run your computational task
python my_script.py  # or whatever command(s) you need

```

# Submitting, monitoring and cancelling a Job


## Submitting the job

Once your job script is ready, submit it using:

`sbatch my_first_job.sh`

Upon submission, SLURM will return a Job ID—for example:

`Submitted batch job 123456`

## Checking the Status of Your Jobs

To see the status of your jobs use `squeue -u $USER`. You can also run `squeue` without the `-u $USER` flag to see all jobs on the cluster, but that might be overwhelming if many other users are running hundreds of jobs.

You should see something like:

```bash
JOBID   PARTITION   NAME           USER ST TIME  NODES NODELIST(REASON)
123456  regular     my_first_job   $USER  R  0:05  1     compute-node-1
```

Typical columns in squeue:

- JOBID: Your job’s unique ID.
- PARTITION: Which partition (node group) the job is assigned to.
- NAME: Job name.
- USER: Owner of the job.
- ST: Status (e.g., R = running, PD = pending).
- TIME: How long the job has been running.
- NODELIST(REASON): Which node(s) the job is on or why it is pending.

## Canceling a Job

If you need to kill a running job, run `scancel <JOB_ID>`. You can see the `<JOB_ID>` on running `squeue`.

You can cancel ALL the jobs that you're running using `scancel -u $USER`.

# Common Pitfalls and Tips

1. Check Your Resource Requests:
    - Requesting too little memory causes crashes (“Out of Memory”).
    - Requesting too much might lead to long wait times or wasted resources.

1. Use `.out` and `.err` Files for Debugging:
   - If a job fails, check the .out and .err files to see the error messages.

1. Permissions: 
   - Make sure your script is executable `chmod +x my_first_job.sh`

1. Environment Modules and paths:
    - Don’t forget to load any modules (e.g., software tools, languages) and/or export `PATHS` that you need within your SLURM script, not just in your command line. 

# Using SLURM with Snakemake and Profiles

Snakemake is a powerful workflow management tool that lets you create reproducible pipelines. When combined with SLURM, you can distribute and run individual workflow steps on your HPC cluster efficiently.

## Using Snakemake Profiles for SLURM

A profile centralizes your SLURM configuration into a set of files, making your commands cleaner and ensuring consistency across runs. Here’s how you can set it up:

1. Create a profile directory (e.g., `cornell_profile/`)

2. Add a cluster configuration file (`config.yaml`). Some cookiecutter profiles that work for most cases can be found [here](https://github.com/jdblischak/smk-simple-slurm?tab=readme-ov-file). Below is an example that I use. This requires the installation of `cluster-generic` plugin from conda ([link](https://bioconda.github.io/recipes/snakemake-executor-plugin-cluster-generic/README.html)):

   Example:

   ```yaml
      executor: cluster-generic
      cluster-generic-submit-cmd:
      mkdir -p logs/`date +"%d-%m-%y"`/{rule} &&
      sbatch
         --cpus-per-task={threads}
         --mem={resources.mem_mb}
         --time={resources.time}
         --job-name=smk-{rule}-{wildcards}
         --output=logs/`date +"%d-%m-%y"`/{rule}/{rule}-{wildcards}-%j.out
         --parsable

      default-resources:
      - mem_mb=4000
      - time="10:00:00"

      restart-times: 0
      max-jobs-per-second: 100
      max-status-checks-per-second: 1
      latency-wait: 60
      jobs: 100
      keep-going: True
      rerun-incomplete: True
      printshellcmds: True
      use-conda: True
      cluster-generic-cancel-cmd: scancel

   ```

3. Run Snakemake with the profile

   `snakemake --profile cornell_profile`



