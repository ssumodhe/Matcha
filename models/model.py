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
        return cls(infos)

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
        return cls(answer)

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
        return cls(answer)

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
        return cls(answer)

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

    @classmethod
    def delete_where(self, column, value):
        db = sqlite3.connect('Matcha.db')
        cursor = db.cursor()
        request = "DELETE FROM '" + self.get_table_name() + "' WHERE " + column + " = " + value + ";"
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