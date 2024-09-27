from sample_project.components.data_ingestion import ingest_data
from sample_project.components.data_transformation import transform_data
from sample_project.components.model_trainer import train_model
from sample_project.components.model_evaluation import evaluate_model

def run_training_pipeline():
    ingest_data()
    transform_data()
    train_model()
    evaluate_model()
