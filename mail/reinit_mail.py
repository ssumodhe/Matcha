from mail.mail import Mail

class ReinitMail(Mail):

	subject = "Reinit your password"

	body = "Please visit http://localhost:5000/reinit_pwd?hash={}"

	def __init__(self, recipients, hash):
		self.__class__.body = self.__class__.body.format(hash[14:])
		super().__init__(recipients)
		