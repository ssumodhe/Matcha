 # -*- coding:utf-8 -*-
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, request, abort, redirect, url_for, render_template, session
from datetime import date, datetime

import sqlite3 
import pprint

from models.model import Model

db = sqlite3.connect('Matcha.db', check_same_thread=False)
cursor = db.cursor()


class User(Model):
    def __init__(self, infos):
        super().__init__(infos)
        pass

    def is_complete(self):
        def dict_factory(cursor, row):
            d = {}
            for idx, col in enumerate(cursor.description):
                d[col[0]] = row[idx]
            return d

        db = sqlite3.connect('Matcha.db')
        db.row_factory = dict_factory
        cursor = db.cursor()
        request = "SELECT * FROM '" + self.get_table_name() + "' WHERE id = " + self.id + ";"
        cursor.execute(request)
        dbData = cursor.fetchone()
        db.commit()
        cursor.close()
        for key, value in dbData.items():
            if value == None and key != 'main_picture':
                return False
        return True

    def check_password(self, password):
        return check_password_hash(getPassword(), password)

    # getID in Model

    def getUserName(self):
        if hasattr(self, 'username'):
            return self.username
        else:
            the_info = self.search('username')
            return the_info[0]

    def getFirstName(self):
        if hasattr(self, 'first_name'):
            return self.first_name
        else:
            the_info = self.search('first_name')
            return the_info[0]

    def getLastName(self):
        if hasattr(self, 'last_name'):
            return self.last_name
        else:
            the_info = self.search('last_name')
            return the_info[0]

    def getEmail(self):
        if hasattr(self, 'email'):
            return self.email
        else:
            the_info = self.search('email')
            return the_info[0]

    def getPassword(self):
        if hasattr(self, 'password'):
            return self.password
        else:
            the_info = self.search('password')
            return the_info[0]

    def getConfirmed(self):
        if hasattr(self, 'confirmed'):
            return self.confirmed
        else:
            the_info = self.search('confirmed')
            return the_info[0]

    def getAge(self):
        if hasattr(self, 'age'):
            return self.age
        else:
            the_info = self.search('age')
            return the_info[0]

    def getSex(self):
        if hasattr(self, 'sex'):
            return self.sex
        else:
            the_info = self.search('sex')
            return the_info[0]

    def getOrientation(self):
        if hasattr(self, 'orientation'):
            return self.orientation
        else:
            the_info = self.search('orientation')
            return the_info[0]

    def getBio(self):
        if hasattr(self, 'bio'):
            return self.bio
        else:
            the_info = self.search('bio')
            return the_info[0]

    def getInterests(self):
        if hasattr(self, 'interests'):
            return self.interests
        else:
            the_info = self.search('interests')
            return the_info[0]

    def getMainPicture(self):
        if hasattr(self, 'main_picture'):
            return self.main_picture
        else:
            the_info = self.search('main_picture')
            return the_info[0]

    def getPopScore(self):
        if hasattr(self, 'pop_score'):
            return self.pop_score
        else:
            the_info = self.search('pop_score')
            return the_info[0]

    def getLocation(self):
        if hasattr(self, 'location'):
            return self.location
        else:
            the_info = self.search('location')
            return the_info[0]

    def getLat(self):
        if hasattr(self, 'lat'):
            return self.lat
        else:
            the_info = self.search('lat')
            return the_info[0]

    def getLong(self):
        if hasattr(self, 'long'):
            return self.long
        else:
            the_info = self.search('long')
            return the_info[0]

    def getLastConnexion(self):
        if hasattr(self, 'last_connexion'):
            return self.last_connexion
        else:
            the_info = self.search('last_connexion')
            return the_info[0]

    def getStatus(self):
        if hasattr(self, 'status'):
            return self.status
        else:
            the_info = self.search('status')
            return the_info[0]
    # getCreatedAt in Model
