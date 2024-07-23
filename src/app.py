from flask import Flask, request, render_template
import mlflow
import pandas as pd
import os, sys
from mlflow.tracking import MlflowClient
import joblib


# Add src directory to sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import helper as hlp

app = Flask(__name__)

mlflow.set_tracking_uri("http://mlflow:5000")
client = MlflowClient()


def preprocess_input(data, scaler):
    """
    This function includes the necessary preprocessing steps
    """
    # Convert input data to DataFrame
    df = pd.DataFrame([data])
    df = hlp.preprocess_data(df)
    df, _ = hlp.scale_data(df, scaler)
    
    return df

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get input values from the form
        input_data = {
            'age': int(request.form['age']),
            'sex': int(request.form['sex']),
            'cp': int(request.form['cp']),
            'trtbps': int(request.form['trtbps']),
            'chol': int(request.form['chol']),
            'fbs': int(request.form['fbs']),
            'restecg': int(request.form['restecg']),
            'thalachh': int(request.form['thalachh']),
            'exng': int(request.form['exng']),
            'oldpeak': float(request.form['oldpeak']),
            'slp': int(request.form['slp']),
            'caa': int(request.form['caa']),
            'thall': int(request.form['thall'])
        }
        
        latest_model_version = client.get_latest_versions("BestSupportVectorClassifier")[0]

        # Load the model
        model = mlflow.sklearn.load_model(f"models:/BestSupportVectorClassifier/{latest_model_version.version}")

        # Load the scaler artifact
        scaler_path = mlflow.artifacts.download_artifacts(f"runs:/{latest_model_version.run_id}/scaler/scaler.pkl")
        scaler = joblib.load(scaler_path)

        # Preprocess input data
        processed_data = preprocess_input(input_data, scaler)
        
        # Predict using the loaded model
        prediction = model.predict(processed_data)
        
        # Return the result to the UI
        return render_template('index.html', prediction=int(prediction[0]))
    
    return render_template('index.html', prediction=None)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)
