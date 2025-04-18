# cache the value of current working directory
NodeDir=$(realpath .)

# run Flash-X setup
cd $FLASHX_HOME && echo Flash-X HEAD is at $(git rev-parse --short HEAD)
cd $FLASHX_HOME && git checkout $FlashSha && ./setup $FlashOptions

# compile the simulation and copy files
cd $FLASHX_HOME/object && make -j && cp flashx $NodeDir/ && cp flash.par $NodeDir/ && cp *hdf5_htr* $NodeDir/

# copy AMReX configuration
cd $AMREX2D_HOME/lib/pkgconfig && cp amrex.pc $NodeDir/

# chdir into node directory and do clean up
cd $NodeDir #&& rm -rf $FLASHX_HOME/object
