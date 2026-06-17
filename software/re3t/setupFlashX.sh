# Setup Flash-X
if [ ! -d "Flash-X" ]; then
	git clone git@github.com:HEDBeams-Argonne/Flash-X-Re3t --branch main Flash-X && cd Flash-X
        git submodule update --init --recursive
fi
