#!/bin/bash
#SBATCH --job-name=fx-setup
#SBATCH --partition=standard
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --time=04:00:00
#SBATCH --output=setup-%j.out
#SBATCH --error=setup-%j.err

# Run `./configure -s hpc3` once beforehand so config.sh exists, then submit
# from the project root, e.g.:
#   sbatch sites/hpc3/setup.sbatch software/amrex software/flashx software/flashkit software/hdf5
#   sbatch sites/hpc3/setup.sbatch simulation/RisingBubble

set -e

cd "$SLURM_SUBMIT_DIR"

source .venv/bin/activate

DIRLIST=("$@")
if [ ${#DIRLIST[@]} -eq 0 ]; then
    DIRLIST=(software/amrex software/flashx software/hdf5)
fi

jobrunner setup "${DIRLIST[@]}" --verbose --exit-on-failure
