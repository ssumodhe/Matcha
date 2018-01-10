# -*- coding:utf-8 -*-
from flask import Flask, request, abort, redirect, url_for, render_template, session
from flask.ext.session import Session
from controllers.root_controller import RootController
from datetime import datetime, date
from config import setup_db

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
  return RootController.view()

@app.route('/signup', methods=['POST'])
def signup():
  return RootController.signup(request.form)

@app.route('/signin', methods=['POST'])
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

@app.route('/profile')
def profile():
  return render_template('profile.html')


@app.errorhandler(404)
def page_not_found(error):
	return render_template('errors/404.html'), 404

# Permet d'executer l'application
if __name__ == '__main__':
   app.run(debug=True)
   # host '0.0.0.0' permet à toutes les machines du reseau d'acceder à l'application
   # port=XXXX permet de choisir le port pour acceder à l'application
   # app.run(debug=True, host='0.0.0.0', port=3000)