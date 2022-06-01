dev:
	sh ./start.sh 8080
dbuild:
	docker build -t mail-server .
_docker_tag_push:
	docker tag mail-server johndope/mail-server:$(version) && docker push johndope/mail-server:$(version)
dpush:
	make dbuild && make _docker_tag_push version=$(version) && make _docker_tag_push version=latest
hkey:
	read -p "Password: " -s password && heroku config:set "PASSWORD=${password}"
hinit:
	read -p "Heroku repo name: " repo_name && heroku git:remote -a $(repo_name) && make hkey
hpush:
	git push heroku main:main