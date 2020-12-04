# obsbox metadata:

To download the files run:
```sh
make download_metadata
```

These files contain information regarding the ObsBox data.
They contain `pd.DataFrames` stored in the "metadata" key.
Each row represents one bunch and the various columns contian information regarding the file, the bunch population and other interesting pieces of information.

Keys:
 * `type`: data type
 * `fill`: fill number
 * `beam`: beam number
 * `plane`: "h" or "v"
 * `q`:
 * `file`: file path
 * `n_bunches`: number of bunches
 * `bunch_index`: index of the bunch in the array
 * `bunch_number`: bunch number
 * `ts_length`: time series length

### `metadata_B1H_1024.h5`:
 * beam: 1
 * plane: horizontal
 * type: instability
 * subset: True, a subset of a randomly selected 1024 files.
 * shape: (422922, 10)

### `metadata_B1H.h5`:
 * beam: 1
 * plane: horizontal
 * type: instability
 * subset: False
 * shape: (13670154, 10)
