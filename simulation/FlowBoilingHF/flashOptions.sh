# cache the value of current working directory

FlashSha="adhruv/development"

FlashOptions="incompFlow/FlowBoiling -auto -maxblocks=1000 -2d -nxb=8 -nyb=8 \
              +amrex +serialIO +nolwf -site=$SiteHome +incomp \
              -tomlfile=$JobWorkDir/job.input HeaterFluxBC=True --with-unitmods"

if [ $Profile = True ]; then
	FlashOptions="$FlashOptions +hpctoolkit"
fi
