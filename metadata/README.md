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

### `metadata_B1H_Inst_32.h5`:
 * beam: 1
 * plane: horizontal
 * type: instability
 * subset: True, a subset of a randomly selected 32 files.
 * shape: (10274, 10)

### `metadata_B1H_Inst_1024.h5`:
 * beam: 1
 * plane: horizontal
 * type: instability
 * subset: True, a subset of a randomly selected 1024 files.
 * shape: (369627, 10)

### `metadata_B1H_Inst_34993.h5`:
* beam: 1
* plane: horizontal
* type: instability
* subset: False
* shape: (11725302, 11)  (note: "date_time" is not the index)

### `metadata_B1V_Inst_51335.h5`:
* beam: 1
* plane: vertical
* type: instability
* subset: False
* shape: (12305947, 11)  (note: "date_time" is not the index)

### `metadata_B2H_Inst_23528.h5`:
* beam: 2
* plane: horizontal
* type: instability
* subset: False
* shape: (15850511, 11)  (note: "date_time" is not the index)

### `metadata_B2V_Inst_60652.h5`:
* beam: 2
* plane: vertical
* type: instability
* subset: False
* shape: (17435804, 11)  (note: "date_time" is not the index)
