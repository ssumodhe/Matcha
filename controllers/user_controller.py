# -*- coding:utf-8 -*-
from flask import redirect, render_template
from models.user import User
from pprint import pprint
from base64 import decodestring

class UserController:
    def __init__(self):
        pass

    @staticmethod
    def confirm_account(hash):
        print(hash)
        user = User.find_by('password', "pbkdf2:sha256:" + hash)
        if not user:
            return redirect("/")
        else:
            user.modif('confirmed', '1')
            user.save()
            return render_template('index.html', all_ok="Ton compte a été confirmé, tu peux te connecter!")
