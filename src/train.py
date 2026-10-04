import json
import random
from pathlib import Path

import joblib
import numpy as np
import yaml
from PIL import Image
from skimage.feature import hog
from sklearn.metrics import accuracy_score, f1_score
from sklearn.svm import SVC


def set_seed(seed):
    random.seed(seed)
    np.random.seed(seed)


def load_dataset(directory, image_size, orientations, pixels_per_cell, cells_per_block):
    features = []
    labels = []

    for path in sorted(Path(directory).glob("*")):
        if path.suffix.lower() not in {".jpg", ".jpeg", ".png"}:
            continue

        label = 0 if path.name.lower().startswith("cat") else 1

        image = Image.open(path).convert("L")
        image = image.resize((image_size, image_size))

        feature = hog(
            np.array(image),
            orientations=orientations,
            pixels_per_cell=(pixels_per_cell, pixels_per_cell),
            cells_per_block=(cells_per_block, cells_per_block),
        )

        features.append(feature)
        labels.append(label)

    return np.array(features), np.array(labels)


def main():
    with open("params.yaml", encoding="utf-8") as file:
        params = yaml.safe_load(file)

    set_seed(params["seed"])

    image_size = params["data"]["image_size"]
    orientations = params["features"]["orientations"]
    pixels_per_cell = params["features"]["pixels_per_cell"]
    cells_per_block = params["features"]["cells_per_block"]

    X_train, y_train = load_dataset(
        params["data"]["train_dir"],
        image_size,
        orientations,
        pixels_per_cell,
        cells_per_block,
    )

    X_val, y_val = load_dataset(
        params["data"]["val_dir"],
        image_size,
        orientations,
        pixels_per_cell,
        cells_per_block,
    )

    model = SVC(
        kernel=params["model"]["kernel"],
        C=params["model"]["C"],
        gamma=params["model"]["gamma"],
        random_state=params["seed"],
    )

    model.fit(X_train, y_train)

    predictions = model.predict(X_val)

    metrics = {
        "accuracy": float(accuracy_score(y_val, predictions)),
        "f1_score": float(f1_score(y_val, predictions)),
    }

    Path("models").mkdir(exist_ok=True)
    joblib.dump(model, "models/model.joblib")

    Path("metrics.json").write_text(
        json.dumps(metrics, indent=2),
        encoding="utf-8",
    )

    print(f"Validation accuracy: {metrics['accuracy']:.4f}")
    print(f"Validation F1: {metrics['f1_score']:.4f}")


if __name__ == "__main__":
    main()
