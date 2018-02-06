from models.user import User
from models.notification import Notification
from models.picture import Picture
from werkzeug.security import generate_password_hash
from faker import Faker
from datetime import date
import random
import sqlite3

fake = Faker('fr_FR')

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
	'lat' : '48.8600',
	'long' : '2.3500',
	'last_connexion': date.today().isoformat(),
	'fake': '0',
	'main_picture': '1'})

Picture.create({
	'user_id': '1',
	'data': 'hello_1.png'
	})

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
	'lat' : '48.891210',
	'long' : '2.322323',
	'last_connexion': date.today().isoformat(),
	'fake': '0',
	'main_picture': '1'})


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
			'sex': str(random.randint(1, 2)),
			'location': fake.city(),
			'lat': str(fake.latitude()),
			'long': str(fake.longitude()),
			'orientation': str(random.randint(0, 2)),
			'status': str(random.randint(0, 1)),
			'fake': '1',
			'bio': fake.sentence(),
			'interests': '1',
			'last_connexion': date.today().isoformat(),
			'main_picture': '1'
		})
	except sqlite3.IntegrityError as e:
		print(e)
