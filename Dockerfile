FROM python:3.10.11-slim

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY app app
COPY alembic alembic
COPY alembic.ini boot.sh ./
RUN chmod a+x boot.sh
COPY .env .env

ENTRYPOINT [ "./boot.sh" ]