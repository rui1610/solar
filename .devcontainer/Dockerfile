FROM python:3.10-slim-bullseye AS picrobo

ENV APPNAME=picrobo
ENV HOME_FOLDER=/$APPNAME
WORKDIR $HOME_FOLDER

COPY requirements.txt /tmp/pip-tmp/requirements.txt

RUN apt -y update
RUN apt -y upgrade
RUN apt install -y git && pip install --upgrade pip 
RUN pip install -r /tmp/pip-tmp/requirements.txt && rm -rf /tmp/pip-tmp

COPY *   $HOME_FOLDER/

CMD ["bash"]
