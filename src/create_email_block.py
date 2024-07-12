import argparse
from prefect_email import EmailServerCredentials

def create_email_block(sender, sender_password):
    # Define email server credentials
    email_credentials = EmailServerCredentials(
        username=sender,
        password=sender_password,
        smtp_server="smtp.gmail.com",
        smtp_port=465,
        smtp_type="SSL"
    )

    # Save the credentials as a block in Prefect
    email_credentials.save(name="gmail")

    print("Email server credentials block created successfully.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create a Prefect email server credentials block.")
    parser.add_argument("--sender", required=True, help="Gmail account from which alerts should be sent.")
    parser.add_argument("--sender_password", required=True, help="Gmail app password.")

    args = parser.parse_args()
    create_email_block(args.sender, args.sender_password)
