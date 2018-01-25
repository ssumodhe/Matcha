 # -*- coding:utf-8 -*-
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, request, abort, redirect, url_for, render_template, session
from datetime import date, datetime

import sqlite3 
import pprint

from models.model import Model

db = sqlite3.connect('Matcha.db', check_same_thread=False)
cursor = db.cursor()

class UsersInterest(Model):
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

    def getInterestId(self):
        if hasattr(self, 'interest_id'):
            return self.interest_id
        else:
            the_info = self.search('interest_id')
            return the_info[0]

    # getCreatedAt in Model