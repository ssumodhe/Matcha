 # -*- coding:utf-8 -*-
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, request, abort, redirect, url_for, render_template, session
from datetime import date, datetime

import sqlite3 
import pprint

from models.model import Model

db = sqlite3.connect('Matcha.db', check_same_thread=False)
cursor = db.cursor()

class Picture(Model):
    def __init__(self, infos):
        super().__init__(infos)
        pass

    # getID in Model
    def getUserId(self):
        if hasattr(self, 'user_id'):
            return self.user_id
        else:
            the_info = self.search('user_id')
            return the_info[0]

    def getData(self):
        if hasattr(self, 'data'):
            return self.data
        else:
            the_info = self.search('data')
            return the_info[0]
    # getCreatedAt in Model
    @classmethod
    def getPicName(self, user_id, number):
        picture = self.where('user_id', str(user_id))
        for i in range(len(picture)):
            if number in picture[i]['data']:
                return picture[i]['data']
        return None

    @classmethod
    def fillInInfos(self, user_id, number):
        if self.getPicName(user_id, number) != None:
            return url_for('static', filename="users_pictures/" + Picture.getPicName(user_id, number))
        else:
            return url_for('static', filename='img/missing_picture.jpeg')