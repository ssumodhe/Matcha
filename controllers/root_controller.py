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

		auth = User.find_by('username', form['username'])
		if auth != None:
			error = "Pseudo déjà utilisé!"
			return render_template('index.html', error=error)

		auth = User.find_by('email', form['email'])
		if auth != None:
			error = "Cet email existe déjà!"
			return render_template('index.html', error=error)

		if not re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", form['email']):
			error = "P***** mais ecris bien ton email!"
			return render_template('index.html', error=error)

		if not re.match(r"(^(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9])[A-Za-z0-9_#@%\*\-]{8,24}$)", form['password']):
			error = "Il s'agirait tout de meme de faire un effort sur la sécurité de ton mot de passe!"
			return render_template('index.html', error=error)

		if form['password'] != form['password_2']:
			error = "P*****, mets les meme mots de passe!"
			return render_template('index.html', error=error)

		# All Good on procède à la création du User
		infos = form.to_dict()
		infos.pop('password_2')
		infos.pop('sign_up')
		infos['password'] = generate_password_hash(infos['password'])
		new_user = User.create(infos)

		return render_template('index.html')