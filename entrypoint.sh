#!/bin/bash
# shellcheck source=/dev/null
source /etc/bashrc
echo "Starting the container..."

# Run python script
echo "Running the python script..."
cd /project || exit
python main.py 

# Change the owner of the project and output folder
chown 1019:1019 -R /project
chown 1019:1019 -R /output
