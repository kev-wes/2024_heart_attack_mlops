# Capstone Project for the MLOps Zoomcamp: Predicting Heart Attack Risks

## Legend
- 🚩 = ToDo
- 🟠 = WiP
- ✅ = Implemented fully

## Problem description

🚩 Lorem ipsum

## Instructions for use
1. Pull from GitHub using 'git pull https://github.com/kev-wes/2024_heart_attack_mlops.git'

#### ToDo! Implement these all in docker!!
2. Install pipenv 'pip install pipenv'
3. Install dependencies 'pipenv install'
4. Activate environment 'pipenv shell'
5. Start MLflow server 'mlflow server --backend-store-uri sqlite:///mlflow.db --default-artifact-root ./artifacts'
6. Start prefect server 'prefect server start'
7. Create prefect workpool 'prefect work-pool create --type process zoompool'
8. Deploy training flow 'prefect deploy src/hyperopt_register_model.py:main_flow -n train-heart-attack-model -p zoompool'
9. Start worker 'prefect worker start --pool 'zoompool''
10. Hyperparam tune, train, and register model 'prefect deployment run 'main-flow/train-heart-attack-model''
11. Start prediction web service 'gunicorn -w 4 -b 0.0.0.0:8000 src.app:app'
12. Open 'http://localhost:8000/' in your browser. Now you can input your health data an it returns the probability 

#### For monitoring (only Gmail for sending supported!)
1. Register app password under https://myaccount.google.com/apppasswords
2. Create new prefect block with your email address and app password 'python src/create_email_block.py --sender your_email@gmail.com --sender_password your_gmail_app_password'
3. Deploy monitoring flow 'prefect deploy src/monitor.py:main_flow -n monitor-heart-attack-data-drift -p zoompool'
4. Create a schedule or monitor dataset ad hoc 'prefect deployment run 'main-flow/monitor-heart-attack-data-drift' -p recipient='recipient@any-provider.com'' 

#### For testing
1. Unit test: 'pytest tests/unit_test.py'
2. Integration test: 

## Project structure explained

### Data
- ✅ data/: Contains all data.
  - ✅ heart.csv: The training and test data for heart attack prediction.

### Environment
- ✅ .gitignore: Contains all files and directories that should be ignored for GitHub commits.
- ✅ Pipfile: Contains the dependencies.
- ✅ Pipfile.lock: Contains the exact versions of all dependencies and their dependencies.
- ✅ prefect.yaml: Contains the .yaml file that stores this .git location to pull.

- 🚩 Dockerfile: #Dockerfile for predict.py (cf. HW4)

### MLflow
- ✅ artifacts: Contains artifacts from MLflow. Ignored by .gitignore, built during runtime!
- ✅ mlflow.db: Contains the local mlflow database. Ignored by .gitignore, built during runtime!

### Scripts
- ✅ src/
  - ✅ hyperopt_register_model.py: This script performs automated hyperparameter optimization for a Support Vector Classifier (SVC) using Hyperopt. It utilizes MLflow for experiment tracking and model management, logging metrics and registering the best model found. The workflow, orchestrated with Prefect, includes data loading, preprocessing, scaling, and evaluating SVC models on a heart attack prediction dataset.
  - ✅ helper.py: The code defines a data preprocessing pipeline for a machine learning project using Prefect for workflow management. It includes tasks for reading a dataset, removing duplicates, splitting features and targets, splitting data into training and testing sets, and scaling features using standardization. 
  - ✅ app.py: Hosts a Flask prediction web service over http://localhost:8000/. Takes the best model registered before and uses it for prediction.
  - ✅ templates/: Stores the template used by the Flask app.
    - ✅ index.html: Simple web form for heart attack risk prediction.
  - ✅ monitor.py: Calculates metrics between current data (data/heart.csv) and reference data set (data/reference.csv) and sends out email.
  - ✅ create_email_block.py: Python helper to create a prefect email block to send monitoring alerts.

