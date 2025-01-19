FROM python:3.12-slim

RUN pip install poetry
WORKDIR /usr/src/app
COPY ./ /usr/src/app
RUN poetry install

CMD ["poetry", "run", "streamlit", "run", "main.py"]
