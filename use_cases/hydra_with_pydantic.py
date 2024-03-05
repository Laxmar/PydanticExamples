import logging
from datetime import datetime
from pathlib import Path
from typing import Annotated

import hydra
from omegaconf import DictConfig
from pydantic import BaseModel, Field, PositiveInt, ValidationError, ValidationInfo, computed_field, field_validator

from utils.file_utils import get_git_revision_hash

log = logging.getLogger(__name__)


class TrainingConfiguration(BaseModel):
	batch_size: Annotated[int, Field(gt=0, lt=512)]  # gt=0 is the same as PositiveInt
	epochs: Annotated[PositiveInt, Field(lt=200)]
	learning_rate: Annotated[float, Field(gt=0.0, lt=1.0)]
	training_dataset: Path
	validation_dataset: Path
	output_dir: Path
	training_name: str
	timestamp: datetime = datetime.now()
	git_revision_hash: str = get_git_revision_hash()

	@computed_field
	def training_unique_name(self) -> str:
		return self.output_dir.stem

	@field_validator("training_dataset", "validation_dataset")
	@classmethod
	def validate_path(cls, value: Path, info: ValidationInfo) -> Path:
		if not value.exists():
			raise ValueError(f"Path {value} does not exist")
		if not value.is_file() or value.suffix != ".csv":
			raise ValueError(f"Path {value} does not have a .csv extension")
		return value

	@field_validator("output_dir")
	@classmethod
	def validate_output_dir(cls, value: Path, info: ValidationInfo) -> Path:
		if not value.exists():
			print(f"Creating output directory {value}")
			value.mkdir(parents=True)
		return value


def run_training(config: TrainingConfiguration):
	log.info(f"Configuration: \n{config.model_dump_json(indent=4)}")
	log.info("Running training...")


@hydra.main(version_base=None, config_path="configs", config_name="training_default.yaml")
def main(config: DictConfig):
	"""
	Examples How to run:

	python use_cases/hydra_configuration.py
	python use_cases/hydra_configuration.py -cn training_default.yaml
	python use_cases/hydra_configuration.py batch_size=128
	python use_cases/hydra_configuration.py batch_size=10000
	python use_cases/hydra_configuration.py learning_rate=1.5
	python use_cases/hydra_configuration.py training_dataset=datasets/iris.csv
	"""
	try:
		train_config = TrainingConfiguration.model_validate(config)
	except ValidationError as e:
		log.error(f"Invalid configuration: {e}")
		return

	run_training(train_config)


if __name__ == "__main__":
	main()
