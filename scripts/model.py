import json
from pathlib import Path

import pandas as pd
from pyobsbox import ObsBoxGenerator
from pyobsbox.models import make_lstm_ae, make_conv_ae
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
        train_metadata,
        metadata_path=metadata_path,
        n_bunches=512,
        sequence_length=2048,
        shuffle=True,
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
    hist = model.fit(
        generator,
        steps_per_epoch=10,
        validation_data=validation_generator,
        validation_steps=2,
        epochs=25,
        use_multiprocessing=False,
        workers=8,
    )
    # Save the model to file
    model_name = df_to_name(metadata_df, base="model", extension="")
    model_path = models_folder / model_name
    while model_path.is_dir():
        model_path = models_folder / (model_path.name + "_")
    model.save(model_path)
    # save model metadata
    model_metadata = {}
    model_metadata["generator"] = generator.to_dict()
    model_metadata["history"] = hist.history
    model_metadata["train_indices"] = train_metadata.index.to_list()
    model_metadata["validation_indices"] = validation_metadata.index.to_list()
    json.dump(model_metadata, (model_path / "metadata.json").open("w"))
    generator.fetched.to_hdf(model_path / "seen_train_metadata.h5", key='metadata')
    validation_generator.fetched.to_hdf(model_path / "seen_validation_metadata.h5", key="metadata")
