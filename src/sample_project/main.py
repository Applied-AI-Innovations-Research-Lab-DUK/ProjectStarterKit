import logging
from src.sample_project.pipelines.train_pipeline import run_training_pipeline
from src.sample_project.utils.logging import setup_logging

def main():
    setup_logging()
    logging.info("Starting the training pipeline.")
    run_training_pipeline()

if __name__ == "__main__":
    main()
