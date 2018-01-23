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

class LikeController:
	def __init__(self):
		pass

	@staticmethod
	def like(form):
		stalker = User.find_by('username', form['stalker'])
		victim = User.find_by('username', form['victim'])
		infos = {}
		infos['stalker_id'] = stalker.getId()
		infos['victim_id'] = victim.getId()
		like = Like.create(infos)

		check_both = Like.find_both('stalker_id', victim.getId(), 'victim_id', stalker.getId())
		if check_both != None:
			infos = {}
			infos['user1_id'] = stalker.getId()
			infos['user2_id'] = victim.getId()
			match = Match.create(infos)
			# notif de match else: notif de like

		return redirect(url_for('profile', username=form['victim']))

	@staticmethod
	def unlike(form):
		stalker = User.find_by('username', form['stalker'])
		victim = User.find_by('username', form['victim'])
		unlike = Like.find_both('stalker_id', stalker.getId(), 'victim_id', victim.getId())
		unlike.delete()
		return redirect(url_for('profile', username=form['victim']))
