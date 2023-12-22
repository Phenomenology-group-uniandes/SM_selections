import argparse
import logging
import os
import subprocess
import time

# Get the command line arguments
parser = argparse.ArgumentParser(description="Run simulations")
parser.add_argument("--data_dir", type=str, help="Monte Carlo Data directory")
parser.add_argument("--flag_file", type=str, help="Flag file")
args = parser.parse_args()

# Create the log file
logging.basicConfig(
    filename=os.path.join(
        os.path.dirname(args.data_dir), "run_simulations.log"
    ),
    level=logging.INFO,
)


def main():
    logging.info("Starting")
    stout, stderr = subprocess.Popen(
        [
            "/Collider/MG5_aMC_v3_1_0/bin/mg5_aMC",
            os.path.join(os.getcwd(), "src", "simulations", "test.mg5"),
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    ).communicate()
    logging.info(f"stdout: {stout}".decode())
    logging.info(f"stderr: {stderr}".decode())
    time.sleep(10)
    logging.info("Finished")


try:
    # create the flag file
    with open(args.flag_file, "w") as f:
        f.write("simulation_in_progress")
    main()
except Exception as e:
    logging.error(e)
finally:
    # remove the flag file
    os.remove(args.flag_file)
