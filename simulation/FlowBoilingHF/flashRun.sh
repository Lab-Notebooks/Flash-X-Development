# cache the value of current working directory
NodeDir=$(realpath .)

FlashOptions="$FlashOptions -tomlfile=$JobWorkDir/job.input --with-unitmods"

# run Flash-X setup
cd $FLASHX_HOME && echo Flash-X HEAD is at $(git rev-parse --short HEAD)
cd $FLASHX_HOME && git checkout $FlashSha && ./setup $FlashOptions

# compile the simulation and copy files
cp object/flash.par $JobWorkDir/ && cp object/*hdf5_htr* $JobWorkDir/

# Run the actualy job using this target script
if [[ $SiteName == "summit/gcc-10.2.0" || $SiteName == "summit/gcc-9.3.0" ]]; then

	echo Running on $SiteName

	cd $JobWorkDir && stdbuf -o0 jsrun -n ${NRS} \
		          -r ${NRS_PER_NODE} \
		          -a ${NMPI_PER_RS} \
		          -c ${NCORES_PER_RS} \
		          -b packed:${NCORES_PER_MPI} \
		          -d packed \
		          $JobWorkDir/job.target
else

	echo Running on $SiteName
        cd $JobWorkDir && mpirun $JobWorkDir/job.target
fi
