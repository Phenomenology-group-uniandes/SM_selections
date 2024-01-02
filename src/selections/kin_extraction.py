import hashlib
import logging
import os
import sqlite3

import pandas as pd
import ROOT
import Zboson

selections = {"z_lep_lep": Zboson.lep_lep_selection}
chain_key = {"MC": "delphes", "data": "mini"}


def get_file_id(file_path):
    return hashlib.md5(file_path.encode()).hexdigest()[:10]


def kinematics_extraction(file_path, sql_db_path, data_type):
    logging.basicConfig(
        filename=os.path.join(os.path.dirname(file_path), "selections.log"),
        level=logging.INFO,
    )
    logging.info("Processing file: {}".format(file_path))

    tree = ROOT.TChain(chain_key[data_type])
    tree.Add(file_path)
    n_entries = tree.GetEntries()
    if n_entries == 0:
        logging.warning("File {} has no entries".format(file_path))
        return False

    sql_conn = sqlite3.connect(sql_db_path)
    file_properties = {
        "file_id": get_file_id(file_path),
        "file_path": file_path,
        "data_type": data_type,
        "n_entries": n_entries,
    }
    logging.info(f"File properties: {file_properties}")

    pd.DataFrame.from_records([file_properties]).to_sql(
        "tbFiles", sql_conn, if_exists="append", index=False
    )

    results = {selection: [] for selection in selections.keys()}
    for event in tree:
        for selection, selection_function in selections.items():
            kin_row = selection_function(event, data_type)
            if kin_row:
                kin_row["file_id"] = file_properties["file_id"]
                results[selection].append(kin_row)
    for selection in results.keys():
        df = pd.DataFrame.from_records(results[selection])
        df.to_sql(
            "tb{}".format(selection),
            sql_conn,
            if_exists="append",
            index=False,
        )

    sql_conn.close()

    return True
