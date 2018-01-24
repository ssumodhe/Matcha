 # -*- coding:utf-8 -*-
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, request, abort, redirect, url_for, render_template, session
from datetime import date, datetime
import sqlite3 
import pprint
db = sqlite3.connect('Matcha.db', check_same_thread=False)
cursor = db.cursor()

class Model():
    def __init__(self, infos):
        for key, value in infos.items():
            string = "self." + str(key) + " = \"" + str(value) +"\""
            exec(string)
        pass

    @classmethod
    def create(cls, infos):
        infos['created_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        keys = ['"' + item + '"' for item in infos.keys()]
        values = ['"' + item + '"' for item in infos.values()]
        get_keys = ", ".join(keys)
        get_values = ", ".join(values)
        req = "INSERT INTO " + cls.get_table_name() + " (" + get_keys + ") VALUES (" + get_values + ");"
        cursor.execute(req)
        db.commit()
        id = cursor.lastrowid
        # cursor.close()
        infos['id'] = str(id)
        return eval(cls.__name__ + "(infos)")

    @classmethod
    def where(cls, column, value):
        def dict_factory(cursor, row):
            d = {}
            for idx, col in enumerate(cursor.description):
                d[col[0]] = row[idx]
            return d

        db = sqlite3.connect('Matcha.db')
        db.row_factory = dict_factory
        cursor = db.cursor()

        req = "SELECT * FROM '" + cls.get_table_name() + "' WHERE " + cls.get_table_name() + "." + column + " = '" + value + "';"
        cursor.execute(req)
        db.commit()
        answer = cursor.fetchall()
        cursor.close()
        return answer

    @classmethod
    def where_multi(cls, column, val1, val2):
        infos = []
        for i in range(val1, (val2 + 1)):
            answer = cls.where(column, str(i))
            infos = infos + answer
       
        return infos


    # With find_by: Check if return not None
    @classmethod
    def find_by(cls, column, value):
        def dict_factory(cursor, row):
            d = {}
            for idx, col in enumerate(cursor.description):
                d[col[0]] = row[idx]
            return d

        db = sqlite3.connect('Matcha.db')
        db.row_factory = dict_factory
        cursor = db.cursor()

        req = "SELECT * FROM '" + cls.get_table_name() + "' WHERE " + cls.get_table_name() + "." + column + " = '" + value + "' LIMIT 1;"
        cursor.execute(req)
        db.commit()
        answer = cursor.fetchone()
        cursor.close()
        if answer == None:
            return None
        return eval(cls.__name__ + "(answer)")

    @classmethod
    def find_like(cls, column, exp):
        def dict_factory(cursor, row):
            d = {}
            for idx, col in enumerate(cursor.description):
                d[col[0]] = row[idx]
            return d

        db = sqlite3.connect('Matcha.db')
        db.row_factory = dict_factory
        cursor = db.cursor()

        req = "SELECT * FROM '" + cls.get_table_name() + "' WHERE " + cls.get_table_name() + "." + column + " LIKE '" + exp + "' LIMIT 1;"
        cursor.execute(req)
        db.commit()
        answer = cursor.fetchone()
        cursor.close()
        if answer == None:
            return None
        return eval(cls.__name__ + "(answer)")

    @classmethod
    def find_both(cls, col1, val1, col2, val2):
        def dict_factory(cursor, row):
            d = {}
            for idx, col in enumerate(cursor.description):
                d[col[0]] = row[idx]
            return d

        db = sqlite3.connect('Matcha.db')
        db.row_factory = dict_factory
        cursor = db.cursor()

        req = "SELECT * FROM '" + cls.get_table_name() + "' WHERE " + cls.get_table_name() + "." + col1 + " = '" + val1 + "' AND " + cls.get_table_name() + "." + col2 + " = '" + val2 + "' LIMIT 1;"
        cursor.execute(req)
        db.commit()
        answer = cursor.fetchone()
        cursor.close()
        if answer == None:
            return None
        return eval(cls.__name__ + "(answer)")

    @classmethod
    def join(cls, table1, table2, col1, col2, value):
        # Attention la requete SELECT ne prend que l'id et le username (dans db users)
        # et le created_at de l'autre table (table2 ici).
        def dict_factory(cursor, row):
            d = {}
            for idx, col in enumerate(cursor.description):
                d[col[0]] = row[idx]
            return d

        db = sqlite3.connect('Matcha.db')
        db.row_factory = dict_factory
        cursor = db.cursor()

        req = "SELECT users.id, users.username, "+table2+".created_at FROM '" + table1 + "' INNER JOIN '" + table2 + "' ON " + table1 + "." + col1 + " = " + table2 + "." + col2 + " WHERE " + table2 + "." + col2 + " = " + value + ";"
        cursor.execute(req)
        db.commit()
        answer = cursor.fetchall()
        cursor.close()
        return answer

    @classmethod
    def exists(self, col1, val1, col2, val2):
        info = self.where(col1, val1)
        for i in range(len(info)):
            if int(info[i][col2]) == int(val2):
                return True
        return False


    @classmethod
    def howMany(self, column, value):
        def dict_factory(cursor, row):
            d = {}
            for idx, col in enumerate(cursor.description):
                d[col[0]] = row[idx]
            return d

        db = sqlite3.connect('Matcha.db')
        db.row_factory = dict_factory
        cursor = db.cursor()

        req = "SELECT COUNT(*) FROM '" + self.get_table_name() + "' WHERE " + self.get_table_name() + "." + column + " = '" + value + "';"
        cursor.execute(req)
        db.commit()
        answer = cursor.fetchall()
        cursor.close()
        return answer[0]['COUNT(*)']

    @classmethod
    def get_table_name(cls):
        return cls.__name__.lower() + 's'

    def save(self):
        selfData = vars(self)

        def dict_factory(cursor, row):
            d = {}
            for idx, col in enumerate(cursor.description):
                d[col[0]] = row[idx]
            return d

        db = sqlite3.connect('Matcha.db')
        db.row_factory = dict_factory
        cursor = db.cursor()
        request = "SELECT * FROM " + self.get_table_name() + " WHERE id = " + self.id + ";"
        cursor.execute(request)
        dbData = cursor.fetchone()
        db.commit()
        cursor.close()
        for key, value in dbData.items():
            if key in selfData.keys():
                if str(selfData[key]) != str(value):
                    db = sqlite3.connect('Matcha.db')
                    cursor = db.cursor()
                    request = "UPDATE " + self.get_table_name() + " SET '" + key + "' = '" + selfData[key] + "' WHERE id = " + self.id + ";"
                    cursor.execute(request)
                    db.commit()
                    cursor.close()
        pass

    def delete(self):
        db = sqlite3.connect('Matcha.db')
        cursor = db.cursor()
        request = "DELETE FROM '" + self.get_table_name() + "' WHERE id = " + self.id + ";"
        cursor.execute(request)
        db.commit()
        cursor.close()

    def modif(self, key, value):
        str = "self." + key + " = \"" + value +"\""
        exec(str)

    def search(self, column):
        db = sqlite3.connect('Matcha.db')
        cursor = db.cursor()
        request = "SELECT " + column +  " FROM '" + self.get_table_name() + "' WHERE id = " + self.id + ";"
        cursor.execute(request)
        db.commit()
        answer = cursor.fetchone()
        cursor.close()
        return answer

    def getId(self):
        if hasattr(self, 'id'):
            return self.id
        else:
            the_info = self.search('id')
            return the_info[0]

    def getCreatedAt(self):
        if hasattr(self, 'created_at'):
            return self.created_at
        else:
            the_info = self.search('created_at')
            return the_info[0]



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

class View(Model):
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

class Interest(Model):
    def __init__(self, infos):
        super().__init__(infos)
        pass

    # getID in Model

    def getValue(self):
        if hasattr(self, 'value'):
            return self.value
        else:
            the_info = self.search('value')
            return the_info[0]

    # getCreatedAt in Model

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

