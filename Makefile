include .env

default:
	@make install
	@make setup
	@make serve

serve:
	@make clean
	@python routes.py

setup:
	@make clean
	@sed 's/=s.*//' .env | while read x ; do eval $$x ; done

install:
	@sudo easy_install pip
	@sudo pip install --ignore-installed -r requirements.txt
	@touch .env
	@touch playground.py
	@make setup

clean:
	@find . -name \*.pyc -delete
	@clear