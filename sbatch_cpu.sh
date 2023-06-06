#!/bin/bash
### sbatch config parameters must start with #SBATCH and must precede any other command. to ignore just add another # - like so ##SBATCH

#SBATCH --partition main ### specify partition name where to run a job. main - 7 days time limit
#SBATCH --time 6-01:30:00 ### limit the time of job running. Make sure it is not greater than the partition time limit!! Format: D-H:MM:SS
#SBATCH --job-name NLPSD ### name of the job. replace my_job with your desired job name
#SBATCH --output job-%J.out ### output log for running job - %J is the job number variable
#SBATCH --mail-user=itaitz@post.bgu.ac.il ### users email for sending job status notifications
#SBATCH --mail-type=END,FAIL ### conditions when to send the email. ALL,BEGIN,END,FAIL, REQUEU, NONE
#SBATCH --cpus-per-task=6 # 6 cpus per task – use for multithreading, usually with --tasks=1
#SBATCH --tasks=1 # 2 processes – use for processing of few programs concurrently in a job (with srun). Use just 1 otherwise
#SBATCH --mem=60G				### ammount of RAM memory, allocating more than 60G requires IT team's permission

### Print some data to output file ###
echo "SLURM_JOBID"=$SLURM_JOBID
echo "SLURM_JOB_NODELIST"=$SLURM_JOB_NODELIST

### Start you code below ####
module load anaconda ### load anaconda module
source activate ec_env ### activating Conda environment, environment must be configured before running the job
python $1 $2 $3 ### execute python script – replace with your own command. For jupyter write: jupyter-lab