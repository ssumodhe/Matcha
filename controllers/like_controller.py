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
from models.like import Like
from models.view import View
from models.block import Block
from models.match import Match
from models.picture import Picture
from models.message import Message
from models.notification import Notification

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
			infos = {}
			infos['user_id'] = victim.getId()
			infos['message'] = "Match : <a href='/profile/" + stalker.getUserName() + "'>"+stalker.getUserName()+"</a> vous a liké en retour! C'est un MATCHA!"
			notif = Notification.create_if(infos, stalker.getId())
			infos = {}
			infos['user_id'] = stalker.getId()
			infos['message'] = "Match : C'est un MATCHA! <a href='/profile/" + victim.getUserName() + "'>"+victim.getUserName()+"</a> vous a egalement liké! "
			notif = Notification.create_if(infos, victim.getId())
		else:
			infos = {}
			infos['user_id'] = victim.getId()
			infos['message'] = "Like : Vous avez été Like par <a href='/profile/" + stalker.getUserName() + "'>"+stalker.getUserName()+"</a>"
			notif = Notification.create_if(infos, stalker.getId())

		return redirect(url_for('profile', username=form['victim']))

	@staticmethod
	def unlike(form):
		stalker = User.find_by('username', form['stalker'])
		victim = User.find_by('username', form['victim'])
		unlike = Like.find_both('stalker_id', stalker.getId(), 'victim_id', victim.getId())
		if Match.is_match(stalker.getId(), victim.getId()) == True:
			print("UNLIKE - THERE IS A MATCHA")
			match = Match.find_both('user1_id', stalker.getId(),'user2_id', victim.getId())
			if match == None:
				match = Match.find_both('user1_id', victim.getId(),'user2_id', stalker.getId())
			Message.delete_where('match_id', match.getId())
			print("MATCHA ID = " + match.getId())
			match.delete()
		infos = {}
		infos['user_id'] = victim.getId()
		infos['message'] = "Unlike : Vous avez été Unlike par <a href='/profile/" + stalker.getUserName() + "'>"+stalker.getUserName()+"</a>"
		notif = Notification.create_if(infos, stalker.getId())
		unlike.delete()
		return redirect(url_for('profile', username=form['victim']))
