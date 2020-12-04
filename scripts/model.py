from pathlib import Path

import pandas as pd
from pyobsbox import ObsBoxGenerator, make_lstm_ae, make_conv_ae

if __name__ == "__main__":
    metadata_path = Path("../metadata") / "metadata_B1H.h5"
    metadata_df = pd.read_hdf(metadata_path, "metadata")
    # remove date time index
    metadata_df = metadata_df.reset_index()

    # create training and validation
    validataion_metadata = metadata_df.sample(frac=0.1)
    train_metadata = metadata_df.drop(validataion_metadata.index)

    generator = ObsBoxGenerator(train_metadata, n_bunches=128, sequence_length=2048)
    validation_generator = ObsBoxGenerator(
        validataion_metadata,
        n_bunches=generator.n_bunches,
        sequence_length=generator.sequence_length,
    )
    model = make_conv_ae(generator.sequence_length)
    model.compile(loss="mse", optimizer="adam")
    model.summary()

    print("To train run: model.fit(generator, validation_data=validation_generator)")
