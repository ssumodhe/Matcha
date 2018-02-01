import sqlite3 

from models.model import Model
from models.block import Block

class Notification(Model):

	def __init__(self, infos):
		super().__init__(infos)
		pass

	def getUserId(self):
		if hasattr(self, 'user_id'):
			return self.user_id
		else:
			the_info = self.search('user_id')
			return the_info[0]

	def getMessage(self):
		if hasattr(self, 'message'):
			return self.message
		else:
			the_info = self.search('message')
			return the_info[0]

	def getSeen(self):
		if hasattr(self, 'seen'):
			return self.seen
		else:
			the_info = self.search('seen')
			return the_info[0]

	@classmethod
	def create_if(self, infos, stalker_id):
		if Block.find_both('by_id', infos['user_id'], 'blocked_id', stalker_id) == None:
			return self.create(infos)
		pass

	@classmethod
	def setAsSeen(self, user_id):
		def dict_factory(cursor, row):
			d = {}
			for idx, col in enumerate(cursor.description):
				d[col[0]] = row[idx]
			return d

		db = sqlite3.connect('Matcha.db')
		db.row_factory = dict_factory
		cursor = db.cursor()

		req = "UPDATE notifications SET 'seen'=1 WHERE user_id="+user_id+";"
		cursor.execute(req)
		db.commit()
		cursor.close()
		pass

