from mail.mail import Mail

class ConfirmationMail(Mail):

    subject = "Confirm your account"

    body = "Please visit http://localhost:5000/confirm_account/{} to complete your registration"

    def __init__(self, recipients, hash):
        super().__init__(recipients)
