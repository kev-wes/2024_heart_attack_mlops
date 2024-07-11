# Import necessary libraries
import pandas as pd  # For data manipulation and analysis
from sklearn.model_selection import train_test_split  # For splitting the data into training and testing sets
from sklearn.preprocessing import StandardScaler  # For feature scaling
from sklearn.metrics import accuracy_score  # For evaluating the accuracy of the model
from prefect import task  # For defining tasks in the workflow

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

@task
def split_x_y(data):
    # Separate the features (X) and the target variable (y)
    X = data.iloc[:, 1:-1].values  # Extract features (columns 1 through second-to-last) as numpy array
    y = data.iloc[:, -1].values  # Extract target variable (last column) as numpy array
    return X, y

@task
def split_train_test(X, y):
    # Split the data into training and testing sets (80% training, 20% testing)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)
    return X_train, X_test, y_train, y_test

@task
def scale_data(data):
    # Initialize the StandardScaler
    scaler = StandardScaler()
    # Fit the scaler on the training data and transform the data
    scaled_data = scaler.fit_transform(data)
    return scaled_data
