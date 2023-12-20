# This file contains helper functions for the Atlas_Reader_13TeV module.

import logging
import os
from pathlib import Path
from urllib.parse import urljoin

import wget


def download_atlas_opendataset(analysis: str, output_path: str):
    """
    Downloads ATLAS open dataset files for a given analysis and stores them in
    the specified output path.

    Parameters:
    analysis (str): The analysis type.
    output_path (str): The path where the downloaded files will be stored.

    Returns:
    list: A list of paths to the downloaded files.
    """

    file_names = [f"data_{i}.{analysis}.root" for i in ["A", "B", "C", "D"]]
    opendata_url = (
        "https://atlas-opendata.web.cern.ch/atlas-opendata/samples/2020/"
    )
    files_urls = [
        urljoin(opendata_url, "/".join([analysis, "Data", file_name]))
        for file_name in file_names
    ]

    output_path = Path(output_path)
    files_paths = [
        output_path / analysis / file_name for file_name in file_names
    ]

    for file_url, file_path in zip(files_urls, files_paths):
        logging.info("Downloading file:\n\t%s", file_url)
        file_path.parent.mkdir(parents=True, exist_ok=True)
        if not file_path.exists():
            try:
                wget.download(file_url, out=str(file_path))
            except Exception as e:
                logging.error(
                    "Error downloading file: %s. Error: %s", file_url, e
                )
                raise e
        else:
            logging.warning("Skipping file, already exists: %s", file_path)
    logging.info(f"Dataset {analysis} downloaded successfully.")

    return [str(file_path) for file_path in files_paths]
