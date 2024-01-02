import argparse
import os

from .kin_extraction import kinematics_extraction

parser = argparse.ArgumentParser(description="Process ROOT files")
parser.add_argument("--sql_db_path", type=str, help="SQL database")
parser.add_argument("--file_path", type=str, help="ROOT file path")
parser.add_argument(
    "--data_dir", type=str, help="Directory where data is stored"
)
parser.add_argument(
    "--data_type", type=str, help="Type of data (MC or data)", default="MC"
)
args = parser.parse_args()

file_path = args.file_path

if __name__ == "__main__":
    if kinematics_extraction(
        file_path, args.sql_db_path, args.data_type, args.data_dir
    ):
        os.remove(file_path)
