#!/usr/bin/env bash
set -euo pipefail

# Setup UniFrame (unified_framework_poc)
if [ ! -d "UniFrame" ]; then
	git clone --branch main git@github.com:RIKEN-RCCS/unified_framework_poc.git UniFrame
fi

cd UniFrame
git submodule update --init --recursive
