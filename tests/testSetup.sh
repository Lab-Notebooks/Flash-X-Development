# Initialiaze Flash-X testing environment by first creating 
# a temprorary site in the Flash-X site folder
TestSiteName=multiphase.simulations && mkdir -pv $FLASHX_HOME/sites/$TestSiteName

# Link makefiles to use the makefile from current site directory
ln -sf $SiteHome/Makefile.h $FLASHX_HOME/sites/$TestSiteName/Makefile.h

# Initialize config and execfile
cd $JobWorkDir && flashxtest init -z $FLASHX_HOME \
	         -s $TestSiteName -m $FLASHTEST_MAIN_ARCHIVE \
	         -a $FLASHTEST_LOCAL_ARCHIVE -o $FLASHTEST_OUTDIR -mpi=mpirun -make="make -j"

# Initialiaze Flash-X test suite
cd $JobWorkDir && flashxtest setup-suite --overwrite Tests.suite 
