---
agents:
- none
category: chain
description: Dataset preparation for ML, HuggingFace datasets, custom loaders, data
  validation with Great Expectations, feature engineering, data versioning with DVC,
  preprocessing pipelines
knowledge:
- none
name: processing-data-pipelines
related_skills:
- none
templates:
- none
tools:
- none
type: skill
version: 1.0.0
---
# Data Pipeline

Dataset preparation for ML, HuggingFace datasets, custom loaders, data validation with Great Expectations, feature engineering, data versioning with DVC, preprocessing pipelines

Build robust data pipelines for machine learning including dataset preparation, validation, feature engineering, versioning, and preprocessing. Handle HuggingFace datasets, custom loaders, and ensure data quality throughout the ML lifecycle.

## Process

1. Review the task requirements.
2. Apply the skill's methodology.
3. Validate the output against the defined criteria.
### Step 1: Dataset Preparation with HuggingFace Datasets

Create and manage datasets using HuggingFace datasets:

```python
from datasets import Dataset, DatasetDict, load_dataset, load_from_disk
from transformers import AutoTokenizer
import pandas as pd
import json

class DatasetPreparer:
    """Prepare datasets for ML training."""

    def __init__(self):
        self.datasets = {}

    def from_pandas(self, df: pd.DataFrame, split: str = "train") -> Dataset:
        """Create dataset from pandas DataFrame."""
        dataset = Dataset.from_pandas(df)
        return dataset

    def from_dict(self, data: dict) -> Dataset:
        """Create dataset from dictionary."""
        return Dataset.from_dict(data)

    def from_json(self, json_path: str, text_key: str = "text") -> Dataset:
        """Load dataset from JSON file."""
        with open(json_path, "r") as f:
            data = json.load(f)

        # Handle different JSON formats
        if isinstance(data, list):
            return Dataset.from_list(data)
        elif isinstance(data, dict):
            return Dataset.from_dict(data)
        else:
            raise ValueError("Unsupported JSON format")

    def from_csv(self, csv_path: str, **kwargs) -> Dataset:
        """Load dataset from CSV."""
        df = pd.read_csv(csv_path, **kwargs)
        return Dataset.from_pandas(df)

    def create_train_val_split(
        self,
        dataset: Dataset,
        train_ratio: float = 0.8,
        seed: int = 42
    ) -> DatasetDict:
        """Split dataset into train/validation."""
        split_dataset = dataset.train_test_split(
            train_size=train_ratio,
            seed=seed
        )
        return DatasetDict({
            "train": split_dataset["train"],
            "validation": split_dataset["test"]
        })

    def save_dataset(self, dataset: Dataset, path: str):
        """Save dataset to disk."""
        dataset.save_to_disk(path)

    def load_dataset(self, path: str) -> Dataset:
        """Load dataset from disk."""
        return load_from_disk(path)

    def prepare_for_training(
        self,
        dataset: Dataset,
        text_column: str = "text",
        label_column: str = "label",
        tokenizer_name: str = "bert-base-uncased"
    ) -> Dataset:
        """Prepare dataset for training with tokenization."""
        tokenizer = AutoTokenizer.from_pretrained(tokenizer_name)

        def tokenize_function(examples):
            return tokenizer(
                examples[text_column],
                truncation=True,
                padding="max_length",
                max_length=512
            )

        tokenized_dataset = dataset.map(
            tokenize_function,
            batched=True,
            remove_columns=[col for col in dataset.column_names if col != label_column]
        )

        return tokenized_dataset

# Usage
preparer = DatasetPreparer()

# From CSV
dataset = preparer.from_csv("data.csv")

# From JSON
dataset = preparer.from_json("data.json")

# Split
dataset_dict = preparer.create_train_val_split(dataset, train_ratio=0.8)

# Save
preparer.save_dataset(dataset_dict["train"], "./data/train")
preparer.save_dataset(dataset_dict["validation"], "./data/val")
```

### Step 2: Custom Dataset Loaders

Create custom dataset loaders for specific data formats:

