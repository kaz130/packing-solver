FROM python:3.9

COPY pyproject.toml poetry.lock .
RUN pip install poetry
RUN poetry install
CMD ["poetry", "run", "uvicorn", "packsolver.main:app", "--host", "0.0.0.0", "--port", "80"]
