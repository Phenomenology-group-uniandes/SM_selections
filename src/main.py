import json
import logging
import os
import sqlite3
import time
from functools import wraps
from subprocess import PIPE, Popen

from Atlas_Reader_13TeV.helpers import download_atlas_opendataset

# Archive directory, inside the project directory to store the results on the
# repository
ARCHIVE_DIR = os.path.join(os.getcwd(), "archive")
os.makedirs(ARCHIVE_DIR, exist_ok=True)

# Data directory, inside a external drive to store the HUGE data files
DATA_DIR = os.path.join(os.sep, "output")
os.makedirs(DATA_DIR, exist_ok=True)
EXP_DATA_DIR = os.path.join(DATA_DIR, "Data")
os.makedirs(EXP_DATA_DIR, exist_ok=True)
MC_DATA_DIR = os.path.join(DATA_DIR, "MC")
os.makedirs(MC_DATA_DIR, exist_ok=True)

# SQLite database file, inside the data directory to store the results
DB_FILE = "sm_selected_events.sqlite"
DB_PATH = os.path.join(DATA_DIR, DB_FILE)
if os.path.exists(DB_PATH):
    os.remove(DB_PATH)
CONN = sqlite3.connect(DB_PATH)

# Experimental data
EXP_DATASETS = {
    # # vector boson
    # "w_lep": "1lep",
    "z_lep_lep": "2lep",
    # "z_tau_tau": "1lep1tau",
    # # higgs boson
    # "h_y_y": "GamGam",
    # "h_w_w_leptonic": "1lep",
    # "h_z_z_leptonic": "2lep",
    # # diboson
    # "wz_3l": "3lep",
    # "zz_4l": "4lep",
    # # top quark
    # "top_lep": "1lep",
    # "ttbar_semileptonic": "1lep",
    # # BSM Sequential Z'
    # "zprime_lep_lep": "2lep",
}
JSON_PATH = os.path.join(EXP_DATA_DIR, "datasets.json")
json.dump(EXP_DATASETS, open(JSON_PATH, "w"))

ANALYSIS = EXP_DATASETS.keys()


def log_decorator(message):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            logging.info(f"Starting {message}")
            result = func(*args, **kwargs)
            logging.info(f"Finished {message}")
            return result

        return wrapper

    return decorator


@log_decorator("Downloading ATLAS open dataset files")
def download_atlas_opendatasets():
    """Download ATLAS open datasets"""
    return list(
        map(
            lambda x: download_atlas_opendataset(x, EXP_DATA_DIR),
            set(EXP_DATASETS.values()),
        )
    )


@log_decorator("Launching madgraph simulation")
def run_simulation(flag_file):
    return Popen(
        [
            "python",
            os.path.join(os.getcwd(), "src", "run_simulations.py"),
            "--data_dir",
            MC_DATA_DIR,
            "--flag_file",
            flag_file,
        ],
        stdout=PIPE,
        stderr=PIPE,
    )


@log_decorator("Running selections")
def process_files(flag_file):
    from pathlib import Path

    data_dic = {
        "Data": EXP_DATA_DIR,
        "MonteCarlo": MC_DATA_DIR,
    }
    files_dic = {key: [] for key in data_dic.keys()}
    while (
        os.path.exists(flag_file)
        or len(files_dic["Data"] + files_dic["MonteCarlo"]) > 0
    ):
        time.sleep(1)
        for key, root_files in files_dic.items():
            for root_file in root_files:
                print(root_file)
                stout, stderr = Popen(
                    [
                        "python",
                        os.path.join(
                            os.getcwd(),
                            "src",
                            "process_file.py",
                        ),
                        "--sql_db_path",
                        DB_PATH,
                        "--file_path",
                        root_file,
                        "--data_type",
                        key,
                        "--json_path",
                        JSON_PATH,
                    ],
                    stdout=PIPE,
                    stderr=PIPE,
                ).communicate()
                process_output = stout
                process_error = stderr
                print(process_output)
                print(process_error)
        # It's important search for new files at the end of the loop, because
        # the simulation script will create new files
        logging.info("searching for new files")
        for key in files_dic.keys():
            files_dic[key] = [
                root_file.as_posix()
                for root_file in Path(data_dic[key]).rglob("*.root")
            ]
        logging.info(f"files_dic: {files_dic}")
    logging.info("No more files to process")


@log_decorator("Running machine learning classifiers")
def run_machine_learning_classifiers():
    pass  # Your implementation here


@log_decorator("Running analysis")
def run_analysis():
    pass  # Your implementation here


def main():
    # Download ATLAS open datasets
    download_atlas_opendatasets()

    # Run simulation
    sim_flag_file = os.path.join(ARCHIVE_DIR, "simulation_in_progress.flag")
    run_simulation(sim_flag_file)
    time.sleep(5)
    # Process files
    process_files(sim_flag_file)

    # Run machine learning classifiers
    run_machine_learning_classifiers()

    # Run analysis
    run_analysis()


if __name__ == "__main__":
    # Initialize logging
    logging.basicConfig(
        filename=os.path.join(DATA_DIR, "main.log"), level=logging.INFO
    )
    logging.info("Starting")
    try:
        main()
    except Exception as e:
        logging.error(e)
    # Finish
    logging.info("Finished")
