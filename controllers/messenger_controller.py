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

class MessengerController:
	def __init__(self):
		pass

	@staticmethod
	def messenger():
		if 'user' in session:
			auth = User.find_by('username', session['user'])
			all_likes = Like.where('stalker_id', auth.getId())

			infos = []
			for item in all_likes:
				if Match.is_match(str(auth.getId()), str(item['victim_id'])) == True:
					matcher = {}
					the_matcha = User.find_by('id', str(item['victim_id']))
					matcher['username'] = the_matcha.getUserName()
					matcher['status'] = the_matcha.getStatus()
					matcher['profile_picture'] = Picture.fillInInfos(the_matcha.getId(), '1')
					infos.append(matcher)

			
			return render_template('messenger.html', infos=infos)
		else:
			return redirect(url_for('accueil'))

	@staticmethod
	def dialog():
		if 'user' in session:
			auth = User.find_by('username', session['user'])
			
			
			return render_template('dialog.html')
		else:
			return redirect(url_for('accueil'))