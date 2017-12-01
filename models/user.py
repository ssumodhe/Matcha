# -*- coding:utf-8 -*-
from datetime import date, datetime
import sqlite3  
db = sqlite3.connect('Matcha.db')
cursor = db.cursor()

class Model():
    def __init__(self):
        pass

    @classmethod
    def create(cls, qqun):
        qqun['created_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        keys = ['"' + item + '"' for item in qqun.keys()]
        values = ['"' + item + '"' for item in qqun.values()]
        get_keys = ", ".join(keys)
        get_values = ", ".join(values)
        request = "INSERT INTO users (" + get_keys + ") VALUES (" + get_values + ");"
        print(request)
        cursor.execute(request)
        db.commit()
        cursor.close()
        return eval(cls.__name__ + "()")

class User(Model):
    def __init__(self):
        pass

    

qqun = {'username': "moi", 
    'first_name': "toi",
    'last_name': "nous", 
    'email': "noustoimoi", 
    'password': "kitty"}
    

new_user = User.create(qqun)
print(new_user)
print(type(new_user))