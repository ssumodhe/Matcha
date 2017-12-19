# -*- coding:utf-8 -*-
from flask import Flask, request, abort, redirect, url_for, render_template
from controllers.root_controller import RootController

app = Flask(__name__)

# Passera la variable 'titre' a toutes les pages.
@app.context_processor
def passer_titre():
    return dict(titre="Bienvenue !")

@app.route('/')
def accueil():
    return RootController.view()

@app.errorhandler(404)
def page_not_found(error):
	return render_template('errors/404.html'), 404

# Permet d'executer l'application
# (Si on execute l'app : run l'appli)
if __name__ == '__main__':
   app.run(debug=True)
   # host '0.0.0.0' permet à toutes les machines du reseau
   # d'acceder à l'application
   # app.run(debug=True, host='0.0.0.0', port=3000)