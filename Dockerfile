FROM python:3.13-slim

EXPOSE 8080

RUN pip install uv
WORKDIR /usr/src/app

COPY ./ /usr/src/app

CMD ["uv", "run", "streamlit", "run", "main.py", "--server.port=8080", "--server.address=0.0.0.0"]
