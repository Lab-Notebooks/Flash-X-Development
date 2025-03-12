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
