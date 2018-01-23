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
			print(all_likes)
			for item in all_likes:
				print("Im going in")
				if Match.is_match(str(auth.getId()), str(item['victim_id'])) == True:
					print(item) 

			return render_template('messenger.html')
		else:
			return redirect(url_for('accueil'))
