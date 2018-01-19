import sqlite3
from datetime import date, datetime
import models.user

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

    # faire where: qui return un tableau de tous les thomas si on cherche tous les thomas


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