```python
from torch.utils.data import Dataset, DataLoader
from typing import List, Dict, Tuple
import torch

class CustomTextDataset(Dataset):
    """Custom dataset for text classification."""

    def __init__(
        self,
        texts: List[str],
        labels: List[int],
        tokenizer,
        max_length: int = 512
    ):
        self.texts = texts
        self.labels = labels
        self.tokenizer = tokenizer
        self.max_length = max_length

    def __len__(self):
        return len(self.texts)

    def __getitem__(self, idx):
        text = self.texts[idx]
        label = self.labels[idx]

        # Tokenize
        encoding = self.tokenizer(
            text,
            truncation=True,
            padding="max_length",
            max_length=self.max_length,
            return_tensors="pt"
        )

        return {
            "input_ids": encoding["input_ids"].flatten(),
            "attention_mask": encoding["attention_mask"].flatten(),
            "labels": torch.tensor(label, dtype=torch.long)
        }

class StreamingDataset(Dataset):
    """Dataset that streams data from disk."""

    def __init__(self, file_paths: List[str], batch_size: int = 1000):
        self.file_paths = file_paths
        self.batch_size = batch_size
        self.current_file_idx = 0
        self.current_batch = []
        self._load_next_batch()

    def _load_next_batch(self):
        """Load next batch from current file."""
        if self.current_file_idx >= len(self.file_paths):
            return

        file_path = self.file_paths[self.current_file_idx]
        # Load batch from file
        with open(file_path, "r") as f:
            data = json.load(f)
            self.current_batch = data[:self.batch_size]

        self.current_file_idx += 1

    def __len__(self):
        return len(self.file_paths) * self.batch_size

    def __getitem__(self, idx):
        batch_idx = idx % self.batch_size
        if batch_idx == 0 and idx > 0:
            self._load_next_batch()

        if batch_idx < len(self.current_batch):
            return self.current_batch[batch_idx]
        else:
            raise IndexError("Dataset exhausted")

# Usage
from transformers import AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
dataset = CustomTextDataset(
    texts=["Text 1", "Text 2"],
    labels=[0, 1],
    tokenizer=tokenizer
)

dataloader = DataLoader(dataset, batch_size=32, shuffle=True)
```

### Step 3: Data Validation with Great Expectations

Validate data quality using Great Expectations:

```python
from great_expectations.core import ExpectationSuite
from great_expectations.dataset import PandasDataset
import great_expectations as ge
import pandas as pd

class DataValidator:
    """Validate data quality with Great Expectations."""

    def __init__(self, context_root_dir: str = "./great_expectations"):
        self.context = ge.get_context()
        self.suite_name = "data_quality_suite"

    def create_expectation_suite(self, suite_name: str = None):
        """Create expectation suite."""
        if suite_name is None:
            suite_name = self.suite_name

        suite = self.context.create_expectation_suite(
            expectation_suite_name=suite_name,
            overwrite_existing=True
        )
        return suite

    def validate_dataframe(
        self,
        df: pd.DataFrame,
        suite_name: str = None
    ) -> dict:
        """Validate DataFrame against expectations."""
        if suite_name is None:
            suite_name = self.suite_name

        # Create validator
        validator = self.context.get_validator(
            batch_request={
                "datasource_name": "pandas_datasource",
                "data_asset_name": "my_dataframe"
            },
            expectation_suite_name=suite_name
        )

        # Run validation
        checkpoint_result = validator.validate()
        return checkpoint_result

    def add_expectations(
        self,
        df: pd.DataFrame,
        expectations: dict
    ):
        """Add custom expectations."""
        ge_df = ge.from_pandas(df)

        # Column expectations
        if "columns" in expectations:
            for col, col_expectations in expectations["columns"].items():
                if "not_null" in col_expectations:
                    ge_df.expect_column_values_to_not_be_null(col)

                if "unique" in col_expectations:
                    ge_df.expect_column_values_to_be_unique(col)

                if "in_range" in col_expectations:
                    min_val, max_val = col_expectations["in_range"]
                    ge_df.expect_column_values_to_be_between(col, min_val, max_val)

                if "in_set" in col_expectations:
                    ge_df.expect_column_values_to_be_in_set(col, col_expectations["in_set"])

        # Row expectations
        if "row_count" in expectations:
            min_rows, max_rows = expectations["row_count"]
            ge_df.expect_table_row_count_to_be_between(min_rows, max_rows)

        return ge_df

    def validate_dataset(
        self,
        dataset_path: str,
        expectations_config: dict
    ) -> dict:
        """Validate dataset file."""
        # Load dataset
        df = pd.read_csv(dataset_path)  # or other format

        # Add expectations
        ge_df = self.add_expectations(df, expectations_config)

        # Validate
        results = ge_df.validate()

        return {
            "success": results["success"],
            "statistics": results["statistics"],
            "results": results["results"]
        }

# Usage
validator = DataValidator()

# Define expectations
expectations = {
    "columns": {
        "text": {"not_null": True},
        "label": {"in_set": [0, 1, 2]}
    },
    "row_count": (100, 10000)
}

# Validate
results = validator.validate_dataset("data.csv", expectations)

if not results["success"]:
    print("Data validation failed!")
    for result in results["results"]:
        if not result["success"]:
            print(f"Failed: {result['expectation_config']['expectation_type']}")
```

### Step 4: Feature Engineering Patterns

