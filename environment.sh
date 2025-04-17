# Bash file to load modules and set environment
# variables for compilers and external libraries

# Set project home using realpath
# of current directory
export PROJECT_HOME=$(realpath .)

# Set SiteHome to realpath of SiteName
SiteHome="$PROJECT_HOME/sites/$SiteName"

# Load modules from the site directory
source $SiteHome/environment.sh

# Path to parallel HDF5 installtion with fortran support
if [ $HDF5_HOME ]; then
	BuildHDF5=false
else
	BuildHDF5=true
	export HDF5_HOME="$PROJECT_HOME/software/hdf5/HDF5/install-$SiteName"
	export LD_LIBRARY_PATH="$LD_LIBRARY_PATH:$HDF5_HOME/lib"
	export LIBRARY_PATH="$LD_LIBRARY_PATH"
fi

# Store path to amrex as environment variable
export AMREX2D_HOME="$PROJECT_HOME/software/amrex/AMReX/install-$SiteName/2D"
export AMREX3D_HOME="$PROJECT_HOME/software/amrex/AMReX/install-$SiteName/3D"

# Path to Flash-X
export FLASHX_HOME="$PROJECT_HOME/software/flashx/Flash-X"

# Store path to ANN
export ANN_HOME="$PROJECT_HOME/software/ann/ANN"
export LD_LIBRARY_PATH="$LD_LIBRARY_PATH:$ANN_HOME/lib"
export LIBRARY_PATH="$LD_LIBRARY_PATH"

# Store path to Hypre
export HYPRE_HOME="$PROJECT_HOME/software/hypre/HYPRE/install-$SiteName"
export LD_LIBRARY_PATH="$LD_LIBRARY_PATH:$HYPRE_HOME/lib"
export LIBRARY_PATH="$LD_LIBRARY_PATH"

# Flash-X test archive paths
if ! [ $FLASHTEST_MAIN_ARCHIVE ]; then
	export FLASHTEST_MAIN_ARCHIVE="$PROJECT_HOME/tests/MainArchive"
fi

if ! [ $FLASHTEST_LOCAL_ARCHIVE ]; then
	export FLASHTEST_LOCAL_ARCHIVE="$PROJECT_HOME/tests/LocalArchive"
fi

if ! [ $FLASHTEST_OUTDIR ]; then
	export FLASHTEST_OUTDIR="$PROJECT_HOME/tests/TestResults"
fi

# Output information to stdout
echo "---------------------------------------------------------------------------------------"
echo "Execution Environment:"
echo "---------------------------------------------------------------------------------------"
echo "PROJECT_HOME=$PROJECT_HOME"
echo "SITE_HOME=$SiteHome"
echo "MPI_HOME=$MPI_HOME"
echo "HDF5_HOME=$HDF5_HOME"
echo "FLASHX_HOME=$FLASHX_HOME"
echo "AMREX2D_HOME=$AMREX2D_HOME"
echo "AMREX3D_HOME=$AMREX3D_HOME"
echo "HYPRE_PATH=$HYPRE_PATH"
echo "LD_LIBRARY_PATH=$LD_LIBRARY_PATH"
echo "ANN_HOME=$ANN_HOME"
echo "PATH=$PATH"
echo "---------------------------------------------------------------------------------------"
