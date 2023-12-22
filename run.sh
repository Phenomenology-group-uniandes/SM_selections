#!/bin/bash
set -e
# shellcheck source=/dev/null
if [ -f .env ]; then
  source .env
else
  echo "Error: .env file not found, please create it with the OUTPUT_PATH variable"
  exit 1
fi

# Establish the number of cores to use
CPUS=2
while getopts ":c:" opt; do
  case ${opt} in
  c)
    CPUS=$OPTARG
    ;;
  \?)
    echo "Invalid option: $OPTARG" 1>&2
    exit 1
    ;;
  :)
    echo "Invalid option: $OPTARG requires an argument" 1>&2
    exit 1
    ;;
  esac
done
shift $((OPTIND - 1))

if [ "$CPUS" -gt "$(($(nproc) / 2))" ]; then
  echo "Error: The number of CPUs specified is greater than the "$(($(nproc) / 2))" available"
  exit 1
fi

# Check if USER_ID exists in .env
if ! grep -q "USER_ID" .env; then
  # If USER_ID does not exist, add it
  printf "\n" >>.env
  echo "USER_ID=$(id -u)" >>.env
fi

# Check if GROUP_ID exists in .env
if ! grep -q "GROUP_ID" .env; then
  # If GROUP_ID does not exist, add it
  printf "\n" >>.env
  echo "GROUP_ID=$(id -g)" >>.env
fi

# update repository
git pull

# update submodules
git submodule update --init --recursive --remote

# remove the old container
docker rm -f sm_selections_container || true

# Build the new image
docker build -t sm_selections .

# Create if not exists the output folder
mkdir -p "$OUTPUT_PATH"
echo "Raw Data folder: $OUTPUT_PATH"

# Remove the symbolic link if exists
rm -f OutputFolder

# Create a symbolic link to the output folder
ln -sf "$OUTPUT_PATH" OutputFolder

# Run the container, use 10 cores i,e 20 threads
docker run -t \
  --env-file .env \
  --cpus="$CPUS" \
  --mount type=bind,source="$OUTPUT_PATH",target=/output \
  --mount type=bind,source="$(pwd)",target=/project \
  --name sm_selections_container \
  sm_selections

# # Remove the container
# docker rm -f sm_selections_container
