import pipeline as pl
import mlflow
from prefect import task, flow

@flow
def main_flow():
    # MLflow settings
    mlflow.set_tracking_uri("http://localhost:5000")
    mlflow.set_experiment("heart-attack-experiment")

    data = pl.read_data()
    preprocessed_data = pl.preprocess_data(data)
    scaled_data = pl.scale_data(preprocessed_data) # Can I use scaling in HPO experiment? Now danger of Data Leakage
    # TODO HPO + Registration of best model!

if __name__ == "__main__":
    main_flow()