 # -*- coding:utf-8 -*-
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, request, abort, redirect, url_for, render_template, session
from datetime import date, datetime

import sqlite3 
import pprint

from models.model import Model

db = sqlite3.connect('Matcha.db', check_same_thread=False)
cursor = db.cursor()



class Block(Model):
    def __init__(self, infos):
        super().__init__(infos)
        pass

    # getID in Model

    def getById(self):
        if hasattr(self, 'by_id'):
            return self.by_id
        else:
            the_info = self.search('by_id')
            return the_info[0]

    def getBlockedId(self):
        if hasattr(self, 'blocked_id'):
            return self.blocked_id
        else:
            the_info = self.search('blocked_id')
            return the_info[0]

    # getCreatedAt in Model