Implement feature engineering pipelines:

```python
from sklearn.preprocessing import StandardScaler, LabelEncoder, OneHotEncoder
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.decomposition import PCA
import numpy as np

class FeatureEngineer:
    """Feature engineering for ML datasets."""

    def __init__(self):
        self.scalers = {}
        self.encoders = {}
        self.vectorizers = {}

    def normalize_numerical(self, data: np.ndarray, feature_name: str = "default") -> np.ndarray:
        """Normalize numerical features."""
        if feature_name not in self.scalers:
            self.scalers[feature_name] = StandardScaler()
            return self.scalers[feature_name].fit_transform(data)
        else:
            return self.scalers[feature_name].transform(data)

    def encode_categorical(
        self,
        data: np.ndarray,
        feature_name: str = "default",
        encoding_type: str = "label"
    ) -> np.ndarray:
        """Encode categorical features."""
        if encoding_type == "label":
            if feature_name not in self.encoders:
                self.encoders[feature_name] = LabelEncoder()
                return self.encoders[feature_name].fit_transform(data)
            else:
                return self.encoders[feature_name].transform(data)

        elif encoding_type == "onehot":
            if feature_name not in self.encoders:
                self.encoders[feature_name] = OneHotEncoder(sparse=False)
                return self.encoders[feature_name].fit_transform(data.reshape(-1, 1))
            else:
                return self.encoders[feature_name].transform(data.reshape(-1, 1))

    def vectorize_text(
        self,
        texts: List[str],
        feature_name: str = "text",
        method: str = "tfidf",
        max_features: int = 1000
    ) -> np.ndarray:
        """Vectorize text features."""
        if method == "tfidf":
            if feature_name not in self.vectorizers:
                self.vectorizers[feature_name] = TfidfVectorizer(max_features=max_features)
                return self.vectorizers[feature_name].fit_transform(texts).toarray()
            else:
                return self.vectorizers[feature_name].transform(texts).toarray()

        elif method == "count":
            if feature_name not in self.vectorizers:
                self.vectorizers[feature_name] = CountVectorizer(max_features=max_features)
                return self.vectorizers[feature_name].fit_transform(texts).toarray()
            else:
                return self.vectorizers[feature_name].transform(texts).toarray()

    def reduce_dimensionality(
        self,
        features: np.ndarray,
        n_components: int = 50
    ) -> np.ndarray:
        """Reduce dimensionality with PCA."""
        pca = PCA(n_components=n_components)
        return pca.fit_transform(features)

    def create_features(
        self,
        dataset: Dataset,
        feature_config: dict
    ) -> Dataset:
        """Create features based on configuration."""
        features = {}

        for feature_name, config in feature_config.items():
            if config["type"] == "numerical":
                data = np.array(dataset[feature_name])
                features[feature_name] = self.normalize_numerical(data, feature_name)

            elif config["type"] == "categorical":
                data = np.array(dataset[feature_name])
                features[feature_name] = self.encode_categorical(
                    data,
                    feature_name,
                    config.get("encoding", "label")
                )

            elif config["type"] == "text":
                texts = dataset[feature_name]
                features[feature_name] = self.vectorize_text(
                    texts,
                    feature_name,
                    config.get("method", "tfidf"),
                    config.get("max_features", 1000)
                )

        # Combine features
        feature_matrix = np.hstack(list(features.values()))

        # Add to dataset
        return dataset.add_column("features", [feature_matrix[i] for i in range(len(dataset))])

# Usage
engineer = FeatureEngineer()

feature_config = {
    "age": {"type": "numerical"},
    "category": {"type": "categorical", "encoding": "onehot"},
    "text": {"type": "text", "method": "tfidf", "max_features": 500}
}

dataset_with_features = engineer.create_features(dataset, feature_config)
```

### Step 5: Data Versioning with DVC

Version datasets using DVC:

