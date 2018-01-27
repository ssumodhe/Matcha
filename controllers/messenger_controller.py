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
	def messenger(form=None):
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

			if form != None:
				print("\n\n\nMESSAGE")
				print(form)
				message = form['message'].strip()
				message = html.escape(message)

				# save dans MESSAGE table
				to = User.find_by('username', form['to'])
				match = Match.find_both('user1_id', auth.getId(), 'user2_id', to.getId())
				if match == None:
					match = Match.find_both('user1_id', to.getId(), 'user2_id', auth.getId())
				new_msg = {}
				new_msg['match_id'] = match.getId()
				new_msg['from_id'] = auth.getId()
				new_msg['content'] = message
				print(new_msg)
				msg = Message.create(new_msg)
				# need to give the infos enabling the form when form is send

			else:
				print("\n\nNo FORM")

			mee = auth.getUserName()
			return render_template('messenger.html', infos=infos, my_username=mee)
		else:
			return redirect(url_for('accueil'))

	@staticmethod
	def dialog(exp, dest):
		if 'user' in session:
			auth = User.find_by('username', session['user'])
			
			# get all messages from MESSAGE table and display in dialog template
			
			return render_template('dialog.html', exp=exp, dest=dest)
		else:
			return redirect(url_for('accueil'))