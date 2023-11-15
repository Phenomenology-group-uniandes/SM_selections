#!/bin/bash
set -e

echo "Starting the container..."

# Sourcing installed software
echo "Sourcing installed software..."
source_paths=(\
  "/etc/bashrc" \
  "/Collider/ROOT/installROOT/bin/thisroot.sh" \
  "/Collider/env/bin/activate"\
  )
for path in "${source_paths[@]}"; do
    if [ -f "$path" ]; then
        # shellcheck source=/dev/null
        source "$path"
    else
        echo "Error: $path file not found"
        exit 1
    fi
done

COLLIDER_DIR="/Collider"
ROOT_BIN="$COLLIDER_DIR/ROOT/installROOT/bin/"
MG5_BIN="$COLLIDER_DIR/MG5_aMC_v3_1_0/bin/"
export PATH="${ROOT_BIN}:${MG5_BIN}:$PATH"

LHAPDF_LIB="$COLLIDER_DIR/LHAPDF/lib/"
export LD_LIBRARY_PATH="${LHAPDF_LIB}:$LD_LIBRARY_PATH"

# Run python script
echo "Running the python script..."
PROJECT_DIR="/project"
OUTPUT_DIR="/output"
cd "$PROJECT_DIR"
python main.py

# Change the owner of the project and output folder
echo "Updating the owner"
for dir in "$PROJECT_DIR" "$OUTPUT_DIR"; do
    if [ -d "$dir" ]; then
        chown -R "$(stat -c '1019:1019' "$dir")" "$dir"
    fi
done

# Done
echo "Done!"