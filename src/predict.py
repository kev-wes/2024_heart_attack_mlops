# Import necessary libraries
import helper as hlp
from sklearn.metrics import accuracy_score  # For evaluating the accuracy of the model
from prefect import flow, task
import mlflow

@task(log_prints=True)
def predict(X_test, y_test):
    model = mlflow.sklearn.load_model(f"models:/BestSupportVectorClassifier/latest")
    y_pred = model.predict(X_test)
    print(f"Predicted results with an accuracy of {accuracy_score(y_test, y_pred)}.")
    
        
@flow
def main_flow():
    mlflow.set_tracking_uri("http://localhost:5000")
    data = hlp.read_data()
    preprocessed_data = hlp.preprocess_data(data)
    X, y = hlp.split_x_y(preprocessed_data)
    _, X_test, _, y_test = hlp.split_train_test(X, y)
    X_test = hlp.scale_data(X_test)
    predict(X_test, y_test)
    

if __name__ == "__main__":
    main_flow()