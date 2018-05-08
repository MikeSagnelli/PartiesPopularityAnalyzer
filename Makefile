default:
	@make install
	@make serve

serve:
	@make clean
	@python routes.py

install:
	@sudo easy_install pip
	@sudo pip install --ignore-installed -r requirements.txt
	@touch .env
	@touch playground.py
	@make setup

clean:
	@find . -name \*.pyc -delete
	@clear