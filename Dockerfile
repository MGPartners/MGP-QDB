FROM python:3.12-slim

EXPOSE 8080
RUN pip install poetry

WORKDIR /usr/src/app
COPY ./ /usr/src/app

RUN apt-get update && apt-get install -y wget gnupg
RUN wget -qO - https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key add -
RUN echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] http://packages.cloud.google.com/apt cloud-sdk main" | tee -a /etc/apt/sources.list.d/google-cloud-sdk.list
RUN apt-get update && apt-get install -y google-cloud-sdk


RUN poetry install
RUN mkdir -p .streamlit

RUN echo "$(gcloud secrets versions access latest --secret=streamlit_oauth2_secrets)" > .streamlit/secrets.toml


CMD ["poetry", "run", "streamlit", "run", "main.py", "--server.port=8080", "--server.address=0.0.0.0"]
