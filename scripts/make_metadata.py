import json
from pathlib import Path

import numpy as np
from pyobsbox import DB
from pyobsbox.utils import df_to_name

if __name__ == "__main__":
    save_folder = Path("../metadata")
    no_data_file = save_folder / "no_data.json"

    # building up a list of files which don't contain any data
    if no_data_file.is_file():
        with no_data_file.open("r") as fp:
            known_no_data = json.load(fp)
            known_no_data = set(known_no_data)
    else:
        known_no_data = set()

    db = DB(n_jobs=40)
    df = db.load()
    df = df[(df["beam"] == 1) & (df["plane"] == "v") & (df["type"] == "Inst")]
    # remove known empty files from the pool
    files = list(set(df["file"].unique()) - known_no_data)
    # select more files to make up for files which contain 0 populated bunches
    # files = np.random.choice(files, 1024 + 128, replace=False)
    df = db.load(files=files, ts_info=True)

    # update list of known empty files
    no_data = df["file"][df["n_bunches"] == 0].to_list()
    no_data = list(known_no_data | set(no_data))
    with no_data_file.open("w+") as fp:
        json.dump(no_data, fp, indent=4)

    # drop the empty data
    df.dropna(inplace=True)

    # cut down to 1024
    # fetched_files = df["file"].unique()
    # keep_files = np.random.choice(fetched_files, 1024, replace=False)
    # df = df[df['file'].isin(keep_files)]
    save_path = save_folder / df_to_name(df)
    df.to_hdf(save_path, "metadata")
    print("Saved to :", save_path)
