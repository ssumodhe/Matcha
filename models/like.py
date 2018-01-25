 # -*- coding:utf-8 -*-
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, request, abort, redirect, url_for, render_template, session
from datetime import date, datetime

import sqlite3 
import pprint

from models.model import Model

db = sqlite3.connect('Matcha.db', check_same_thread=False)
cursor = db.cursor()

class Like(Model):
    def __init__(self, infos):
        super().__init__(infos)
        pass

    # getID in Model

    def getStalkerId(self):
        if hasattr(self, 'stalker_id'):
            return self.stalker_id
        else:
            the_info = self.search('stalker_id')
            return the_info[0]

    def getVictimId(self):
        if hasattr(self, 'victim_id'):
            return self.victim_id
        else:
            the_info = self.search('victim_id')
            return the_info[0]

    # getCreatedAt in Model