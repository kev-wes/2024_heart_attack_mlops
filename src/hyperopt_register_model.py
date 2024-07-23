# Import necessary libraries
import pandas as pd  # For data manipulation and analysis
import numpy as np
import helper as hlp  # Custom module for helper functions

from sklearn.svm import SVC  # For the Support Vector Classifier model
from sklearn.preprocessing import StandardScaler  # For scaling the data
from sklearn.metrics import accuracy_score  # For evaluating the accuracy of the model

import mlflow  # MLflow for experiment tracking and model management
from mlflow.tracking import MlflowClient  # Interface to interact with the MLflow server
from mlflow.entities import ViewType  # To specify the view type for querying runs

from prefect import task, flow  # Prefect for building and orchestrating workflows
from prefect.artifacts import create_markdown_artifact
from datetime import date

from hyperopt import STATUS_OK, Trials, fmin, hp, tpe  # Hyperopt for hyperparameter optimization
from hyperopt.pyll import scope  # Scope for specifying hyperparameter types

import joblib # For saving and loading the scaler
import os


@task
def run_optimization(num_trials: int,
                     X_train: pd.DataFrame,
                     X_test: pd.DataFrame,
                     y_train: pd.DataFrame,
                     y_test: pd.DataFrame,
                     scaler: StandardScaler):
    """
    Perform hyperparameter optimization for Support Vector Classifier using Hyperopt.

    Args:
    - num_trials (int): Number of trials for hyperparameter optimization.
    - X_train, X_test (pd.DataFrame): Training and testing feature datasets.
    - y_train, y_test (pd.DataFrame): Training and testing target datasets.

    Returns:
    - None
    """

    def objective(params):
        """
        Objective function for hyperparameter optimization.

        Args:
        - params (dict): Dictionary of hyperparameters.

        Returns:
        - dict: Dictionary containing 'loss' (negative accuracy) and 'status'.
        """
        with mlflow.start_run():
            model = SVC(**params)  # Initialize SVC with given parameters
            model.fit(X_train, y_train)  # Train the model
            y_pred = model.predict(X_test)  # Predict using test data
            acc = accuracy_score(y_test, y_pred)  # Calculate accuracy
            mlflow.log_params(params)  # Log hyperparameters
            mlflow.log_metric("acc", acc)  # Log accuracy

            # Save the scaler as an artifact
            joblib.dump(scaler, "src/scaler.pkl")
            mlflow.log_artifact("src/scaler.pkl", "scaler")
            # After logging, you can delete the local file
            os.remove("src/scaler.pkl")

            # Since we want to maximize accuracy, we minimize the negative accuracy
            return {'loss': -acc, 'status': STATUS_OK}

    # Define search space for hyperparameters
    search_space = {
        'C': hp.loguniform('C', np.log(1e-3), np.log(1e2)),  # Regularization parameter
        'kernel': hp.choice('kernel', ['linear', 'rbf', 'poly', 'sigmoid']),
        'degree': scope.int(hp.quniform('degree', 2, 5, 1)),  # Only relevant for 'poly' kernel
        'gamma': hp.choice('gamma', ['scale', 'auto']),
        'probability': hp.choice('probability', [True, False]),
        'random_state': 42  # Fixed random state for reproducibility
    }

    rstate = np.random.default_rng(42)  # Random number generator for reproducible results

    # Perform hyperparameter optimization
    fmin(
        fn=objective,
        space=search_space,
        algo=tpe.suggest,
        max_evals=num_trials,
        trials=Trials(),
        rstate=rstate
    )

@task
def register_model():
    """
    Register the best model found during hyperparameter optimization to MLflow.
    """

    client = MlflowClient()  # Create an MLflow client to interact with the tracking server
    experiment = client.get_experiment_by_name("heart-attack-hyperopt")  # Get the experiment by name

    # Retrieve the best run based on highest accuracy
    best_run = client.search_runs(
        experiment_ids=experiment.experiment_id,
        run_view_type=ViewType.ACTIVE_ONLY,
        order_by=["metrics.acc DESC"]  # Sort by accuracy descending
    )[0]

    best_run_id = best_run.info.run_id  # Get the ID of the best run
    model_uri = f"runs:/{best_run_id}/model"  # URI to the best model artifact
    mlflow.register_model(model_uri, "BestSupportVectorClassifier")  # Register the best model
    markdown_report = f"""# Model Registration

    ## Summary
    Registered best model (run_id: {best_run_id}) with a test acc of {best_run.data.metrics['acc']}."""

    create_markdown_artifact(
        key="heart-attack-hyper-opt-report", markdown=markdown_report
    )


@flow
def main_flow():
    """
    Main flow of the program.

    This function sets up the MLflow environment, loads data, preprocesses it,
    performs hyperparameter optimization, and registers the best model.
    """

    # MLflow settings
    mlflow.set_tracking_uri("http://mlflow:5000")  # Set the URI for MLflow tracking server
    mlflow.set_experiment("heart-attack-hyperopt")  # Set the experiment name
    mlflow.sklearn.autolog()  # Enable automatic logging for sklearn models

    # Load and preprocess data using helper functions
    data = hlp.read_data()
    preprocessed_data = hlp.preprocess_data(data)
    X, y = hlp.split_x_y(preprocessed_data)
    X_train, X_test, y_train, y_test = hlp.split_train_test(X, y)
    X_test, _ = hlp.scale_data(X_test, None)  # Scale test data
    X_train, scaler = hlp.scale_data(X_train, None)  # Scale train data
    
    run_optimization(10, X_train, X_test, y_train, y_test, scaler)  # Perform hyperparameter optimization
    register_model()  # Register the best model found


if __name__ == "__main__":
    main_flow()  # Execute the main flow when running the script
