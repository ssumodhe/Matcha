import pprint

from models.model import Model

db = sqlite3.connect('Matcha.db', check_same_thread=False)
cursor = db.cursor()

class Message(Model):
    def __init__(self, infos):
        super().__init__(infos)
        pass

    # getID in Model

    def getMatchId(self):
        if hasattr(self, 'dialog_id'):
            return self.dialog_id
        else:
            the_info = self.search('dialog_id')
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