```python
import dvc.api
from pathlib import Path
import yaml

class DataVersionManager:
    """Manage data versions with DVC."""

    def __init__(self, repo_path: str = "."):
        self.repo_path = Path(repo_path)
        self.dvc_path = self.repo_path / "data.dvc"

    def init_dvc(self):
        """Initialize DVC repository."""
        import subprocess
        subprocess.run(["dvc", "init"], cwd=self.repo_path)

    def add_data(
        self,
        data_path: str,
        remote: str = None,
        remote_url: str = None
    ):
        """Add data to DVC tracking."""
        import subprocess

        cmd = ["dvc", "add", data_path]
        subprocess.run(cmd, cwd=self.repo_path)

        if remote:
            # Configure remote
            subprocess.run(
                ["dvc", "remote", "add", "-d", remote, remote_url],
                cwd=self.repo_path
            )

            # Push to remote
            subprocess.run(["dvc", "push"], cwd=self.repo_path)

    def get_data(
        self,
        data_path: str,
        rev: str = None,
        remote: str = None
    ):
        """Get data from DVC."""
        if rev:
            return dvc.api.get_url(
                data_path,
                repo=self.repo_path,
                rev=rev,
                remote=remote
            )
        else:
            return dvc.api.get_url(
                data_path,
                repo=self.repo_path,
                remote=remote
            )

    def list_versions(self, data_path: str) -> list:
        """List available versions."""
        import subprocess
        result = subprocess.run(
            ["dvc", "list", data_path, "--all-commits"],
            cwd=self.repo_path,
            capture_output=True,
            text=True
        )
        return result.stdout.split("\n")

    def tag_version(self, tag_name: str, data_path: str):
        """Tag a data version."""
        import subprocess
        subprocess.run(
            ["git", "tag", tag_name],
            cwd=self.repo_path
        )

# Usage
version_manager = DataVersionManager()

# Add data
version_manager.add_data(
    data_path="data/train",
    remote="s3",
    remote_url="s3://my-bucket/data"
)

# Get specific version
data_url = version_manager.get_data("data/train", rev="v1.0")
```

### Step 6: Preprocessing Pipeline

Create complete preprocessing pipeline:

```python
from typing import Callable, List
from datasets import Dataset

class PreprocessingPipeline:
    """Complete preprocessing pipeline."""

    def __init__(self):
        self.steps: List[Callable] = []

    def add_step(self, func: Callable, name: str = None):
        """Add preprocessing step."""
        self.steps.append({
            "name": name or func.__name__,
            "func": func
        })

    def apply(self, dataset: Dataset) -> Dataset:
        """Apply all preprocessing steps."""
        result = dataset

        for step in self.steps:
            print(f"Applying step: {step['name']}")
            result = step["func"](result)

        return result

    def clean_text(self, dataset: Dataset, text_column: str = "text") -> Dataset:
        """Clean text data."""
        def clean_function(examples):
            import re
            texts = examples[text_column]
            cleaned = [
                re.sub(r'\s+', ' ', text.strip().lower())
                for text in texts
            ]
            examples[text_column] = cleaned
            return examples

        return dataset.map(clean_function, batched=True)

    def remove_duplicates(self, dataset: Dataset) -> Dataset:
        """Remove duplicate examples."""
        return dataset.filter(lambda x, idx: idx not in dataset.duplicates(), with_indices=True)

    def filter_by_length(
        self,
        dataset: Dataset,
        text_column: str = "text",
        min_length: int = 10,
        max_length: int = 1000
    ) -> Dataset:
        """Filter examples by text length."""
        def length_filter(example):
            length = len(example[text_column].split())
            return min_length <= length <= max_length

        return dataset.filter(length_filter)

# Usage
pipeline = PreprocessingPipeline()

# Add steps
pipeline.add_step(
    lambda ds: pipeline.clean_text(ds, "text"),
    "clean_text"
)
pipeline.add_step(
    lambda ds: pipeline.remove_duplicates(ds),
    "remove_duplicates"
)
pipeline.add_step(
    lambda ds: pipeline.filter_by_length(ds, "text", min_length=10, max_length=500),
    "filter_length"
)

# Apply pipeline
processed_dataset = pipeline.apply(dataset)
```

## Output

After data pipeline processing, you'll have:

1. **Prepared Datasets** - Train/validation/test splits
2. **Validated Data** - Quality-checked datasets
3. **Engineered Features** - Processed feature sets
4. **Versioned Data** - Tracked data versions
5. **Preprocessing Pipeline** - Reusable transformation pipeline
6. **Documentation** - Data schema and processing logs

## Best Practices

- Always validate data before training
- Use DVC for data versioning
- Create reusable preprocessing pipelines
- Document feature engineering decisions
- Split data properly (train/val/test)
- Handle missing values consistently
- Normalize features appropriately
- Version control data processing code

## Anti-Patterns

| Anti-Pattern | Fix |
|--------------|-----|
| No validation | Always validate data quality |
| No versioning | Use DVC for data versioning |
| Data leakage | Proper train/test splitting |
| Inconsistent preprocessing | Use pipelines |
| No documentation | Document data schema |
| Hardcoded paths | Use configuration files |

## Related

- Knowledge: `{directories.knowledge}/data-engineering-ml.json`
- Skill: `training-models`
- Skill: `model-fine-tuning`

## When to Use
This skill should be used when strict adherence to the defined process is required.

## Prerequisites
- Basic understanding of the agent factory context.
- Access to the necessary tools and resources.
