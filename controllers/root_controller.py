# -*- coding:utf-8 -*-
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from flask import Flask, request, abort, redirect, url_for, render_template, session
from flask_session import Session
from datetime import date, datetime
from pprint import pprint

import re
import html
import os

from models.user import User
from models.user import Like
from models.user import View
from models.user import Picture

UPLOAD_FOLDER = 'static/users_pictures'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
sess = Session()
app.secret_key = 'super secret pswd'
app.config['SESSION_TYPE'] = 'filesystem'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
sess.init_app(app)

class RootController:
	def __init__(self):
		pass

	@staticmethod
	def view():
		if 'user' in session:
			auth = User.find_by('username', session['user'])
			if auth.is_complete() == True:
				return redirect(url_for('home'))
			else:
				return redirect(url_for('profile', username=session['user']))
		return render_template('index.html')

	@staticmethod
	def signup(form):
		for item in form.values():
			if item == '' or item == None:
				error = "REMPLIS TOUS LES P***** DE CHAMPS!"
				return render_template('index.html', error=error)

		auth = User.find_by('username', form['username'])
		if auth != None:
			error = "Ce pseudo existe déjà!"
			return render_template('index.html', error=error)

		auth = User.find_by('email', form['email'])
		if auth != None:
			error = "Cet email existe déjà!"
			return render_template('index.html', error=error)

		# Prendre REGEX du JS in index-controller.js ???
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
		infos.pop('submit')
		infos['password'] = generate_password_hash(infos['password'])
		new_user = User.create(infos)

		all_ok = "C'est Good!"
		return render_template('index.html', all_ok=all_ok)

	@staticmethod
	def signin(form):
		for item in form.values():
			if item == '' or item == None:
				error = "REMPLIS TOUS LES P***** DE CHAMPS!"
				return render_template('index.html', error=error)

		auth = User.find_by('username', form['username'])
		if auth == None:
			error = "On ne connait pas ce pseudo!"
			return render_template('index.html', error=error)
			
		actual_pswd = auth.getPassword()
		hashed_pswd = check_password_hash(actual_pswd, form['password'])
		if hashed_pswd == False:
			error = "Mot de passe incorrect!"
			return render_template('index.html', error=error)

		# All Good on modifie les infos nécessaires
		auth.modif('status', '1')
		auth.modif('last_connexion', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
		auth.save()
		session['user'] = auth.getUserName()

		if auth.is_complete() == True:
			return redirect(url_for('home'))
			# return render_template('home.html', user=session['user'])
		else:
			return redirect(url_for('profile', username=session['user']))
			# return render_template('profile.html', user=session['user'])


	@staticmethod
	def signout():
		if 'user' in session:
			auth = User.find_by('username', session['user'])
			auth.modif('status', '0')
			auth.save()
			session.pop('user', None)
		return redirect(url_for('accueil'))

	

















































