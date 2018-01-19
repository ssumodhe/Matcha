# -*- coding:utf-8 -*-
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from flask import Flask, request, abort, redirect, url_for, render_template, session
from flask_session import Session
from datetime import date, datetime
from flask import render_template
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

	@staticmethod
	def profile(username):
		if 'user' in session:
			infos = {}
			if session['user'] == username:
				infos['is_user_me'] = True
			else:
				infos['is_user_me'] = False
				infos['stalker'] = session['user']
				victim = User.find_by('username', username)
				if victim.is_complete() == False:
					return redirect(url_for('profile_not_complete'))
				stalker = User.find_by('username', infos['stalker'])
				view = {}
				view['stalker_id'] = stalker.getId()
				view['victim_id'] = victim.getId()
				View.create(view)
				victim.modif('pop_score', str(View.howMany('victim_id', victim.getId())))
				victim.save()



			auth = User.find_by('username', username)
			# if auth doesn't exists redirect accueil

			infos['username'] = auth.getUserName()
			infos['first_name'] = auth.getFirstName()
			infos['last_name'] = auth.getLastName()
			infos['email'] = auth.getEmail()
			
			if auth.getSex() == '1':
				infos['sex'] = "Homme"
			elif auth.getSex() == '2':
				infos['sex'] = "Femme"
			else:
				infos['sex'] = auth.getSex()
			
			if auth.getOrientation() == '0':
				infos['orientation'] = "Homo"
			elif auth.getOrientation() == '1':
				infos['orientation'] = "Hetero"
			else:
				infos['orientation'] = "Bi"
			

			infos['bio'] = html.unescape(auth.getBio())
			
			infos['interests'] = auth.getInterests()
			infos['main_picture'] = auth.getMainPicture()
			infos['pop_score'] = auth.getPopScore()
			infos['location'] = auth.getLocation()
			infos['last_connexion'] = auth.getLastConnexion()
			infos['status'] = auth.getStatus()

			picture = Picture.where('user_id', auth.getId())
			infos['picture_1'] = Picture.fillInInfos(auth.getId(), '1')
			infos['picture_2'] = Picture.fillInInfos(auth.getId(), '2')
			infos['picture_3'] = Picture.fillInInfos(auth.getId(), '3')
			infos['picture_4'] = Picture.fillInInfos(auth.getId(), '4')
			infos['picture_5'] = Picture.fillInInfos(auth.getId(), '5')

			if infos['is_user_me'] == False:
				stalker = User.find_by('username', infos['stalker'])
				infos['has_liked'] = Like.has_liked(stalker.getId(), auth.getId())
				nb_picture = Picture.howMany('user_id', stalker.getId())
				if nb_picture == 0:
					infos['stalker_can_like'] = False
			infos['nb_like'] = Like.howMany('victim_id', auth.getId())

			all_views = View.where('victim_id', auth.getId())
			join_infos_views = []
			for item in all_views:
				join_infos_views = join_infos_views + User.join('users', 'views', 'id', 'stalker_id', str(item['stalker_id']))
			infos['all_views'] = join_infos_views

			all_likes = Like.where('victim_id', auth.getId())
			join_infos_likes = []
			for item in all_likes:
				join_infos_likes = join_infos_likes + User.join('users', 'likes', 'id', 'stalker_id', str(item['stalker_id']))
			infos['all_likes'] = join_infos_likes
			

			print("\n\nALL_VIEWS")
			print(join_infos_views)
			print("\n\nALL_LIKES")
			print(join_infos_likes)
			

			print("\n\nPROFILE PAGE infos = ")
			print(infos)

			return render_template('profile.html', infos=infos)
		else:
			return redirect(url_for('accueil'))

	@staticmethod
	def profile_modifications(form):
		modif = User.find_by('username', form['username'])
		infos = form.to_dict()
		infos.pop('username')
		infos.pop('submit')
		pprint(form)
		print("MODIFICATIONS PAGE infos = ")
		pprint(infos)
		for key, value in infos.items():
			print("KEY = " + key)
			print("VALUE = " + value)
			if key == "bio":
				value = html.escape(value)
				# need to add html.unescape in /profile when infos
			else:
				# error if spec chars
				print("VALUE2 = " + value)

			modif.modif(key, value)
		modif.save()

		return redirect(url_for('profile', username=modif.getUserName()))

	@staticmethod
	def profile_add_picture(form, file):

		def allowed_file(filename):
			return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

		if 'picture' not in file:
			print('No file part')
			# display error on PROFILE PAGE
		file_to_save = file['picture']
		if file_to_save.filename == '':
			print('No selected file')
			# display error on PROFILE PAGE
			
		if file_to_save and allowed_file(file_to_save.filename):
			filename = secure_filename(file_to_save.filename)
			user = User.find_by('username', form['username'])
			ext = filename.rsplit('.', 1)[1].lower()
			filename = user.getUserName() + "_" + form['number'] + "." + ext
			path_to_upload = os.path.join(app.config['UPLOAD_FOLDER'], filename)
			file_to_save.save(path_to_upload)
			
			if Picture.getPicName(user.getId(), form['number']) == None:
				infos = {}
				infos['user_id'] = user.getId() 
				infos['data'] = filename
				picture = Picture.create(infos)
				
			else:
				expression = user.getUserName() + "_" + form['number'] + ".%"
				picture = Picture.find_like('data', expression)
				picture.modif('data', filename)
				picture.save()
				# SUPPR. if ext differente else bourrage du dossier users_pictures

			if form['number'] == '1':
				user.modif('main_picture', picture.getId())
				user.save()

		return redirect(url_for('profile', username=form['username']))


















































