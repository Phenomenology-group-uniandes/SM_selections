import logging
import os
import sqlite3

from Atlas_Reader_13TeV.helpers import download_atlas_opendataset
from selections import Zboson

# Archive directory, inside the project directory to store the results on the
# repository
ARCHIVE_DIR = os.path.join(os.getcwd(), "archive")
os.makedirs(ARCHIVE_DIR, exist_ok=True)

# Data directory, inside a external drive to store the HUGE data files
DATA_DIR = os.path.join(os.sep, "output")
os.makedirs(DATA_DIR, exist_ok=True)
EXP_DATA_DIR = os.path.join(DATA_DIR, "Data")

# SQLite database file, inside the data directory to store the results
DB_FILE = "sm_selected_events.sqlite"
DB_PATH = os.path.join(DATA_DIR, DB_FILE)
if os.path.exists(DB_PATH):
    os.remove(DB_PATH)
CONN = sqlite3.connect(DB_PATH)

# Experimental data
EXP_DATASETS = {
    # vector boson
    "w_lep": "1lep",
    "z_lep_lep": "2lep",
    "z_tau_tau": "1lep1tau",
    # higgs boson
    "h_y_y": "GamGam",
    "h_w_w_leptonic": "1lep",
    "h_z_z_leptonic": "2lep",
    # diboson
    "wz_3l": "3lep",
    "zz_4l": "4lep",
    # top quark
    "top_lep": "1lep",
    "ttbar_semileptonic": "1lep",
    # BSM Sequential Z'
    "zprime_lep_lep": "2lep",
}

# Selectors
SELECTORS = {
    # vector boson
    "z_lep_lep": Zboson.lep_lep_selection
}


def main():
    logging.basicConfig(
        filename=os.path.join(ARCHIVE_DIR, "main.log"), level=logging.INFO
    )
    logging.info("Downloading ATLAS open dataset files")

    for key in SELECTORS:
        if key not in EXP_DATASETS:
            message = f"Selector {key} not found in EXP_DATASETS dictionary"
            logging.error(message)
            raise ValueError(message)
        else:
            download_atlas_opendataset(
                EXP_DATASETS[key], os.path.join(EXP_DATA_DIR)
            )

    logging.info("Finished downloading ATLAS open dataset files")


if __name__ == "__main__":
    main()
