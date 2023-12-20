import hashlib
import logging
import os

import pandas as pd
import ROOT


def get_file_id(file_path):
    return hashlib.md5(file_path.encode()).hexdigest()[:10]


def process_file(
    file_path, sql_conn, sql_table, selection_function, data_type
):
    logging.info("Processing file: {}".format(file_path))
    tree = ROOT.TChain("mini")
    tree.Add(file_path)
    n_entries = tree.GetEntries()
    logging.info("Number of entries: {}".format(n_entries))

    file_properties = {
        "file_id": get_file_id(file_path),
        "file_path": file_path,
        "data_type": data_type,
        "n_entries": n_entries,
    }

    pd.DataFrame.from_records([file_properties]).to_sql(
        "tbFiles", sql_conn, if_exists="append", index=False
    )

    results = []
    for event in tree:
        kin_row = selection_function(event, data_type)
        if kin_row:
            kin_row["file_id"] = get_file_id(file_path)
            results.append(kin_row)

    df = pd.DataFrame.from_records(results)
    df.to_sql(sql_table, sql_conn, if_exists="append", index=False)
    logging.info("Finished processing file: {}".format(file_path))
