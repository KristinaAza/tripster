import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from twilio.rest import Client

def send_email(to_email, subject, html_content):
    message = Mail(
        from_email=os.environ.get('FROM_EMAIL'),
        to_emails=to_email,
        subject=subject,
        html_content=html_content)
    try:
        sg = SendGridAPIClient(os.environ['SENDGRID_API_KEY'])
        response = sg.send(message)
        print(response.status_code)
    except Exception as e:
        print(e.message)

def send_sms(to_phone_number, body):
    account_sid = os.environ['TWILIO_ACCOUNT_SID']
    auth_token = os.environ['TWILIO_AUTH_TOKEN']
    client = Client(account_sid, auth_token)

    message = client.messages.create(
                        body=body,
                        from_=os.environ['FROM_PHONE_NUMBER'],
                        to=to_phone_number
                    )
    print("sms sent")
    print(message.sid)
