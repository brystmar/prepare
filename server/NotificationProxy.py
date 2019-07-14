from flask import Flask
from twilio.rest import Client

from credentials.Twilio import ACCOUNT_SID, AUTH_TOKEN


def send_sms(number, message):
    account_sid = ACCOUNT_SID
    auth_token = AUTH_TOKEN
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        body = message,
        from_ = "+19166194713",
        to = number
    )
    return message.sid
