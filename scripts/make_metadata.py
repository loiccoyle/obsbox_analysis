from pyobsbox import DB
from pathlib import Path

if __name__ == "__main__":
    save_path = Path("../metadata") / "metadata_B1H.h5"
    db = DB(n_jobs=32)
    df = db.load()
    df = df[(df["beam"] == 1) & (df["plane"] == "h") & (df["type"] == "Inst")]
    files = df["file"]  # [:1024]
    df = db.load(files=files, ts_info=True)
    df.to_hdf(save_path, "metadata")

