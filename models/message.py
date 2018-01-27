import pprint
import sqlite3 

from models.model import Model

db = sqlite3.connect('Matcha.db', check_same_thread=False)
cursor = db.cursor()

class Message(Model):
    def __init__(self, infos):
        super().__init__(infos)
        pass

    # getID in Model

    def getMatchId(self):
        if hasattr(self, 'match_id'):
            return self.match_id
        else:
            the_info = self.search('match_id')
            return the_info[0]

    def getFromId(self):
        if hasattr(self, 'from_id'):
            return self.from_id
        else:
            the_info = self.search('from_id')
            return the_info[0]

    def getContent(self):
        if hasattr(self, 'content'):
            return self.content
        else:
            the_info = self.search('content')
            return the_info[0]

    # getCreatedAt in Model