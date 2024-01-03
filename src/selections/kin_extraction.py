import hashlib
import json
import logging
import os
import sqlite3
from pathlib import Path

import pandas as pd
import ROOT

from . import Zboson

selections = {"z_lep_lep": Zboson.lep_lep_selection}
chain_key = {"MonteCarlo": "Delphes;1", "Data": "mini"}


def get_file_id(file_path):
    return hashlib.md5(file_path.encode()).hexdigest()[:10]


def get_random_seed(filename):
    with open(filename, "r") as file:
        for line in file:
            if "iseed ! rnd seed" in line:
                seed = line.split("=")[0].strip()
                return int(seed)
    return None


def kinematics_extraction(file_path, sql_db_path, data_type, json_path):
    logging.info("Processing file: {}".format(file_path))
    datasets_dict = json.load(open(json_path, "r"))
    tree = ROOT.TChain(chain_key[data_type])
    tree.Add(file_path)
    n_entries = tree.GetEntries()
    if n_entries == 0:
        logging.warning("File {} has no entries".format(file_path))
        return False
    file_name = os.path.basename(file_path)
    if data_type == "Data":
        run = "N/A"
        seed = 0
    elif data_type == "MonteCarlo":
        run = os.path.basename(os.path.dirname(file_path))
        banner_file = [
            banner.as_posix()
            for banner in Path(file_path).parent.glob("*banner.txt")
        ][0]
        seed = get_random_seed(banner_file)
        if seed is None:
            logging.error(f"Seed not found in {banner_file}")
            return False
    sql_conn = sqlite3.connect(sql_db_path)
    file_properties = {
        "file_id": get_file_id(file_path),
        "file_path": file_path,
        "data_type": data_type,
        "n_entries": n_entries,
        "file_name": file_name,
        "run": run,
        "seed": seed,
    }
    logging.info(f"File properties: {file_properties}")

    pd.DataFrame.from_records([file_properties]).to_sql(
        "tb_files", sql_conn, if_exists="append", index=False
    )

    results = {}
    for event in tree:
        for selection, selection_function in selections.items():
            if (
                datasets_dict[selection]
                != os.path.basename(os.path.dirname(file_path))
            ) and (data_type == "Data"):
                continue
            results[selection] = results.get(selection, [])
            kin_row = selection_function(event, data_type)
            if kin_row:
                kin_row["file_id"] = file_properties["file_id"]
                results[selection].append(kin_row)
    for selection in results.keys():
        df = pd.DataFrame.from_records(results[selection])
        tb_name = f"tb_{selection}"
        df.to_sql(
            tb_name,
            sql_conn,
            if_exists="append",
            index=False,
        )
        df.to_csv(
            file_path + f".{tb_name}.csv",
            index=False,
        )

    sql_conn.close()

    return True
