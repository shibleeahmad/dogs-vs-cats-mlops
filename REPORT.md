# Dogs vs Cats Image Classification — MLOps Assignment Report

## 1. Project Overview

This project implements a reproducible machine learning workflow for binary image classification of dogs and cats. The project uses Git for version control and collaboration, DVC for dataset versioning and reproducibility, DagsHub as the DVC remote, and GitHub Actions for continuous integration.

The machine learning model is an RBF-kernel Support Vector Machine (SVM) trained on Histogram of Oriented Gradients (HOG) image features.

**Repository:** https://github.com/shibleeahmad/dogs-vs-cats-mlops.git

**DagsHub:** https://dagshub.com/shibleeahmad/dogs-vs-cats-mlops

---

## 2. Team and Git Workflow

The project was developed by a two-member team using a protected Git workflow.

Permanent branches:

* `main` — release branch
* `staging` — final validation branch
* `dev` — integration/development branch

Short-lived branches were used for individual tasks, experiments, fixes, and demonstrations.

Examples include:

* `feat/ci`
* `fix/ignore-dvc-metrics`
* `fix/restore-baseline-lock`
* `fix/resolve-params-conflict`
* `exp/shiblee-conflict`

Direct pushes to the protected integration and release branches were prevented through GitHub branch protection. Changes were therefore submitted through pull requests and reviewed before merging.

---

## 3. Dataset and DVC

The project uses a subset of the Dogs vs Cats dataset containing:

* 1,000 training images
* 200 validation images
* 100 test images
* 1,300 images in total
* 1 dataset license document

The dataset is stored locally under:

`data/raw/dogs_vs_cats_subset`

The dataset is tracked by DVC rather than Git. The Git repository stores the DVC pointer file:

`data/raw/dogs_vs_cats_subset.dvc`

DagsHub was configured as the DVC remote so that the dataset can be retrieved without committing the large image files directly to Git.

The dataset archive was obtained from Zenodo:

https://zenodo.org/records/10997322

---

## 4. Project Structure

The main project structure is:

```text
dogs-vs-cats-mlops/
├── data/
│   └── raw/
│       ├── dogs_vs_cats_subset/
│       └── dogs_vs_cats_subset.dvc
├── models/
├── src/
│   ├── __init__.py
│   └── train.py
├── tests/
│   └── test_train.py
├── .github/
│   └── workflows/
│       └── ci.yml
├── .gitignore
├── .pre-commit-config.yaml
├── CONTRIBUTING.md
├── dvc.yaml
├── params.yaml
├── pytest.ini
├── requirements.txt
└── README.md
```

---

## 5. Machine Learning Pipeline

The training pipeline is defined in `dvc.yaml`.

The pipeline performs the following operations:

1. Loads the training and validation images.
2. Converts images to grayscale.
3. Resizes images to 64 × 64 pixels.
4. Extracts HOG features.
5. Trains an RBF-kernel SVM.
6. Evaluates the model.
7. Saves the trained model to `models/model.joblib`.
8. Records evaluation metrics in `metrics.json`.

The main configurable parameters are stored in `params.yaml`.

Baseline configuration:

```yaml
seed: 42

data:
  image_size: 64
  train_dir: data/raw/dogs_vs_cats_subset/train
  val_dir: data/raw/dogs_vs_cats_subset/val
  test_dir: data/raw/dogs_vs_cats_subset/test

model:
  type: svm
  kernel: rbf
  C: 1.0
  gamma: scale

features:
  pixels_per_cell: 8
  cells_per_block: 2
  orientations: 9
```

---

## 6. Baseline Model

The baseline configuration uses:

* Model: SVM
* Kernel: RBF
* `C = 1.0`
* `gamma = scale`
* Image size: 64 × 64
* HOG pixels per cell: 8
* HOG cells per block: 2
* HOG orientations: 9
* Random seed: 42

Baseline performance:

| Configuration          | Accuracy | F1 Score |
| ---------------------- | -------: | -------: |
| C = 1.0, gamma = scale |   0.7650 |   0.7685 |

The baseline was retained as the selected model because it achieved the best overall accuracy and F1 score among the tested configurations.

---

## 7. Experiment Comparison

Three parameter variations were tested against the baseline.

| Run          |    C | Gamma | Accuracy | F1 Score |
| ------------ | ---: | ----- | -------: | -------: |
| Baseline     |  1.0 | scale |   0.7650 |   0.7685 |
| Experiment 1 |  0.1 | scale |   0.7000 |   0.6591 |
| Experiment 2 | 10.0 | scale |   0.7550 |   0.7633 |
| Experiment 3 |  1.0 | 0.01  |   0.7150 |   0.7273 |

