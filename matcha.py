# -*- coding:utf-8 -*-
from flask import Flask, request, abort, redirect, url_for, render_template, session
from flask_session import Session
from controllers.root_controller import RootController
from controllers.user_controller import UserController
from controllers.profile_controller import ProfileController
from controllers.like_controller import LikeController
from controllers.home_controller import HomeController
from controllers.block_controller import BlockController
from controllers.messenger_controller import MessengerController
from controllers.notification_controller import NotificationController
from datetime import datetime, date, timedelta
from config import setup_db
from geolite2 import geolite2
import pprint

app = Flask(__name__)
sess = Session()
app.secret_key = 'super secret pswd'
app.config['SESSION_TYPE'] = 'filesystem'
sess.init_app(app)

# By default in Flask, permanent_session_lifetime is set to 31 days.
@app.before_request
def make_session_permanent():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=60)
 
# Passera les variables à toutes les pages.
@app.context_processor
def get_time_now():
  return dict({'now_year': datetime.now().year, 'date': date.today().isoformat(), 'name': session['user']})

@app.route('/')
def accueil():
  ip = request.environ['REMOTE_ADDR']
  print("IP = " + ip)
  # reader = geolite2.reader()
  # match = reader.get('62.210.33.168')
  # geolite2.close()
  # print(match is not None)
  # print(match)
  # print(match['location'])
  return RootController.view()

@app.route('/forgotten_password', methods=['GET'])
def forgotten_pwd():
  return UserController.forgotten_pwd()

@app.route('/mail_reinit_pwd', methods=['GET'])
def mail_reinit_pwd():
  return UserController.mail_reinit_pwd()

@app.route('/reinit_pwd', methods=['GET'])
def reinit_pwd():
  return UserController.display_reinit_pwd()

@app.route('/set_pwd', methods=['POST'])
def set_pwd():
  return UserController.set_new_pwd()

@app.route('/signup', methods=['GET', 'POST'])
def signup():
  return RootController.signup(request.form)

@app.route('/signin', methods=['GET', 'POST'])
def signin():
  return RootController.signin(request.form)

@app.route('/signout')
def signout():
  return RootController.signout()

@app.route('/profile/<username>')
def profile(username):
  return ProfileController.profile(username)

@app.route('/profile_modifications', methods=['GET', 'POST'])
def profile_modifications():
  return ProfileController.profile_modifications(request.form)

@app.route('/profile_add_picture', methods=['GET', 'POST'])
def profile_add_picture():
  return ProfileController.profile_add_picture(request.form, request.files)

@app.route('/profile_not_complete')
def profile_not_complete():
  return render_template('profile_not_complete.html')

@app.route('/profile_not_exists')
def profile_not_exists():
  return render_template('profile_not_exists.html')

@app.route('/like', methods=['POST'])
def like():
  return LikeController.like(request.form)

@app.route('/unlike', methods=['POST'])
def unlike():
  return LikeController.unlike(request.form)


@app.route('/confirm_account/<hash>')
def confirm_account(hash):
  return UserController.confirm_account(hash)

@app.route('/block', methods=['POST'])
def block():
  return BlockController.block(request.form)

@app.route('/unblock', methods=['POST'])
def unblock():
  return BlockController.unblock(request.form)

@app.route('/home')
def home():
  return HomeController.home()

@app.route('/search', methods=['POST'])
def search():
  return HomeController.search(request.form)

@app.route('/messenger', methods=['GET', 'POST'])
def messenger():
  if request.method == 'POST':
    return MessengerController.messenger(request.form)
  else:
    return MessengerController.messenger()

@app.route('/dialog/<exp>&<dest>')
def dialog(exp, dest):
  return MessengerController.dialog(exp, dest)

@app.route('/notifications', methods=['POST'])
def list_notifications():
  return NotificationController.list_notifications(request.form)

@app.route('/unread_notif', methods=['POST'])
def unread_notifications():
  return NotificationController.unread_notifications(request.form)

@app.errorhandler(404)
def page_not_found(error):
	return render_template('errors/404.html'), 404

# Permet d'executer l'application
if __name__ == '__main__':
   app.run(debug=True, host='0.0.0.0', threaded=True)
   # host '0.0.0.0' permet à toutes les machines du reseau d'acceder à l'application
   # port=XXXX permet de choisir le port pour acceder à l'application
   # app.run(debug=True, host='0.0.0.0', port=3000)
