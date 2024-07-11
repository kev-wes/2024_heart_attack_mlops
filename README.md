# Capstone Project for the MLOps Zoomcamp: Predicting Heart Attack Risks
## Problem description

Lorem ipsum

## Instructions to start project
1. Pull from GitHub using 'git pull https://github.com/kev-wes/2024_heart_attack_mlops.git'

#### ToDo! Implement these all in docker!!
2. Install pipenv 'pip install pipenv'
3. Install dependencies 'pipenv install'
4. Activate environment 'pipenv shell'
5. Start MLflow server 'mlflow server --backend-store-uri sqlite:///mlflow.db --default-artifact-root ./artifacts'
6. Start prefect server 'prefect server start'


## Project structure

### Legend
- 🚩 = ToDo
- 🟠 = WIP
- ✅ = Implemented fully

### Data
- ✅ data: Contains all data.
  - ✅ heart.csv: The training and test data for heart attack prediction.

### Environment
- ✅ .gitignore: Contains all files and directories that should be ignored for GitHub commits.
- ✅ Pipfile: Contains the dependencies.
- ✅ Pipfile.lock: Contains the exact versions of all dependencies and their dependencies.

### MLflow
- ✅ artifacts: Contains artifacts from MLflow.
- ✅ mlflow.db: Contains the local mlflow database.

### Scripts
- 🟠 src
  - ✅ hyperopt_register_model.py: This script performs automated hyperparameter optimization for a Support Vector Classifier (SVC) using Hyperopt. It utilizes MLflow for experiment tracking and model management, logging metrics and registering the best model found. The workflow, orchestrated with Prefect, includes data loading, preprocessing, scaling, and evaluating SVC models on a heart attack prediction dataset.
  - ✅ helper.py: The code defines a data preprocessing pipeline for a machine learning project using Prefect for workflow management. It includes tasks for reading a dataset, removing duplicates, splitting features and targets, splitting data into training and testing sets, and scaling features using standardization. 
  - 🟠 predict.py: Takes the best model registered before and uses it for prediction. ToDo: Provide a webservice that allows to input X_values and returns the risk of heart attack (cf. HW4)!
  - 🚩 monitor.py: Calculates metrics between current data and reference data set periodically / Sends out email / Use prefect? (cf. HW5) / cf. evidently_metrics_calculation.py for Prefect implementation with database storage

### Orchestration
- 🚩 prefect.yaml: Contains the .yaml file that stores this .git location to pull (cf. HW3)
- 🚩 deployment.yaml: Contains three deployment for pipeline.py, register.py, and predict.py (cf. HW3)

### Predict
- 🚩 Dockerfile: #Dockerfile for predict.py (cf. HW4)
- 🚩 outputs: Contains predictions as parquet (cf. HW4)
  - 🚩 predictions_<ID>.parquet (cf. HW4)
 
### Tests
- 🚩 unit-tests
  - 🚩 __init__.py: init file
  - 🚩 test_data_preparation.py: Unit tests for data preparation (cf. HW 6.1-6.3)
  - 🚩 integration-test.py: Integration test (cf. HW 6.4-6.6 / video 6.2 & 6.3)

## Evaluation criteria
* Problem description
    * [ ] 0 points: The problem is not described
    * [ ] 1 point: The problem is described but shortly or not clearly 
    * [x] 2 points: The problem is well described and it's clear what the problem the project solves
      * 🚩 Describe problem well
* Cloud
    * [x] 0 points: Cloud is not used, things run only locally
      * 🚩 Host local on ubuntu server
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
      * 🟠 I added @task and @flow decorators. ToDo: Deploy model like HW3 (deploy, email message when training finished.)
* Model deployment
    * [ ] 0 points: Model is not deployed
    * [ ] 2 points: Model is deployed but only locally
    * [x] 4 points: The model deployment code is containerized and could be deployed to cloud or special tools for model deployment are used 
      * 🚩 containerize model like HW4.
* Model monitoring
    * [ ] 0 points: No model monitoring
    * [ ] 2 points: Basic model monitoring that calculates and reports metrics
    * [x] 4 points: Comprehensive model monitoring that sends alerts or runs a conditional workflow (e.g. retraining, generating debugging dashboard, switching to a different model) if the defined metrics threshold is violated 
      * 🚩 Calculate report and send out email (prefect?) / cf. evidently_metrics_calculation.py for Prefect implementation with database storage (cf. HW5)} 
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
