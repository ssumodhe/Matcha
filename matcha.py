# -*- coding:utf-8 -*-
from flask import Flask, request, abort, redirect, url_for, render_template, session
from flask_session import Session
from controllers.root_controller import RootController
from datetime import datetime, date
from config import setup_db
from geolite2 import geolite2
import pprint




app = Flask(__name__)
sess = Session()
app.secret_key = 'super secret pswd'
app.config['SESSION_TYPE'] = 'filesystem'
sess.init_app(app)



# Passera les variables à toutes les pages.
@app.context_processor
def get_time_now():
  return dict({'now_year': datetime.now().year, 'date': date.today().isoformat()})

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

@app.route('/signup', methods=['GET', 'POST'])
def signup():
  return RootController.signup(request.form)

@app.route('/signin', methods=['GET', 'POST'])
def signin():
  return RootController.signin(request.form)

@app.route('/signout')
def signout():
  return RootController.signout()

@app.route('/home')
def home():
  return render_template('home.html')

@app.route('/messenger')
def messenger():
  return render_template('messenger.html')

@app.route('/profile/<username>')
def profile(username):
  return RootController.profile(username)

@app.route('/profile_modifications', methods=['GET', 'POST'])
def profile_modifications():
  return RootController.profile_modifications(request.form)

@app.route('/profile_add_picture', methods=['GET', 'POST'])
def profile_add_picture():
  # file = request.files
  # pic = file.to_dict()
  # for key, value in pic.items():
  #   print("FILE : " + str(key) + " et = " + str(value))
  # form = request.form
  # user = form.to_dict()
  # for key, value in user.items():
  #   print("FORM : " + str(key) + " et = " + str(value)) 
  return RootController.profile_add_picture(request.form, request.files)

@app.route('/profile_not_complete')
def profile_not_complete():
  return render_template('profile_not_complete.html')


@app.errorhandler(404)
def page_not_found(error):
	return render_template('errors/404.html'), 404

# Permet d'executer l'application
if __name__ == '__main__':
   app.run(debug=True)
   # host '0.0.0.0' permet à toutes les machines du reseau d'acceder à l'application
   # port=XXXX permet de choisir le port pour acceder à l'application
   # app.run(debug=True, host='0.0.0.0', port=3000)






































