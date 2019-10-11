from flask_mail import Message
from app import app, mail
from flask import render_template

def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    mail.send(msg)

#send_email(subject="test email", sender="colirsweb@gmail.com", recipients="colirsweb@gmail.com", text_body="this is body", html_body="<html> <body> <p>this is html body</p> <body> </html>")

def send_password_reset_email(user):
    token = user.get_reset_password_token()
    send_email('[Microblog] Reset Your Password',
        sender=app.config['ADMINS'][0],
        recipients=[user.email],
        text_body=render_template('email/reset_password.txt', user=user, token=token),
        html_body=render_template('email/reset_password.html', user=user, token=token)
        )

#
