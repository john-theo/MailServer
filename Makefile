dev:
	sh ./start.sh 8080
docker_build:
	docker build -t gmail-server .
docker_tag_push:
	docker tag gserver johndope/gmail-server:$(version) && docker push johndope/gmail-server:$(version)
docker_push:
	make docker_build && make docker_tag_push version=$(version) && make docker_tag_push version=latest
heroku_key:
	heroku config:set GMAIL_APP_PASSWORD=`python -c "from dotenv import dotenv_values; print(dotenv_values('.env.local')['GMAIL_APP_PASSWORD'])"`
heroku_init:
	read -p "Heroku repo name: " repo_name && heroku git:remote -a $(repo_name) && make heroku_key
heroku_push:
	git push heroku main:main