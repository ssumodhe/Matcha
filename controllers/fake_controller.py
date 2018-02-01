from flask import Flask, request, abort, redirect, url_for, render_template, session
from pprint import pprint

from models.user import User

class FakeController:
	def __init__(self):
		pass

	@staticmethod
	def fake_report(form):
		print("IN FAKE REPORT")
		faker = User.find_by('username', form['victim'])
		faker.modif('fake', '1')
		faker.save()

		return redirect(url_for('profile', username=form['victim']))