### Experiment Analysis

Experiment 1 reduced `C` from 1.0 to 0.1 and resulted in a significant reduction in both accuracy and F1 score.

Experiment 2 increased `C` to 10.0. Its performance was close to the baseline but remained slightly lower.

Experiment 3 changed `gamma` from `scale` to `0.01`, which also reduced performance.

Therefore, the baseline configuration of `C = 1.0` and `gamma = scale` was selected.

### Reproducibility Note

The baseline configuration and pipeline are tracked through Git and DVC. The additional parameter comparisons were executed directly using the reproducible training script after retrieving the DVC dataset. They were used for model comparison but were not all retained as permanent DVC experiment references.

---

## 8. Testing

A unit test was created for the training data-loading functionality.

The test verifies that:

* image data can be loaded,
* both cat and dog classes are recognized,
* the expected number of samples is produced for the test images,
* HOG feature extraction produces a non-empty feature vector.

The test suite was executed successfully:

```text
1 passed
```

---

## 9. Pre-Commit Quality Controls

Pre-commit hooks were configured to improve repository quality and prevent accidental commits of problematic files.

The configured checks include:

* Ruff
* Ruff formatting
* nbstripout
* large-file detection
* secret detection

The complete pre-commit check was successfully executed.

Two security demonstrations were also performed:

1. A large file exceeding the configured limit was blocked.
2. A fake AWS-style secret was detected and blocked.

These demonstrations show that repository-level controls can prevent common accidental commits before they reach GitHub.

---

## 10. Merge Conflict Demonstration

A merge conflict was intentionally created in `params.yaml`.

Two branches modified the same parameter with different values:

* one branch changed `C` to `5.0`
* another changed `C` to `2.0`

The branches were merged, producing a content conflict.

The conflict was manually resolved by restoring the intended baseline value:

```text
C = 1.0
```

The resolution was committed and subsequently submitted through a pull request because direct pushes to the protected `dev` branch were rejected.

This demonstrated the team's conflict-resolution and protected-branch workflow.

---

## 11. Continuous Integration

A GitHub Actions workflow was created at:

`.github/workflows/ci.yml`

The workflow runs on pushes and pull requests involving the main project branches.

The CI workflow:

1. Checks out the repository.
2. Sets up Python 3.13.
3. Installs project dependencies.
4. Installs pytest.
5. Runs the test suite.

The workflow initially used Python 3.10, but dependency installation failed because the project's NumPy requirement was incompatible with the selected Python version.

The workflow was corrected to Python 3.13.

After the correction, all GitHub Actions checks passed successfully and the CI pull request was reviewed and merged.

---

## 12. Pull Request Review Workflow

Development was integrated through pull requests rather than direct changes to protected branches.

Major reviewed changes included:

* dataset and DVC integration
* reproducible training pipeline
* unit testing
* teammate EDA work
* DVC metrics tracking
* `.gitignore` corrections
* baseline lock restoration
* merge-conflict resolution
* GitHub Actions CI

Pull requests were reviewed and approved before merging where required.

---

## 13. Reproducibility

The project separates source code, configuration, and large datasets.

Git tracks:

* source code
* configuration
* DVC pointer files
* tests
* CI configuration
* documentation

DVC tracks the dataset and stores the dataset content in the configured DagsHub remote.

The model configuration is controlled through `params.yaml`, while the training process is defined in `dvc.yaml`.

A clean environment can therefore obtain the repository, retrieve the DVC dataset, install the required dependencies, and execute the training code using the same configuration.

---

## 14. Branch Promotion and Release

The intended promotion workflow is:

```text
feature branches
       ↓
      dev
       ↓
   staging
       ↓
     main
       ↓
 model-v1.0
```

The `dev` branch contains the reviewed development work. The completed CI changes were merged into `dev`.

The next stage is final staging validation, followed by promotion to `main` and creation of the `model-v1.0` release tag.

---

## 15. Conclusion

This project demonstrates an end-to-end Git-based MLOps workflow for a small image-classification problem.

The final workflow combines Git branching and pull-request reviews with DVC dataset versioning, DagsHub remote storage, a parameterized training pipeline, automated testing, pre-commit quality checks, merge-conflict handling, and GitHub Actions CI.

The baseline SVM configuration achieved an accuracy of 0.7650 and an F1 score of 0.7685 on the evaluation data used in the project. The tested alternatives did not improve upon the baseline, so the original configuration was retained.

The resulting project provides a structured and reproducible foundation for developing, testing, reviewing, and releasing the Dogs vs Cats classification model.
