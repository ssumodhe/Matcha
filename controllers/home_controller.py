# -*- coding:utf-8 -*-
from flask import Flask, request, abort, redirect, url_for, render_template, session
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from datetime import date, datetime
from flask_session import Session
from vincenty import vincenty
from pprint import pprint

import re
import os
import html

from models.user import User
from models.like import Like
from models.view import View
from models.block import Block
from models.match import Match
from models.picture import Picture

UPLOAD_FOLDER = 'static/users_pictures'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
sess = Session()
app.secret_key = 'super secret pswd'
app.config['SESSION_TYPE'] = 'filesystem'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
sess.init_app(app)

class HomeController:
	def __init__(self):
		pass

	@staticmethod
	def home():
		if 'user' in session:
			auth = User.find_by('username', session['user'])
			if auth.is_complete() == False:
				return redirect(url_for('profile', username=session['user']))
			orientation = auth.getOrientation()
			sex = auth.getSex()
			if orientation == '0':
				infos = User.where('sex', sex)
				for item in infos:
					if int(item['orientation']) == 1:
						infos.remove(item)
			elif orientation == '1' and sex == '1':
				infos = User.where('sex', '2')
				for item in infos:
					if int(item['orientation']) == 0:
						infos.remove(item)
			elif orientation == '1' and sex == '2':
				infos = User.where('sex', '1')
				for item in infos:
					if int(item['orientation']) == 0:
						infos.remove(item)
			else:
				infos = User.where_multi('sex', 1, 2)
				for item in infos:
					if int(sex) == 1 and int(item['sex']) == 2 and int(item['orientation']) == 0:
						infos.remove(item)
					if int(sex) == 2 and int(item['sex']) == 1 and int(item['orientation']) == 0:
						infos.remove(item)
					if int(sex) == int(item['sex']) and int(item['orientation']) == 1:
						infos.remove(item)

			for item in infos:
				if Block.exists('by_id', auth.getId(), 'blocked_id', item['id']) == True:
					infos.remove(item)

			for item in infos:
				item['profile_picture'] = Picture.fillInInfos(item['id'], '1')
				item.pop('password')

			for item in infos:
				if item['username'] == session['user']:
					infos.remove(item)

			n = len(infos)
			return render_template('home.html', infos=infos, length=n)
		else:
			return redirect(url_for('accueil'))

	@staticmethod
	def search(form):
		if 'user' in session:
			auth = User.find_by('username', session['user'])
			orientation = auth.getOrientation()
			sex = auth.getSex()
			if orientation == '0':
				infos = User.where('sex', sex)
				for item in infos:
					if int(item['orientation']) == 1:
						infos.remove(item)
			elif orientation == '1' and sex == '1':
				infos = User.where('sex', '2')
				for item in infos:
					if int(item['orientation']) == 0:
						infos.remove(item)
			elif orientation == '1' and sex == '2':
				infos = User.where('sex', '1')
				for item in infos:
					if int(item['orientation']) == 0:
						infos.remove(item)
			else:
				infos = User.where_multi('sex', 1, 2)
				for item in infos:
					if int(sex) == 1 and int(item['sex']) == 2 and int(item['orientation']) == 0:
						infos.remove(item)
					if int(sex) == 2 and int(item['sex']) == 1 and int(item['orientation']) == 0:
						infos.remove(item)
					if int(sex) == int(item['sex']) and int(item['orientation']) == 1:
						infos.remove(item)

			if form['age_min'] != '' and form['age_max'] != '':
				for item in infos:
					if int(item['age']) < int(form['age_min']) or int(item['age']) > int(form['age_max']):
						infos.remove(item)

			if form['pop_score_min'] != '' and form['pop_score_max'] != '':
				for item in infos:
					if item['pop_score'] < form['pop_score_min'] or item['pop_score'] > form['pop_score_max']:
						infos.remove(item)


			if form['location'] != '':
				my_loc = (float(auth.getLat()), float(auth.getLong()))
				for item in infos:
					if item['lat'] is not None and item['long'] is not None:
						other = User.find_by('username', item['username'])
						else_loc = (float(other.getLat()), float(other.getLong()))
						delta = vincenty(my_loc, else_loc)
						if int(delta) > int(form['location']):
							infos.remove(item)





			for item in infos:
				item['profile_picture'] = Picture.fillInInfos(item['id'], '1')
				item.pop('password')
			
			for item in infos:
				if item['username'] == session['user']:
					infos.remove(item)
		
			n = len(infos)
			return render_template('home.html', infos=infos, length=n)

		else:
			return redirect(url_for('accueil'))



















































		