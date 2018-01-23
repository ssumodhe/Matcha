# -*- coding:utf-8 -*-
from flask import Flask, request, abort, redirect, url_for, render_template, session
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from datetime import date, datetime
from flask_session import Session
from pprint import pprint

import re
import os
import html

from models.user import User
from models.user import Like
from models.user import View
from models.user import Block
from models.user import Match
from models.user import Picture

UPLOAD_FOLDER = 'static/users_pictures'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
sess = Session()
app.secret_key = 'super secret pswd'
app.config['SESSION_TYPE'] = 'filesystem'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
sess.init_app(app)

class ProfileController:
	def __init__(self):
		pass

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
				if victim == None:
					return redirect(url_for('profile_not_exists'))
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
			infos['age'] = auth.getAge()
			
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

			# Put in first ELSE at the top
			if infos['is_user_me'] == False:
				stalker = User.find_by('username', infos['stalker'])
				infos['has_liked'] = Like.exists('stalker_id', stalker.getId(), 'victim_id', auth.getId())
				infos['has_blocked'] = Block.exists('by_id', stalker.getId(), 'blocked_id', auth.getId())
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
