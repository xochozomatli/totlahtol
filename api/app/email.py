from threading import Thread
from flask import current_app, render_template 
from flask_mail import Message
from app import mail

def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)

def send_email(subject, sender, recipients, text_body, html_body, attachments=None, sync=False):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    if attachments:
        for attachment in attachments:
            msg.attach(*attachment)
        if sync:
            mail.send(msg)
        else:
            Thread(target=send_async_email, args=(current_app._get_current_object(), msg)).start()

def send_verification_email(user):
    token = user.get_email_verification_token()
    send_email('[Totlahtol] Verify Your Email',
                sender=current_app.config['ADMINS'][0],
                recipients=[user.email],
                text_body=render_template('verify_email.txt',
                                          user=user, token=token),
                html_body=render_template('verify_email.html',
                                          user=user, token=token))

def send_password_reset_email(user):
    token = user.get_reset_password_token()
    send_email('[Totlahtol] Reset Your Password',
               sender=current_app.config['ADMINS'][0],
               recipients=[user.email],
               text_body=render_template('reset_password.txt',
                                         user=user, token=token),
               html_body=render_template('reset_password.html',
                                         user=user, token=token))