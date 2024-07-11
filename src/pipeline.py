# Import necessary libraries
import pandas as pd  # For data manipulation and analysis
from sklearn.model_selection import train_test_split  # For splitting the data into training and testing sets
from sklearn.preprocessing import StandardScaler  # For feature scaling
from sklearn.svm import SVC  # For the Support Vector Classifier model
from sklearn.metrics import accuracy_score  # For evaluating the accuracy of the model
from prefect import flow, task
from prefect.artifacts import create_markdown_artifact
import mlflow
from datetime import date


@task
def read_data() -> pd.DataFrame:
    # Load the dataset from a CSV file
    data = pd.read_csv('./data/heart.csv')
    return data

@task
def preprocess_data(data):
    # Remove duplicate rows from the dataset
    data.drop_duplicates(keep='first', inplace=True)
    return data

def split_train_test(data):

    # Separate the features (x) and the target variable (y)
    x = data.iloc[:, 1:-1].values
    y = data.iloc[:, -1].values

    # Split the data into training and testing sets (80% training, 20% testing)
    X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=0)
    return X_train, X_test, y_train, y_test

def scale_data(data):
    # Initialize the StandardScaler
    scaler = StandardScaler()
    # Fit the scaler on the training data and transform the training data
    scaled_data = scaler.fit_transform(data)
    return scaled_data


@task(log_prints=True)
def train_predict_model(X_train, X_test, y_train, y_test):
    mlflow.sklearn.autolog()
    with mlflow.start_run():
        # Define a dictionary with the desired parameters
        params = {
            'C': 1.0,           # Regularization parameter
            'kernel': 'rbf',    # Kernel type
            'degree': 3,        # Degree for 'poly' kernel
            'gamma': 'scale',   # Kernel coefficient
            'probability': False,  # Whether to enable probability estimates
        }
        # Initialize the Support Vector Classifier model
        model = SVC(**params)
        # Train the model using the training data
        model.fit(X_train, y_train)
        # Predict the target variable for the testing data
        predicted = model.predict(X_test)
        acc = accuracy_score(y_test, predicted)
        mlflow.sklearn.log_model(model, artifact_path="models_mlflow")
        markdown_rmse_report = f"""# Accuracy Report

        ## Summary

        Heart Attack Prediction 

        ## Accuracy SVC Model

        | Region    | Accuracy |
        |:----------|-------:|
        | {date.today()} | {acc:.2f} |
        """

        create_markdown_artifact(
            key="duration-model-report", markdown=markdown_rmse_report
        )

@flow
def main_flow():
    # MLflow settings
    mlflow.set_tracking_uri("http://localhost:5000")
    mlflow.set_experiment("heart-attack-experiment")

    data = read_data()
    preprocessed_data = preprocess_data(data)
    X_train, X_test, y_train, y_test = split_train_test(preprocessed_data)
    X_train = scale_data(X_train)
    X_test = scale_data(X_test)
    train_predict_model(X_train, X_test, y_train, y_test)

if __name__ == "__main__":
    main_flow()