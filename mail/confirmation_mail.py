from mail.mail import Mail

class ConfirmationMail(Mail):

    subject = "Confirm your account"

    body = "We should put a confirmation mail in this string"

    def __init__(self, recipients):
        super().__init__(recipients)
