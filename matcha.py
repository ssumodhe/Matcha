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



if __name__ == '__main__':
   app.run(debug=True)