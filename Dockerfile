FROM python:3.10-slim

COPY ["requirements.txt","/usr/code/"]

WORKDIR /usr/code/

RUN pip install --no-cache-dir --upgrade -r /usr/code/requirements.txt

EXPOSE 8000

COPY [".", "/usr/code/"]