### Tests
- 🟠 tests/: Contains a unit and an integration test.
  - ✅ __init__.py: init file for testing.
  - ✅ unit_test.py: Unit tests for data preprocessing. Tests the function 'preprocess_data' that is stored in src/helper.py and is used for training (hyperopt_register_model.py) and prediction (app.py).
  - 🚩 integration-test.py: Integration test (cf. HW 6.4-6.6 / video 6.2 & 6.3)
  - ✅ run.sh

## Evaluation criteria
* Problem description
    * [ ] 0 points: The problem is not described
    * [ ] 1 point: The problem is described but shortly or not clearly 
    * [x] 2 points: The problem is well described and it's clear what the problem the project solves
      * 🚩 Describe problem well
* Cloud
    * [x] 0 points: Cloud is not used, things run only locally
      * ✅ Everything is hosted locally on an ubuntu server. It can be hosted anywhere on premise and can be accessed outside through the hosted web services, but it does not use cloud or IaC tools.
    * [ ] 2 points: The project is developed on the cloud OR uses localstack (or similar tool) OR the project is deployed to Kubernetes or similar container management platforms
    * [ ] 4 points: The project is developed on the cloud and IaC tools are used for provisioning the infrastructure
* Experiment tracking and model registry
    * [ ] 0 points: No experiment tracking or model registry
    * [ ] 2 points: Experiments are tracked or models are registered in the registry
    * [x] 4 points: Both experiment tracking and model registry are used 
      * ✅ I do hyperparameter tuning in 'src/hyperopt_register_model.py' where I track experiments and promote the best model to the model registry. I then load the model from model registry in 'predict.py'. 
* Workflow orchestration
    * [ ] 0 points: No workflow orchestration
    * [ ] 2 points: Basic workflow orchestration
    * [x] 4 points: Fully deployed workflow  
      * ✅ I used prefect for workflow orchestration (cf. course material from 2023). Unfortunately, Mage did not work for me. I added @task and @flow decorators to my code. I also created a prefect deployment for hyperparameter optimization, model registration, and monitoring. Additionally I created a workpool with one worker that automatically starts a hyperparameter optimization and model registration run. Each run, returns a markdown report as artifact.
* Model deployment
    * [ ] 0 points: Model is not deployed
    * [ ] 2 points: Model is deployed but only locally
    * [x] 4 points: The model deployment code is containerized and could be deployed to cloud or special tools for model deployment are used 
      * 🟠 I hosted the model as a webservice that is reachable under 'localhost:8000'. ToDo: containerize model using Docker like HW4.
* Model monitoring
    * [ ] 0 points: No model monitoring
    * [ ] 2 points: Basic model monitoring that calculates and reports metrics
    * [x] 4 points: Comprehensive model monitoring that sends alerts or runs a conditional workflow (e.g. retraining, generating debugging dashboard, switching to a different model) if the defined metrics threshold is violated 
      * ✅ I calculate dataset drift metrics between current data (data/heart.csv) and reference data set (data/reference.csv) and send out an email alert.
* Reproducibility
    * [ ] 0 points: No instructions on how to run the code at all, the data is missing
    * [ ] 2 points: Some instructions are there, but they are not complete OR instructions are clear and complete, the code works, but the data is missing
    * [x] 4 points: Instructions are clear, it's easy to run the code, and it works. The versions for all the dependencies are specified. 
      * 🟠 I used pipenv so that all versions for all dependencies are specified. Additionally I provide instructions to run the code above. ToDo: Bundle everything in Docker to make startup easy.
* Best practices
    * [x] There are unit tests (1 point) 
      * 🚩 cf. HW6.1 to 6.3 and video 6.1. Create unit tests for data preparation script.
    * [x] There is an integration test (1 point) 
      * 🚩 cf. HW6.4 to 6.6 and video 6.2-6.3. Create integration test for application.
    * [x] Linter and/or code formatter are used (1 point) 
      * 🚩 cf. video 6.4. ???
    * [x] There's a Makefile (1 point) 
      * 🚩 cf. video 6.5. ???
    * [x] There are pre-commit hooks (1 point) 
      * 🚩 cf. video 6.6. ???
    * [x] There's a CI/CD pipeline (2 points) 
      * 🚩 cf. video 6B.5-6B.7. ???
