from app import app, db
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

def verify_email_verification_token(token):
    s = Serializer(app.config['SECRET_KEY'])
    try:
        email = s.loads(token)
    except:
        return None
    user = db.session.query(User).filter_by(email=email).first()
    if user:
        user.email_verified = True
        db.session.commit()
        return user
    return None
