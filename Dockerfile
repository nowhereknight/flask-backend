FROM python:3.6-alpine

ENV FLASK_APP flasky.py
ENV FLASK_CONFIG development
ENV DATABASE_USER <DATABASE_USER>
ENV DATABASE_PWD <DATABASE_PWD>
ENV DATABASE_HOST <DATABASE_HOST>
ENV DATABASE_NAME <DATABASE_NAME>

RUN adduser -D flasky
USER flasky

WORKDIR /home/flasky

COPY requirements requirements
RUN python -m venv venv
RUN venv/bin/pip install -r requirements/docker.txt

COPY app app
COPY migrations migrations
COPY flasky.py config.py boot.sh ./

# run-time configuration
EXPOSE 5000
ENTRYPOINT ["./boot.sh"]
