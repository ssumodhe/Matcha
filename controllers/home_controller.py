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
from models.user import Picture

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
				print("C'est pas complet")
				return redirect(url_for('profile', username=session['user']))
			
			return render_template('home.html')
		else:
			return redirect(url_for('accueil'))
		