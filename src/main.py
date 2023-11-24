import os
import sqlite3
from urllib.parse import urljoin

import pandas as pd
import ROOT
import wget
from tqdm import tqdm

from selections.Zboson import lep_lep_selection

analysis = "2lep"
data_type = "Data"
file_names = [
    "data_{}.{}.root".format(data_type, analysis)
    for data_type in ["A", "B", "C", "D"]
]


opendata_url = (
    "https://atlas-opendata.web.cern.ch/atlas-opendata/samples/2020/"
)


data_path = os.path.join(os.path.dirname(os.getcwd()), "archive", analysis)
output_path = os.path.join(os.sep, "output", analysis)
db_file = "kin_row.db"
db_path = os.path.join(output_path, db_file)
os.makedirs(data_path, exist_ok=True)
os.makedirs(output_path, exist_ok=True)
if os.path.exists(db_path):
    os.remove(db_path)


# Invariant mass histograms definition
hist = ROOT.TH1F(
    "z_mass",
    "Dilepton invariant-mass ; Invariant Mass m_{ll} [GeV] ; events",
    30,
    66,
    116,
)
canvas = ROOT.TCanvas("canvas", "canvas", 800, 600)
canvas.SetLogy()
conn = sqlite3.connect(db_path)


def process_file(file_name):
    relative_url = "/".join([analysis, data_type, file_name])
    file_url = urljoin(opendata_url, relative_url)

    file = os.path.join(output_path, file_name)

    if not os.path.exists(file):
        wget.download(file_url, out=file)

    tree = ROOT.TChain("mini")
    tree.Add(file)
    n_batches = 100

    batch_size = tree.GetEntries() // n_batches

    def process_batch(n):
        results = []
        for i in range(batch_size):
            tree.GetEntry(n * batch_size + i)
            kin_row = lep_lep_selection(tree, "Data")
            if kin_row:
                results.append(kin_row)
        df = pd.DataFrame.from_records(results)
        df.to_sql(analysis, conn, if_exists="append", index=False)
        for dat in df["reco_z_mass"]:
            hist.Fill(dat)
        hist.Draw()
        canvas.Update()

    list(tqdm(map(process_batch, range(n_batches)), total=n_batches))


from multiprocessing import Pool

with Pool(4) as p:
    p.map(process_file, file_names)


hist.Draw()
canvas.Draw()
canvas.SaveAs(os.path.join(data_path, "z_mass.pdf"))

conn.close()
