#!/usr/bin/env bash
set -euo pipefail

# Mirrors files from Flash-X source tree into the corresponding FlashLite tree.
#
# Default behavior mirrors only the *top-level files* in the requested directory
# (no subdirectories) using rsync --delete scoped to that directory.

usage() {
	cat <<'EOF'
Usage:
	mirror_flashx_to_flashlite.sh [--dry-run] [--recursive] <relative-path>

Arguments:
	<relative-path>  Path relative to Flash-X source root
	                (software/flashx/Flash-X/source)
	                Example: Grid/GridMain/AMR/Amrex

Options:
	--dry-run    Show what would change without modifying files
	--recursive  Copy recursively (include subdirectories). Default is top-level files only.
	-h, --help   Show this help

Notes:
	- Destination is mapped to the same relative path under:
	  software/uniframe/UniFrame/FlashLite/source
	- Uses rsync --delete (will delete destination-only files within the target dir).
EOF
}

DRY_RUN=0
RECURSIVE=0
REL_PATH=""

while [[ $# -gt 0 ]]; do
	case "$1" in
	--dry-run)
		DRY_RUN=1
		shift
		;;
	--recursive)
		RECURSIVE=1
		shift
		;;
	-h | --help)
		usage
		exit 0
		;;
	--*)
		echo "Unknown option: $1" >&2
		usage >&2
		exit 2
		;;
	*)
		if [[ -n "$REL_PATH" ]]; then
			echo "Unexpected extra argument: $1" >&2
			usage >&2
			exit 2
		fi
		REL_PATH="$1"
		shift
		;;
	esac
done

if [[ -z "$REL_PATH" ]]; then
	echo "Missing <relative-path>." >&2
	usage >&2
	exit 2
fi

# Prefer the git repo root if available; fall back to current directory.
ROOT_DIR="$PWD"
if command -v git >/dev/null 2>&1; then
	if GIT_ROOT=$(git rev-parse --show-toplevel 2>/dev/null); then
		ROOT_DIR="$GIT_ROOT"
	fi
fi

FLASHX_ROOT_REL="software/flashx/Flash-X/source/physics/IncompNS"
FLASHLITE_ROOT_REL="software/uniframe/UniFrame/FlashLite/source/physics/IncompNS"

SRC="$ROOT_DIR/$FLASHX_ROOT_REL/$REL_PATH"
DST="$ROOT_DIR/$FLASHLITE_ROOT_REL/$REL_PATH"

if [[ ! -d "$SRC" ]]; then
	echo "Source directory not found: $SRC" >&2
	exit 1
fi

if [[ ! -d "$DST" ]]; then
	echo "Destination directory not found: $DST" >&2
	echo "Create it first if needed." >&2
	exit 1
fi

EXCLUDES=(
	--exclude '.git/'
	--exclude '.gitmodules'
	--exclude '.gitattributes'
	--exclude '.github/'
)

if [[ $RECURSIVE -eq 0 ]]; then
	# Exclude all subdirectories to mirror only top-level files.
	EXCLUDES+=(--exclude '*/')
fi

RSYNC_ARGS=(
	-a
	--delete
	--itemize-changes
)

if [[ $DRY_RUN -eq 1 ]]; then
	RSYNC_ARGS+=(--dry-run)
fi

echo "Repo root:   $ROOT_DIR"
echo "Source:      $SRC"
echo "Destination: $DST"
if [[ $DRY_RUN -eq 1 ]]; then
	echo "Mode:        dry-run"
else
	echo "Mode:        mirror (will delete destination-only files)"
fi
if [[ $RECURSIVE -eq 1 ]]; then
	echo "Depth:       recursive"
else
	echo "Depth:       top-level files only"
fi
echo

rsync "${RSYNC_ARGS[@]}" "${EXCLUDES[@]}" "$SRC/" "$DST/"
