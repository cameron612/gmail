from flask import Flask, render_template, request, flash, redirect, url_for, session
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
import base64
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

# OAuth 2.0 configuration
CLIENT_SECRETS_FILE = "credentials.json"
SCOPES = ['https://www.googleapis.com/auth/gmail.send']

@app.route('/')
def index():
    if 'credentials' not in session:
        return redirect(url_for('authorize'))
    return render_template('index.html')

@app.route('/authorize')
def authorize():
    flow = Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE,
        scopes=SCOPES,
        redirect_uri=url_for('oauth2callback', _external=True)
    )
    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true'
    )
    session['state'] = state
    return redirect(authorization_url)

@app.route('/oauth2callback')
def oauth2callback():
    state = session['state']
    flow = Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE,
        scopes=SCOPES,
        state=state,
        redirect_uri=url_for('oauth2callback', _external=True)
    )
    authorization_response = request.url
    flow.fetch_token(authorization_response=authorization_response)
    credentials = flow.credentials
    session['credentials'] = {
        'token': credentials.token,
        'refresh_token': credentials.refresh_token,
        'token_uri': credentials.token_uri,
        'client_id': credentials.client_id,
        'client_secret': credentials.client_secret,
        'scopes': credentials.scopes
    }
    return redirect(url_for('index'))

def create_message_with_attachment(sender, to, subject, message_text, files=None):
    message = MIMEMultipart()
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject

    msg = MIMEText(message_text)
    message.attach(msg)

    if files:
        for file in files:
            content_type = file.content_type
            filename = file.filename
            
            # Read and attach the file
            part = MIMEBase(*content_type.split('/'))
            part.set_payload(file.read())
            encoders.encode_base64(part)
            part.add_header(
                'Content-Disposition',
                'attachment',
                filename=filename
            )
            message.attach(part)

    return {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode()}

@app.route('/send', methods=['POST'])
def send_email():
    if 'credentials' not in session:
        return redirect(url_for('authorize'))

    credentials = Credentials(**session['credentials'])
    service = build('gmail', 'v1', credentials=credentials)

    recipient = request.form.get('recipient')
    subject = request.form.get('subject')
    body = request.form.get('body')
    files = request.files.getlist('attachments')

    try:
        # Get user's email address
        profile = service.users().getProfile(userId='me').execute()
        sender = profile['emailAddress']

        # Create the email
        if files and files[0].filename:
            message = create_message_with_attachment(sender, recipient, subject, body, files)
        else:
            message = create_message_with_attachment(sender, recipient, subject, body)

        # Send the email
        service.users().messages().send(userId='me', body=message).execute()
        flash('Email sent successfully!', 'success')
    except Exception as e:
        flash(f'Error sending email: {str(e)}', 'error')

    return redirect(url_for('index'))

if __name__ == '__main__':
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'  # Only for development
    app.run(port=3000, debug=True)