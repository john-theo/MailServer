FROM python:3.9-slim
LABEL maintainer="John Dope (zhuangxh.cn@gmail.com)"

ENV GMAIL_USERNAME="example@gmail.com"
ENV SENDER_NAME="Example Corp"

COPY . /app
WORKDIR /app

RUN pip install -r requirements.txt

CMD ["sh", "./start.sh", "8080"]