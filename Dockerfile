FROM python:3.9-slim
LABEL maintainer="John Dope (zhuangxh.cn@gmail.com)"

COPY . /app
WORKDIR /app

RUN pip install -r requirements.txt

CMD ["sh", "./start.sh", "8080"]