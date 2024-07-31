# Capstone Project for the MLOps Zoomcamp: Predicting Heart Attack Risks

## Problem statement

Cardiovascular diseases, including heart attacks, are the leading cause of death globally, claiming millions of lives each year. Early detection and prevention are critical to reducing the mortality rate associated with heart diseases. Despite advancements in medical technology, there remains a significant need for accessible and accurate tools that can predict the risk of heart attacks, enabling timely intervention and potentially saving lives.

To address this pressing issue, I developed a comprehensive heart attack risk prediction service as part of my capstone project for the DataTalksClub MLOps course ('https://github.com/DataTalksClub/mlops-zoomcamp'). This project utilizes a dataset of heart attack risk factors to build and deploy a machine learning model capable of predicting an individual's risk of experiencing a heart attack. The service is designed to be user-friendly and accessible, requiring only 13 input measurements to generate a prediction.

The project leverages state-of-the-art MLOps techniques to ensure robustness, scalability, and maintainability. Key features include:

- __Experiment Tracking and Model Registry__: Hyperparameter tuning and model training are tracked using MLflow, with the best model automatically registered for deployment.
- __Workflow Orchestration__: Prefect is used to orchestrate workflows, including model training, deployment, and monitoring.
- __Model Deployment__: The trained model is deployed as a web service using Flask, allowing users to access the prediction service via a web browser.
- __Model Monitoring__: The service includes comprehensive monitoring to detect data drift and ensure model performance, with alerts sent via email if anomalies are detected.
- __Reproducibility and Best Practices__: The project follows best practices in software development, including the use of Docker for containerization, pipenv for dependency management, and unit tests to ensure code quality.

This repository showcases the application of MLOps principles to a real-world problem, providing a valuable tool for predicting heart attack risk and demonstrating the effectiveness of modern machine learning operations.

## Instructions for use

### A. Installation
1. Install Git and docker-compose (or docker compose) 
2. Pull from GitHub using `git clone https://github.com/kev-wes/2024_heart_attack_mlops.git`
3. Move to repo `cd 2024_heart_attack_mlops`
4. `docker-compose build` (or 'docker compose build') 
5. `docker-compose up` (or 'docker compose up') 

### B. Training a Model
1. Train a model by opening prefect over `http://localhost:4200/`.
2. Go to `Deployments`
3. For the deployment `train-heart-attack-model` start `Quick run`. Now a hyperparameter tuning is performed and the best model is registered via MLflow.

### C. Heart Attack Risk Prediction
1. __Important: You have to train a model first!__ Open `http://localhost:8000/` in your browser. Now you can input your health data an it returns the probability of increased heart attack risk using your best trained model.

### D. Monitoring Data Drift (only Gmail for sending supported!)
1. Register app password under https://myaccount.google.com/apppasswords
2. Create new prefect block with your email address and app password (You can also refer to `python src/create_email_block.py --sender your_email@gmail.com --sender_password your_gmail_app_password` for a programmatic solution)
   - Open prefect over `http://localhost:4200/`
   - Click on `Block`
   - Add block via `Add Block+`
   - Choose type `Email Server Credentials`
   - Set `Block Name` to `gmail`
   - Input your gmail username via `Username` and your app password set register in step 1 via `Password`
   - Set `SMPTServer` to `smtp.gmail.com`, `SMTP Type` to `SSL`, and `SMTP Port` to `465`
3. Monitor dataset ad hoc (you can also create a schedule) by going to `Deyploments` again. Start a custom run of deployment `monitor-heart-attack-data-drift`. Set `recipient` to an email address you want to send the data drift alert to. 

## Repository Contents

### Data
- __data/__: Contains all data.
  - __heart.csv__: The training and test data for heart attack prediction.
  - __reference.csv__: This is the reference dataset that is saved for monitoring. This can be exchanged with any dataset to measure data drift using 'src/monitor.py'. In the current case, the data set is a subset of heart.csv, where I deleted observations in such a way that a data drift is simulated.

### Scripts
- __src/__
  - __hyperopt_register_model.py__: This script performs automated hyperparameter optimization for a Support Vector Classifier (SVC) using Hyperopt. It utilizes MLflow for experiment tracking and model management, logging metrics and registering the best model found. The workflow, orchestrated with Prefect, includes data loading, preprocessing, scaling, and evaluating SVC models on a heart attack prediction dataset.
  - __helper.py__: The code defines a data preprocessing pipeline for a machine learning project using Prefect for workflow management. It includes tasks for reading a dataset, removing duplicates, splitting features and targets, splitting data into training and testing sets, and scaling features using standardization. 
  - __app.py__: Hosts a Flask prediction web service over http://localhost:8000/. Takes the best model registered before and uses it for prediction.
  - __templates/__: Stores the template used by the Flask app.
    - __index.html__: Simple web form for heart attack risk prediction.
  - __monitor.py__: Calculates metrics between current data (data/heart.csv) and reference data set (data/reference.csv) and sends out email.
  - __create_email_block.py__: Python helper to create a prefect email block to send monitoring alerts.

### Tests
- __tests/__: Contains a unit and an integration test.
  - __\_\_init\_\_.py__: init file for testing.
  - __unit_test.py__: Unit tests for data preprocessing. Tests the function 'preprocess_data' that is stored in src/helper.py and is used for training (hyperopt_register_model.py) and prediction (app.py).

