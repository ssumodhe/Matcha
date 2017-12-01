DB_NAME = Matcha.db

all: drop setup

setup: 
	@echo "db setup"
	@python config/setup_db.py

# seed:
# 	@echo "db seed"
# 	@php config/seed.php

drop:
	@echo "db drop"
	@rm $(DB_NAME)