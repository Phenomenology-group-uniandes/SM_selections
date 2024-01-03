import argparse
import logging
import os

from selections.kin_extraction import kinematics_extraction

parser = argparse.ArgumentParser(description="Process ROOT files")
parser.add_argument("--sql_db_path", type=str, help="SQL database")
parser.add_argument("--file_path", type=str, help="ROOT file path")
parser.add_argument(
    "--data_type", type=str, help="Type of data (MC or data)", default="MC"
)
parser.add_argument("--json_path", type=str, help="JSON file path")
args = parser.parse_args()

file_path = args.file_path
logging.basicConfig(
    filename=file_path + ".selections.log",
    level=logging.INFO,
)
if __name__ == "__main__":
    try:
        if kinematics_extraction(
            file_path, args.sql_db_path, args.data_type, args.json_path
        ):
            os.remove(file_path)
            logging.info(f"File {file_path} processed")
        else:
            logging.warning(f"File {file_path} has no entries")
    except Exception as e:
        logging.error(f"Error processing file {file_path}: {e}")
