import sys
sys.path.insert(0, 'package/')
import json
from twilio.rest import Client
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from config import \
    TWILIO_ACCOUNT_SID, \
    TWILIO_AUTH_TOKEN, \
    TWILIO_PHONE_NUMBER, \
    SENDGRID_API_KEY
import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def send_sms(phone_number, body_message, client):
    """Send sms
    Args:
        phone_number (string): the phone number that will receive the sms
        body_message (string): the message
        client(object)
    """
    try:
        message = client.messages.create(
            body=body_message,
            from_=TWILIO_PHONE_NUMBER,
            to=phone_number
        )
        logging.info("send_sms: Message sent to number: %s."
                     "Message Sid: %s" % (phone_number, message.sid))
    except Exception as err:
        logging.error("send_sms: Message not sent to %s"
                      % (phone_number))
        raise Exception(err)


def send_email(content, to_):
    """Send email

    Args:
        subject(str): subject of email
        content(str): content of email
        to_(str): email to receive
    """
    subject = '{YOUR_CUSTOM_SUBJECT}'
    message = Mail(
        from_email='{YOUR_EMAIL}@{YOUR_EMAIL_SERVICE}',
        to_emails=to_,
        subject=subject,
        plain_text_content=content)
    try:
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        sg.send(message)
        logger.info("send_email: Message sent to email: %s" % (to_))
    except Exception as e:
        logging.error("send_email: Message not sent to %s"
                      % (to_))
        logging.error(e.body)
        raise Exception(e)


def handler(event, context):
    account_sid = TWILIO_ACCOUNT_SID
    auth_token = TWILIO_AUTH_TOKEN
    client = Client(account_sid, auth_token)
    for message in event['data']:
        body_message = message['message']
        try:
            phone_number = message['phone_number']
            send_sms(phone_number, body_message, client)
        except KeyError:
            email = message['email']
            send_email(body_message, email)
