import pandas as pd

from prefect_email import EmailServerCredentials
from prefect_email import email_send_message
from prefect import flow, task

from evidently import ColumnMapping
from evidently.report import Report
from evidently.metrics import DatasetDriftMetric

@task
def evidently_report():
    current_data = pd.read_csv('./data/heart.csv')
    reference_data = pd.read_csv('./data/reference.csv')
    num_features = ["age", "trtbps", "chol", "thalachh", "oldpeak"]
    cat_features = ["sex", "cp", "fbs", "restecg", "exng", "slp", "caa", "thall", "output"]
    column_mapping = ColumnMapping(
        target= 'output',
        prediction=None,
        numerical_features=num_features,
        categorical_features=cat_features
    )
    report = Report(metrics=[DatasetDriftMetric()])
    report.run(reference_data=reference_data, current_data=current_data, column_mapping=column_mapping)
    result = report.as_dict()
    share_of_drifted_columns = result['metrics'][0]['result']['share_of_drifted_columns']
    return share_of_drifted_columns

@task
def send_notification(subject, msg, email_to, email_from):
    # Load the credentials block
    email_credentials_block = EmailServerCredentials.load("gmail")
    
    email_send_message(
        email_server_credentials=email_credentials_block,
        subject=subject,
        msg=msg,
        email_to=email_to,
        email_from=email_from
    )


@flow
def main_flow(recipient: str):
    share_of_drifted_columns = evidently_report()
    if share_of_drifted_columns > 0: 
        send_notification("Data drift detected!", f"We have identified a data drift between heart.csv and reference.csv with a 'share_of_drifted_columns' of, {share_of_drifted_columns:.5f}",
                          recipient, "noreply@mlops.com")
    else: 
        send_notification("No data drift detected!", f"We have identified no data drift between heart.csv and reference.csv",
                          recipient, "noreply@mlops.com")

if __name__ == "__main__":
    main_flow()  # Execute the main flow when running the script