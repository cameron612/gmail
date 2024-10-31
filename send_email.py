import ezgmail

def send_email(recipient, subject, body, attachments=None):
    """
    Send an email using Gmail API
    
    Args:
        recipient (str): Email address of the recipient
        subject (str): Subject of the email
        body (str): Body content of the email
        attachments (list, optional): List of file paths to attach to the email
    """
    try:
        if attachments:
            ezgmail.send(recipient, subject, body, attachments)
        else:
            ezgmail.send(recipient, subject, body)
        print(f"Email sent successfully to {recipient}")
    except Exception as e:
        print(f"Failed to send email: {str(e)}")

if __name__ == "__main__":
    # Example usage
    recipient = "example@example.com"
    subject = "Test Email"
    body = "This is a test email sent using ezgmail."
    
    # Send a simple email
    send_email(recipient, subject, body)
    
    # Example with attachment
    # send_email(recipient, subject, body, ["document.pdf"])