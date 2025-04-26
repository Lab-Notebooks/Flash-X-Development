# cache the value of current working directory

FlashSha="55157877a"

FlashOptions="incompFlow/FlowBoiling -auto -maxblocks=1000 -2d -nxb=16 -nyb=16 \
              +amrex +serialIO +nolwf -site=$SiteHome +incomp \
              -tomlfile=$JobWorkDir/job.input HeaterFluxBC=True --with-unitmods"

if [ $Profile = True ]; then
	FlashOptions="$FlashOptions +hpctoolkit"
fi
