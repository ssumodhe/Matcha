DB_NAME = Matcha.db
USERS_PIC = static/users_pictures

all: del-do drop setup

setup: 
	@echo "db setup"
	@python config/setup_db.py

# seed:
# 	@echo "db seed"
# 	@php config/seed.php

del-do:
	@echo "file deleted"
	@rm -r $(USERS_PIC)
	@echo "file created"
	@mkdir $(USERS_PIC)

drop:
	@echo "db droped"
	@rm $(DB_NAME)

