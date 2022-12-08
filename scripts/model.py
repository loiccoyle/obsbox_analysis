import json
import logging

import numpy as np
import pandas as pd
from pyobsbox import ObsBoxGenerator
from pyobsbox.models import (
    make_lstm_ae,
    make_conv_ae,
    make_time_distributed_ae,
    make_dense_ae,
    make_conv_ae_2,
    make_conv_max_pool_ae,
)
from pyobsbox.utils import df_to_name

from paths import metadata_folder, models_folder

if __name__ == "__main__":
    logging.getLogger("pyobsbox").setLevel(logging.INFO)

    metadata_path = metadata_folder / "metadata_B1H_Inst_34994.h5"
    metadata_df = pd.read_hdf(metadata_path, "metadata")
    # remove date time index
    metadata_df = metadata_df.reset_index()

    # model name
    model_path = (
        models_folder
        / "model_conv_64_32_16_8_stride_4_noDO_decode_B1H_Inst_min_max_rolling_avg_std_window_17_seed_42"
    )
    while model_path.is_dir():
        model_path = models_folder / (model_path.name + "_")
    model_path.mkdir()

    # create training and validation
    validation_metadata = metadata_df.sample(frac=0.1)
    train_metadata = metadata_df.drop(validation_metadata.index)

    generator = ObsBoxGenerator(
        train_metadata,
        metadata_path=metadata_path,
        n_bunches=256,
        sequence_length=2048,
        shuffle=True,
        seed=42,
        fetched_log_folder=model_path,
        fetched_log_prefix="train",
        normalization="min_max",
        normalization_pre_split=False,
        normalization_kwargs={},
        abs_diff=False,
        diff=False,
        rolling_avg=True,
        rolling_std=True,
        rolling_window=17,
        return_window_size=None,
    )
    validation_generator = ObsBoxGenerator(
        validation_metadata,
        n_bunches=generator.n_bunches,
        sequence_length=generator.sequence_length,
        shuffle=generator.shuffle,
        seed=generator.seed,
        fetched_log_folder=model_path,
        fetched_log_prefix="validation",
        normalization=generator.normalization,
        normalization_pre_split=generator.normalization_pre_split,
        normalization_kwargs=generator.normalization_kwargs,
        abs_diff=generator.abs_diff,
        diff=generator.diff,
        rolling_avg=generator.rolling_avg,
        rolling_std=generator.rolling_std,
        rolling_window=generator.rolling_window,
        return_window_size=generator.return_window_size,
    )
    # create model
    # model = make_conv_max_pool_ae(generator.sequence_length)
    # model = make_dense_ae(generator.sequence_length, 2)
    # model = make_lstm_ae(generator.return_window_size, 2)
    model_kwargs = {
        "encoder_sizes": [64, 32, 16, 8],
        "encoder_strides": [4, 4, 4, 4],
        "encoder_dropout": 0.2,
        "decoder_sizes": None,
        "decoder_strides": None,
        "decoder_dropout": None,
    }
    model = make_conv_ae_2(generator.sequence_length, 2, **model_kwargs)
    model.compile(loss="mse", optimizer="adam")
    model.summary()
    # train
    train_kwargs = {
        "steps_per_epoch": 10,
        "validation_steps": 4,
        "epochs": 50,
        # "use_multiprocessing": True,
        # "workers": 10,
        # "use_multiprocessing": False,
        # "workers": 1,
    }
    hist = model.fit(generator, validation_data=validation_generator, **train_kwargs)
    # Save the model to file
    print("model save path: ", model_path)
    model.save(model_path)
    # Save train kwargs
    json.dump(train_kwargs, (model_path / "train_kwargs.json").open("w"))
    # save model metadata
    model_metadata = {}
    model_metadata["generator"] = generator.to_dict()
    model_metadata["history"] = hist.history
    json.dump(model_metadata, (model_path / "metadata.json").open("w"))
    json.dump(model_kwargs, (model_path / "model_kwargs.json").open("w"))

    # save the train validation splitting
    train_split_indices = train_metadata.index.to_numpy()
    validation_split_indices = validation_metadata.index.to_numpy()
    np.save(model_path / "train_split_indices.npy", train_split_indices)
    np.save(model_path / "validation_split_indices.npy", validation_split_indices)

    # cleanup the logs
    generator.cleanup_logs()
    validation_generator.cleanup_logs()
