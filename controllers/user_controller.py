# -*- coding:utf-8 -*-
from flask import redirect, render_template, request
from models.user import User
from pprint import pprint
from base64 import decodestring
from mail.reinit_mail import ReinitMail
from flask import abort
from werkzeug.security import generate_password_hash

class UserController:
    def __init__(self):
        pass

    @staticmethod
    def confirm_account():
        hash = request.args.get('hash')
        user = User.find_by('password', "pbkdf2:sha256:" + hash)
        if not user:
            return redirect("/")
        else:
            user.modif('confirmed', '1')
            user.save()
            return render_template('index.html', all_ok="Ton compte a été confirmé, tu peux te connecter!")

    @staticmethod
    def forgotten_pwd():
        return render_template('forgotten_pwd.html')

    @staticmethod
    def mail_reinit_pwd():
        user_email = request.args.get('email')
        user = User.find_by("email", user_email)
        if user:
            email = ReinitMail(user.getEmail(), user.getPassword())
            email.send()
            return render_template('index.html', all_ok="We sent you the link to reinit your pwd")    
        else: 
            return render_template('index.html', error="We did not find any user matching this email")

    @staticmethod
    def display_reinit_pwd():
        if 'hash' in request.args:
            user_hash = "pbkdf2:sha256:" + request.args.get('hash')
            user = User.find_by("password", user_hash)
            if user:
                return render_template('change_pwd.html', hash=user_hash)
        abort(404)

    @staticmethod
    def set_new_pwd():
        if ('hash' in request.form) and (request.form['password'] == request.form['verify']):
            user = User.find_by('password', request.form['hash'])
            if user:
                hash = generate_password_hash(request.form['password'])
                import pdb; pdb.set_trace()
                user.modif('password', hash)
                user.save()
                return render_template('index.html', all_ok='Your password have been change, you can login')
        abort(404)
