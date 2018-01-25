 # -*- coding:utf-8 -*-
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, request, abort, redirect, url_for, render_template, session
from datetime import date, datetime

import sqlite3 
import pprint

from models.model import Model
from models.like import Like


db = sqlite3.connect('Matcha.db', check_same_thread=False)
cursor = db.cursor()

class Match(Model):
    def __init__(self, infos):
        super().__init__(infos)
        pass

    # getID in Model

    def getUser1Id(self):
        if hasattr(self, 'user1_id'):
            return self.user1_id
        else:
            the_info = self.search('user1_id')
            return the_info[0]

    def getUser2Id(self):
        if hasattr(self, 'user2_id'):
            return self.user2_id
        else:
            the_info = self.search('user2_id')
            return the_info[0]

    @classmethod
    def is_match(self, user1_id, user2_id):
        check_1 = Like.find_both('stalker_id', user1_id, 'victim_id', user2_id)
        check_2 = Like.find_both('stalker_id', user2_id, 'victim_id', user1_id)
        if check_1 != None and check_2 != None:
            return True
        return False

    # getCreatedAt in Model