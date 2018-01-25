from flask import Flask
from flask_mail import Message
from flask_mail import Mail as Emailer
from config.config import config

mailer = Emailer()
app = Flask(__name__)
app.config['DEBUG']= True
app.config['MAIL_SERVER']= config['EMAIL']['SMTP_SERVER']
app.config['MAIL_PORT'] = config['EMAIL']['PORT']
app.config['MAIL_USERNAME'] = config['EMAIL']['USERNAME']
app.config['MAIL_PASSWORD'] = config['EMAIL']['PASSWORD']
app.config['MAIL_USE_TLS'] = config['EMAIL'].getboolean('TLS')
app.config['MAIL_USE_SSL'] = config['EMAIL'].getboolean('SSL')
mailer.init_app(app)

class Mail():

    subject = "Basic mail"

    body = "This is the basic mail of matcha, you should not have received this one"

    sender = ("Matcha's team", "no-reply@matcha.matcha")

    def __init__(self, recipients):
        """
        When instanciate class, you can give only one recipient as string
        or a list of recipients (list of string)
        """
        self.recipients = recipients if isinstance(recipients, list) else [recipients]
        self.message = Message(self.__class__.subject, sender=self.__class__.sender, recipients=self.recipients)
        self.message.body = self.__class__.body

    def send(self):
        with app.app_context():
            mailer.send(self.message)
