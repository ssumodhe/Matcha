# -*- coding:utf-8 -*-
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import date
from flask import render_template
from pprint import pprint
import re
from models.user import User

class RootController:
	def __init__(self):
		pass

	@staticmethod
	def view():
		return render_template('index.html')

	@staticmethod
	def signup(form):
		for item in form.values():
			if item == '' or item == None:
				error = "REMPLIS TOUS LES P***** DE CHAMPS!"
				return render_template('index.html', error=error)
		
		if form['password'] != form['password_2']:
			error = "P*****, mets les meme mots de passe!"
			return render_template('index.html', error=error)

		if not re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", form['email']):
			error = "P***** mais ecris bien ton email!"
			return render_template('index.html', error=error)

		# Check if form['username'] & form['email'] doesn't already exists avec le find_by de User
		# Si find_by return NULL, il a rien trouvé c'est good. Otherwise: return error

		infos = form.to_dict()
		infos.pop('password_2')
		infos.pop('sign_up')
		infos['password'] = generate_password_hash(infos['password'])
		new_user = User.create(infos)



		return render_template('index.html')