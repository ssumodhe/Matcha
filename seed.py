from models.user import User
from models.notification import Notification

User.create({
	'username': 'totolapaille',
	'first_name': 'Thomas',
	'last_name': 'Payet',
	'email': 'totolapaille@gmail.com',
	'password': 'fy3wifEE',
	'confirmed': '1',
	'age': '25',
	'sex': '0'})

Notification.create({
	'user_id': '1',
	'message': 'Hey just setting up my notifications'
	})