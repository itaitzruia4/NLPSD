#!/bin/bash
### sbatch config parameters must start with #SBATCH and must precede any other command. to ignore just add another # - like ##SBATCH
#SBATCH --partition main ### partition name where to run a job. Use ‘main’ unless qos is required. qos partitions ‘rtx3090’ ‘rtx2080’ ‘gtx1080’
#SBATCH --time 6-10:30:00 ### limit the time of job running. Make sure it is not greater than the partition time limit (7 days)!! Format: D-H:MM:SS
#SBATCH --job-name NLPSD-train ### name of the job. replace my_job with your desired job name
#SBATCH --output job-%J.out ### output log for running job - %J is the job number variable
#SBATCH --mail-user=itaitz@post.bgu.ac.il ### user’s email for sending job status notifications
#SBATCH --mail-type=END,FAIL ### conditions for sending the email. ALL,BEGIN,END,FAIL, REQUEU, NONE
#SBATCH --gpus=1 ### number of GPUs. Choosing type e.g.: #SBATCH --gpus=gtx_1080:1 , or rtx_2080, or rtx_3090 . Allocating more than 1 requires the IT team’s permission
#SBATCH --mem=60G				### ammount of RAM memory, allocating more than 60G requires IT team's permission
##SBATCH --tasks=1 # 1 process – use for processing of few programs concurrently in a job (with srun). Use just 1 otherwise

### Print some data to output file ###
echo "SLURM_JOBID"=$SLURM_JOBID
echo "SLURM_JOB_NODELIST"=$SLURM_JOB_NODELIST
nvidia-smi -L
### Start your code below ####
module load anaconda ### load anaconda module
source activate ec_env ### activate a conda environment, replace my_env with your conda environment
python $1 $SLURM_JOBID ### this command executes jupyter lab – replace with your own command e.g. ‘python my.py my_arg