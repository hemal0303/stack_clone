FROM python:3.10.9-slim

COPY . /app
WORKDIR /app

RUN python3 -m venv venv /opt/venv

RUN /opt/venv/bin/pip install pip --upgrade && \
    /opt/venv/bin/pip install -r requirements.txt && \
    /opt/venv/bin/pip install 'uvicorn[standard]' && \
    chmod +x entrypoint.sh

CMD ["/app/entrypoint.sh"]