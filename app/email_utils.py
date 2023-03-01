from flask import render_template
from flask_mail import Message
# from app import mail

def send_email_verification(new_user):
    token = new_user.get_verification_token()
    msg = Message('Veuillez valider votre adresse email',
                  sender='mhg.airdrop@gmail.com',
                  recipients=[new_user.email])
    msg.body = render_template('email/verify_email.txt',
                               user=new_user, token=token)
    msg.html = render_template('email/verify_email.html',
                               user=new_user, token=token)
    mail.send(msg)