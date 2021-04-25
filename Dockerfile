FROM python:3.9

COPY requirements.txt .
RUN pip install poetry
RUN poetry install
