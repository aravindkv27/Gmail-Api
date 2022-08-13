FROM python:3.11.0a4-slim-buster

RUN python3 -m venv /opt/venv

COPY  requirements.txt .

RUN /opt/venv/bin/pip install -r requirements.txt

ADD . ./app

WORKDIR /app

COPY . .

# RUN pip3 install --upgrade pip --user

CMD [ "/opt/venv/bin/python", "main.py" ]