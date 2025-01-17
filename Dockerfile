FROM python:3.12-slim

EXPOSE 8080

RUN pip install poetry
WORKDIR /usr/src/app

COPY ./ /usr/src/app
RUN poetry install

CMD ["poetry", "run", "streamlit", "run", "main.py", "--server.port=8080", "--server.address=0.0.0.0"]
