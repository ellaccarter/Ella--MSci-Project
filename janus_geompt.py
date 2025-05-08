#!/bin/bash -l
#$ -l gpu=1
#$ -l h_rt=18:00:00
#$ -l mem=15G
#$ -N comp_2_sys1_1to100
#$ -wd /home/zccaeca/Scratch  # Set working directory

# Load CUDA version
module unload compilers mpi
module unload cuda/7.5.18/gnu-4.9.2
module load cuda/11.3.1/gnu-10.2.0

# Activate the JANUS virtual environment
source /home/zccaeca/janus_env/bin/activate

# Move to the directory where the structure file is located
cd /home/zccaeca/Scratch

# Debugging: Check if the file exists
if [ ! -f cage_crystal_sys1_1.cif ]; then
    echo "Error: cage_crystal_sys1_1.cif not found!" >&2
    exit 1
fi

# set memory limits 
ulimit -s unlimited

# Run JANUS optimization
# Loop through cage_crystal_2_units_1.cif to cage_crystal_2_units_100.cif
for i in {1..101}; do
    janus geomopt --struct /home/zccaeca/Scratch/cage_crystal_sys1_${i}.cif \
                  --no-tracker --arch mace --steps 2000 --fmax 0.005 --opt-cell-fully \
                  --model-path /home/zccaeca/Scratch/mofs_model \
                  --device cuda --pressure 0.1 \
                  > /home/zccaeca/Scratch/cage_crystal_sys1_${i}_output.log 2> /home/zccaeca/Scratch/janus_error.log
done