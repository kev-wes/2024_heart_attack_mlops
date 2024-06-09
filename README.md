# Capstone Project for the MLOps Zoomcamp

## Project structure
- artifacts        # Contains artifacts from MLflow
- outputs          # Contains model and data .pkl's
- mlflow.db        # Contains the local mlflow database
- pipeline.py      # Contains the Python pipeline data load, preparation, model training/testing
- register.py      # Contains script to register best model after training / Optional Build Docker Container
- predict.XX       # Takes the registered model and uses it for prediction / Alternatively Run Docker Container
- monitor.XX       # Monitoring 
- prefect.yaml     # Contains the .yaml file that stores this .git location to pull 

