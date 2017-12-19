# -*- coding:utf-8 -*-
from datetime import date
from flask import render_template

class RootController:
	def __init__(self):
		pass

	@staticmethod
	def view():
		mots = ["bonjour", "à", "toi,", "visiteur."]
		d = date.today().isoformat()
		return render_template('index.html', 
			mots=mots,
			date=d)
