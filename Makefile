include .env

default:
	@make install
	@make setup

setup:
	@make clean
	@sed 's/=s.*//' .env | while read x ; do eval $$x ; done

install:
	@sudo easy_install pip
	@sudo pip install --ignore-installed -r requirements.txt
	@touch .env
	@make setup