from models.user import User
from models.notification import Notification
from werkzeug.security import generate_password_hash
from faker import Faker
import random
import sqlite3

fake = Faker('fr_FR')

for i in range(1000):
	try:
		first_name = fake.first_name()
		last_name = fake.last_name()
		User.create({
			'username': first_name + last_name,
			'first_name': first_name,
			'last_name': last_name,
			'email': fake.free_email(),
			'password': generate_password_hash('QWErty123'),
			'confirmed': '1',
			'age': str(random.randint(18, 70)),
			'sex': str(random.uniform(0, 1)),
			'lat': str(fake.latitude()),
			'long': str(fake.longitude()),
			'fake': '1'
		})
	except sqlite3.IntegrityError as e:
		print(e)

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
	'bio': 'homme hetero',
	'fake': '0'})

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
	'bio': 'femme hetero',
	'fake': '0'})
	
# Notification.create({
# 	'user_id': '1',
# 	'message': 'Hey just setting up my notifications'
# 	})
