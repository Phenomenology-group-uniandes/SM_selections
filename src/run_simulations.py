import argparse
import logging
import os
import time

# Get the command line arguments
parser = argparse.ArgumentParser(description="Run simulations")
parser.add_argument("--data_dir", type=str, help="Monte Carlo Data directory")
parser.add_argument("--flag_file", type=str, help="Flag file")
args = parser.parse_args()

# Create the log file
logging.basicConfig(
    filename=os.path.join(os.dirname(args.data_dir), "run_simulations.log"),
    level=logging.INFO,
)


def main():
    logging.info("Starting")
    ### Your implementation here ###
    logging.info("Finished")


# create the flag file
with open(args.flag_file, "w") as f:
    f.write("simulation_in_progress")

try:
    main()
except Exception as e:
    logging.error(e)
finally:
    # remove the flag file
    os.remove(args.flag_file)
