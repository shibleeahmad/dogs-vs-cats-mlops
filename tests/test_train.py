import numpy as np
from PIL import Image

from src.train import load_dataset


def test_load_dataset_extracts_features_and_labels(tmp_path):
    cat_path = tmp_path / "cat.test.jpg"
    dog_path = tmp_path / "dog.test.jpg"

    Image.fromarray(np.zeros((64, 64), dtype=np.uint8)).save(cat_path)
    Image.fromarray(np.ones((64, 64), dtype=np.uint8) * 255).save(dog_path)

    features, labels = load_dataset(
        tmp_path,
        image_size=64,
        orientations=9,
        pixels_per_cell=8,
        cells_per_block=2,
    )

    assert features.shape[0] == 2
    assert labels.tolist() == [0, 1]
    assert features.shape[1] > 0
