# config.py
from os import getenv

MAIL_SERVER = getenv('MAIL_SERVER')
MAIL_PORT = getenv('MAIL_PORT')
MAIL_USERNAME = getenv('MAIL_USERNAME')
MAIL_PASSWORD = getenv('MAIL_PASSWORD')
MAIL_DEFAULT_SENDER = getenv('MAIL_DEFAULT_SENDER')
MAIL_USE_TLS = bool(getenv('MAIL_USE_TLS'))
