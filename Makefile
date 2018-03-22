DB_NAME = Matcha.db
USERS_PIC = static/users_pictures

all: drop setup seed

setup: 
	@echo "db setup"
	@python config/setup_db.py
	@mkdir static/users_pictures

seed:
	@echo "db seed"
	@python seed.py

del-do:
	@echo "file deleted"
	@rm -r $(USERS_PIC)
	@echo "file created"
	@mkdir $(USERS_PIC)

drop:
	@echo "db droped"
	@rm $(DB_NAME)

