from mail.mail import Mail

class ConfirmationMail(Mail):

    subject = "Confirm your account"

    body = "Please visit http://localhost:5000/confirm_account?hash={} to complete your registration"

    def __init__(self, recipients, hash):
    	self.__class__.body = self.__class__.body.format(hash[14:])
        super().__init__(recipients)