### Environment
- __.gitignore__: Contains all files and directories that should be ignored for GitHub commits.
- __docker-compose.yaml__: This Docker Compose configuration defines three services (mlflow, prefect, and app) each built from their respective Dockerfiles and joined to a common network. The mlflow service exposes port 5000 and the prefect service exposes port 4200, while the app service exposes port 8000. All three services share a volume named mlflow-data mounted at /app/artifacts to facilitate data sharing between them. The PREFECT_API_URL environment variable is set for the prefect service to point to its API endpoint. The mlflow-data volume is defined to persist data, and a network is created to allow inter-service communication.
- __Dockerfile.app__: This Dockerfile uses pipenv to manage dependencies. It designates /app as the working directory, copies Pipfile and Pipfile.lock to install the necessary packages, and then copies the entire application code into the container. The Dockerfile exposes port 8000 for the web service and uses pipenv to run gunicorn with four workers to serve the application located at src.app:app on 0.0.0.0:8000.
- __Dockerfile.mlflow__: Containerizes the mlflow server that is accessed by training (to find and register best model) and prediction (to retrieve best model).
- __Dockerfile.prefect__: This Dockerfile sets up a Prefect environment and installs dependencies with pipenv. The Prefect server is exposed on port 4200. Upon starting the container, it runs a script to start the Prefect server, ensures the existence of a work pool, deploys two flows (hyperopt_register_model.py for training a model and monitor.py for monitoring data drift), and finally starts a Prefect worker within the pool.
- __Pipfile__: Contains the dependencies.
- __Pipfile.lock__: Contains the exact versions of all dependencies and their dependencies.
- __prefect.yaml__: Contains the .yaml file that stores this .git location to pull.
- __README.md__: This file.


## Evaluation criteria
* __Problem description__
    * [ ] 0 points: The problem is not described
    * [ ] 1 point: The problem is described but shortly or not clearly 
    * [x] 2 points: The problem is well described and it's clear what the problem the project solves
      * I provided an in-depth problem statement, instructions for use, and explained the repository structure.
* __Cloud__
    * [x] 0 points: Cloud is not used, things run only locally
      * Everything is hosted locally on an ubuntu server. It can be hosted anywhere on premise and can be accessed outside through the hosted web services, but it does not use cloud or IaC tools.
    * [ ] 2 points: The project is developed on the cloud OR uses localstack (or similar tool) OR the project is deployed to Kubernetes or similar container management platforms
    * [ ] 4 points: The project is developed on the cloud and IaC tools are used for provisioning the infrastructure
* __Experiment tracking and model registry__
    * [ ] 0 points: No experiment tracking or model registry
    * [ ] 2 points: Experiments are tracked or models are registered in the registry
    * [x] 4 points: Both experiment tracking and model registry are used 
      * I do hyperparameter tuning in 'src/hyperopt_register_model.py' where I track experiments and promote the best model to the model registry. I then load the model from model registry in 'predict.py'. 
* __Workflow orchestration__
    * [ ] 0 points: No workflow orchestration
    * [ ] 2 points: Basic workflow orchestration
    * [x] 4 points: Fully deployed workflow  
      * I used prefect for workflow orchestration (cf. course material from 2023). Unfortunately, Mage did not work for me. I added @task and @flow decorators to my code. I also created a prefect deployment for hyperparameter optimization, model registration, and monitoring. Additionally I created a workpool with one worker that automatically starts a hyperparameter optimization and model registration run. Each run, returns a markdown report as artifact.
* __Model deployment__
    * [ ] 0 points: Model is not deployed
    * [ ] 2 points: Model is deployed but only locally
    * [x] 4 points: The model deployment code is containerized and could be deployed to cloud or special tools for model deployment are used 
      * I hosted the model as a webservice that is reachable under 'localhost:8000'. Additionally, I fully containerized the code using docker-compose.
* __Model monitoring__
    * [ ] 0 points: No model monitoring
    * [ ] 2 points: Basic model monitoring that calculates and reports metrics
    * [x] 4 points: Comprehensive model monitoring that sends alerts or runs a conditional workflow (e.g. retraining, generating debugging dashboard, switching to a different model) if the defined metrics threshold is violated 
      * I calculate dataset drift metrics between current data (data/heart.csv) and reference data set (data/reference.csv) and send out an email alert.
* __Reproducibility__
    * [ ] 0 points: No instructions on how to run the code at all, the data is missing
    * [ ] 2 points: Some instructions are there, but they are not complete OR instructions are clear and complete, the code works, but the data is missing
    * [x] 4 points: Instructions are clear, it's easy to run the code, and it works. The versions for all the dependencies are specified. 
      * I used pipenv so that all versions for all dependencies are specified. Additionally I provide instructions to run the code above and bundled everything using docker-compose to make startup easy.
* __Best practices__
    * [x] There are unit tests (1 point) 
      * I created a unit test for data preprocessing. 'tests/unit_test' tests the function 'preprocess_data' that is stored in 'src/helper.py' and is used for training ('hyperopt_register_model.py') and prediction ('app.py').
    * [ ] There is an integration test (1 point) 
      * I do not use integration tests.
    * [ ] Linter and/or code formatter are used (1 point) 
      * I do not use linter or code formatter.
    * [ ] There's a Makefile (1 point) 
      * I do not use a Makefile.
    * [ ] There are pre-commit hooks (1 point) 
      * I do not use pre-commit hooks.
    * [ ] There's a CI/CD pipeline (2 points) 
      * I do not have a CI/CD pipeline.
