 # -*- coding:utf-8 -*-
from datetime import date, datetime
import sqlite3 
import pprint
db = sqlite3.connect('Matcha.db')
cursor = db.cursor()

class Model():
    def __init__(self, infos):
        for key, value in infos.items():
            str = "self." + key + " = \"" + value +"\""
            exec(str)
        pass

    @classmethod
    def create(cls, infos):
        infos['created_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        keys = ['"' + item + '"' for item in infos.keys()]
        values = ['"' + item + '"' for item in infos.values()]
        get_keys = ", ".join(keys)
        get_values = ", ".join(values)
        request = "INSERT INTO " + cls.get_table_name() + " (" + get_keys + ") VALUES (" + get_values + ");"
        print(request)
        cursor.execute(request)
        db.commit()
        id = cursor.lastrowid
        cursor.close()
        infos['id'] = str(id)
        return eval(cls.__name__ + "(infos)")

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
        # print("self.get_table_name : ", self.get_table_name())
        # print("self.id : ", self.id)
        # print("selfData : ", selfData)
        # print("dbData", dbData)
        for key, value in dbData.items():
            # print("key = ", key)
            # print("value = ", value)
            if key in selfData.keys():
                if str(selfData[key]) != str(value):
                    # print("not the same data =", selfData[key])
                    # print("because of this value =", value)
                    db = sqlite3.connect('Matcha.db')
                    cursor = db.cursor()
                    request = "UPDATE " + self.get_table_name() + " SET '" + key + "' = '" + selfData[key] + "' WHERE id = " + self.id + ";"
                    # print(request)
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
        # save()?????

    def search(self):
        db = sqlite3.connect('Matcha.db')
        cursor = db.cursor()
        request = "SELECT * FROM '" + self.get_table_name() + "' WHERE id = " + self.id + ";"
        cursor.execute(request)
        db.commit()
        answer = cursor.fetchone()
        cursor.close()
        return answer


class User(Model):
    def __init__(self, infos):
        super().__init__(infos)
        pass

infos = {'username': "moi", 
    'first_name': "toi",
    'last_name': "nous", 
    'email': "noustoimoi", 
    'password': "kitty"}
    

new_user = User.create(infos)
# new_user = new User   
# new_user = User()
# new_user.create(qqun)
# new_user.first_name
print(new_user)
print(new_user.email)
print(new_user.first_name)
new_user.modif("email", "1234@mail.re")
# new_user.email = '1234@mail.re'
print(new_user.email)
print(new_user.search())
new_user.save()
print(new_user.search())
new_user.delete()
print(new_user.search())


# usr  = User.find_by({'name': 'thomas'})
# usr.email = 'toto@toto.toto'
# usr.save