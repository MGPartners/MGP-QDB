FROM python:3.13-slim

EXPOSE 8080

RUN pip install poetry
WORKDIR /usr/src/app

COPY ./ /usr/src/app
RUN poetry install --no-root

CMD ["poetry", "run", "streamlit", "run", "apps/main.py", "--server.address=0.0.0.0"]
