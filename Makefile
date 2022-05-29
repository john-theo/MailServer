dev:
	sh ./start.sh $PORT
heroku:
	git push heroku master:main
heroku_key:
	heroku config:set GMAIL_APP_PASSWORD=`python -c "from dotenv import dotenv_values; print(dotenv_values('.env.local')['GMAIL_APP_PASSWORD'])"`
docker:
	docker run --rm -it -p 8080:8080 -e "GMAIL_USERNAME=example@gmail.com" -e "SENDER_NAME=Example Corp" -v $(pwd)/.env.local:/app/.env.local gmail_server
