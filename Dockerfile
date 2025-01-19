FROM python:3.12-slim

EXPOSE 8080

RUN pip install poetry
WORKDIR /usr/src/app

# Create the .streamlit directory
RUN mkdir -p .streamlit

# Write the secret from the build argument to secrets.toml
ARG STREAMLIT_SECRETS
RUN echo "$STREAMLIT_SECRETS" > .streamlit/secrets.toml

COPY ./ /usr/src/app
RUN poetry install

CMD ["poetry", "run", "streamlit", "run", "main.py", "--server.port=8080", "--server.address=0.0.0.0"]
