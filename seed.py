from models.user import User
from models.notification import Notification
from werkzeug.security import generate_password_hash

User.create({
	'username': 'totolapaille',
	'first_name': 'Thomas',
	'last_name': 'Payet',
	'email': 'totolapaille@gmail.com',
	'password': generate_password_hash('fy3wifEE'),
	'confirmed': '1',
	'age': '25',
	'sex': '1'})

User.create({
	'username': 'ketchup',
	'first_name': 'Thomas',
	'last_name': 'P',
	'email': 'thomas@payet.ru',
	'password': generate_password_hash('QWErty123'),
	'confirmed': '1',
	'age': '25',
	'sex': '1',
	'orientation': '1',
	'bio': 'homme hetero'})

User.create({
	'username': 'hello',
	'first_name': 'Elodie',
	'last_name': 'D',
	'email': 'elodie@d.fr',
	'password': generate_password_hash('QWErty123'),
	'confirmed': '1',
	'age': '18',
	'sex': '2',
	'orientation': '1',
	'bio': 'femme hetero'})
Notification.create({
	'user_id': '1',
	'message': 'Hey just setting up my notifications'
	})
