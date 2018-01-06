# -*- coding:utf-8 -*-
from datetime import date
from flask import render_template
from pprint import pprint

class RootController:
	def __init__(self):
		pass

	@staticmethod
	def view():
		return render_template('index.html')

	@staticmethod
	def signup(form, session):
		pprint(form)
		pprint("SESSSIONNÑ")
		pprint(session)
		for item in form.values():
			if item == '' or item == None:
				error = "REMPLIS LES P***** DE CHAMPS!"
				return render_template('index.html', error=error)
		
		form['username'] 
		form['first_name']
		form['last_name']
		form['email']
		form['password']
		form['password_2']
		return render_template('index.html')