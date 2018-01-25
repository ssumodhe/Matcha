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
        # pprint(dbData)
        # virer if last_connexion == None?
        for key, value in dbData.items():
            if value == None:
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
















# infos = {'username': "marie", 
#     'first_name': "marie",
#     'last_name': "jeanne", 
#     'email': "marie@jeanne.com", 
#     'password': "kitty",
#     'sex': '2',
#     'orientation': '2',
#     'bio': 'hello',
#     'interests': '2',
#     'main_picture': '3',
#     'pop_score': '72',
#     'location': "Paris",
#     'last_connexion': '2018-01-10 19:34:39'}
# new_user1 = User.create(infos)



# infos = User.where_multi('age', 5, 52)
# print(infos)
# infos = {'user_id': '2',
# 'data': "qqchose"}
# new_pic = Picture.create(infos)
# print(new_pic.where())

# infos = {'username': "moi", 
#     'first_name': "toi",
#     'last_name': "nous", 
#     'email': "noustoimoi", 
#     'password': "kitty",
#     'sex': '1',
#     'bio': 'hello',
#     'interests': '2',
#     'main_picture': '2',
#     'last_connexion': '2018-01-10 19:34:39'}
# new_user1 = User.create(infos)

# print(new_user1.is_complete())

# infos = {'username': "hello", 
#     'first_name': "toi",
#     'last_name': "bonjour", 
#     'email': "aloha", 
#     'password': "kitty"}
# new_user2 = User.create(infos)

# infos = {'username': "tous", 
#     'first_name': "tous",
#     'last_name': "nous", 
#     'email': "noustous", 
#     'password': "kitty"}
# new_user3 = User.create(infos)

# infos = {'username': "coco", 
#     'first_name': "coco",
#     'last_name': "toto", 
#     'email': "totococo", 
#     'password': "kitty"}
# new_user4 = User.create(infos)

# # qqchose = User.where('first_name', 'toi')
# # my_list_len = len(qqchose)
# # for i in range(0, my_list_len):
# #     print("LIST " + str(i))
# #     print(qqchose[i])

# qqchose = User.find_by('username', 'toi')
# print("All Ok so far")
# if qqchose != None:
#     print(qqchose.getEmail())

# # new_user = new User   
# # new_user = User()
# # new_user.create(qqun)
# # new_user.first_name
# print(new_user)
# print(new_user.email)
# print(new_user.first_name)
# new_user.modif("email", "1234@mail.re")
# # new_user.email = '1234@mail.re'
# print(new_user.email)
# new_user.save()
# print("search : ", new_user.search('*'))
# print("LastCo : ", new_user.getLastConnexion())
# print("User.Id : ", new_user.getId())
# print("PopScore : ", new_user.getPopScore())

