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
from models.user import Picture

UPLOAD_FOLDER = 'static/users_pictures'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
sess = Session()
app.secret_key = 'super secret pswd'
app.config['SESSION_TYPE'] = 'filesystem'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
sess.init_app(app)

class LikeController:
	def __init__(self):
		pass

	@staticmethod
	def like(form):
		print(form)
		stalker = User.find_by('username', form['stalker'])
		victim = User.find_by('username', form['victim'])
		infos = {}
		infos['stalker_id'] = stalker.getId()
		infos['victim_id'] = victim.getId()
		like = Like.create(infos)
		return redirect(url_for('profile', username=form['victim']))