dev:
	sh ./start.sh 8080
dbuild:
	docker build -t mail-server .
_docker_tag_push:
	docker tag mail-server johndope/mail-server:$(version) && docker push johndope/mail-server:$(version)
dpush:
	make dbuild && make _docker_tag_push version=$(version) && make _docker_tag_push version=latest
heroku_key:
	heroku config:set GMAIL_APP_PASSWORD=`python -c "from dotenv import dotenv_values; print(dotenv_values('.env.local')['GMAIL_APP_PASSWORD'])"`
heroku_init:
	read -p "Heroku repo name: " repo_name && heroku git:remote -a $(repo_name) && make heroku_key
heroku_push:
	git push heroku main:main