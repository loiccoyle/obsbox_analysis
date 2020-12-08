import json
from pathlib import Path

import pandas as pd
from pyobsbox import ObsBoxGenerator, make_lstm_ae, make_conv_ae
from pyobsbox.utils import df_to_name

from paths import metadata_folder, models_folder

if __name__ == "__main__":
    metadata_path = metadata_folder / "metadata_B1H_Inst_34994.h5"
    metadata_df = pd.read_hdf(metadata_path, "metadata")
    # remove date time index
    metadata_df = metadata_df.reset_index()

    # create training and validation
    validation_metadata = metadata_df.sample(frac=0.1)
    train_metadata = metadata_df.drop(validation_metadata.index)

    generator = ObsBoxGenerator(
        train_metadata, metadata_path=metadata_path, n_bunches=128, sequence_length=2048
    )
    validation_generator = ObsBoxGenerator(
        validation_metadata,
        n_bunches=generator.n_bunches,
        sequence_length=generator.sequence_length,
    )
    # create model
    model = make_conv_ae(generator.sequence_length)
    model.compile(loss="mse", optimizer="adam")
    model.summary()
    # train
    hist = model.fit(generator, validation_data=validation_generator, epochs=5)
    # Save the model to file
    model_name = df_to_name(metadata_df, base="model", extension="")
    model_path = models_folder / model_name
    while model_path.is_dir():
        model_path = models_folder / (model_path.name + "_")
    model.save(model_path)
    json.dump(hist.history, (model_path / "history.json").open("w"))
    json.dump(generator.to_dict(), (model_path / "generator.json").open("w"))
    json.dump(train_metadata.index.to_list(), (model_path / "train_index.json").open("w"))
    json.dump(validation_metadata.index.to_list(), (model_path / "validation_index.json").open("w"))
    json.dump(generator.to_dict(), (model_path / "generator.json").open("w"))
