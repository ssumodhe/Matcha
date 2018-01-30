from pprint import pprint
from flask import jsonify
from flask import Flask, request, abort, redirect, url_for, render_template, session

from models.user import User
from models.notification import Notification

class NotificationController():
	def __init__(self):
		pass

	@staticmethod
	def notifications():
		if 'user' in session:
			user = User.find_by("username", session['user'])
			notes = Notification.where('user_id', user.getId())
			Notification.setAsSeen(user.getId())
			return render_template('notifications.html', notes=notes)
		else:
			return redirect(url_for('accueil'))

	@staticmethod
	def list_notifications(form):
		user = User.find_by("username", form["username"])
		if not user:
			abort(404)
		notifications = Notification.where("user_id", user.getId())

		return jsonify(notifications)

	@staticmethod
	def unread_notifications(form):
		user = User.find_by("username", form["username"])
		if not user:
			abort(404)
		notifications = Notification.where("user_id", user.getId())
		unread_notifications = [n for n in notifications if n['seen'] == 0]

		return jsonify(unread_notifications)