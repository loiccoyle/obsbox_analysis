from pyobsbox import ObsBoxGenerator

import pandas as pd
from pathlib import Path

if __name__ == "__main__":
    metadata_path = Path("../metadata") / "metadata_B1H_1024.h5"
    metadata_df = pd.read_hdf(metadata_path, "metadata")
    generator = ObsBoxGenerator(metadata_df, n_bunches=2048, sequence_length=2048)
