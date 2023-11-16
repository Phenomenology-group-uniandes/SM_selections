#!/bin/bash
set -e

echo "Starting the container..."

# Sourcing installed software
echo "Sourcing installed software..."
source_paths=(
  "/etc/bashrc"
  "/Collider/ROOT/installROOT/bin/thisroot.sh"
  "/Collider/env/bin/activate"
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

# Set up the environment to use ROOT, MadGraph and LHAPDF
COLLIDER_DIR="/Collider"
ROOT_BIN="$COLLIDER_DIR/ROOT/installROOT/bin/"
MG5_BIN="$COLLIDER_DIR/MG5_aMC_v3_1_0/bin/"
LHAPDF_LIB="$COLLIDER_DIR/LHAPDF/lib/"
export PATH="${ROOT_BIN}:${MG5_BIN}:$PATH"
export LD_LIBRARY_PATH="${LHAPDF_LIB}:$LD_LIBRARY_PATH"

# Set up the project, install the requirements and run the python script
echo "Setting up the project..."
PROJECT_DIR="/project"
OUTPUT_DIR="/output"
touch "$OUTPUT_DIR/selections.log"
cd "$PROJECT_DIR"
# shellcheck source=/dev/null
source ".env"
pip install -q -r $PROJECT_DIR/hep_pheno_tools/requirements.txt
pip install -q -r $PROJECT_DIR/requirements.txt

# Run python script
echo "Running the python script..."
python main.py

# Change the owner of the project and output folder
echo "Updating the owner"
for dir in "$PROJECT_DIR" "$OUTPUT_DIR"; do
  if [ -d "$dir" ]; then
    chown -R "${USER_ID}:${GROUP_ID}" "$dir"
  fi
done

# Done
echo "Done!"
