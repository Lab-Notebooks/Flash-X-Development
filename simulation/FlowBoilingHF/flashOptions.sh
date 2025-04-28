# cache the value of current working directory

FlashSha="15af86e76"

FlashOptions="incompFlow/FlowBoiling -auto -maxblocks=1000 -2d -nxb=16 -nyb=16 \
              +amrex +serialIO +nolwf -site=$SiteHome +incomp HeaterFluxBC=True"

if [ $Profile = True ]; then
	FlashOptions="$FlashOptions +hpctoolkit"
fi
