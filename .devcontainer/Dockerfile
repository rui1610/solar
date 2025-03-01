FROM python:3.10-slim-bullseye AS picrobo

ENV APPNAME=picrobo
ENV HOME_FOLDER=/$APPNAME
WORKDIR $HOME_FOLDER

COPY requirements.txt /tmp/pip-tmp/requirements.txt

RUN apt -y update
RUN apt -y upgrade
RUN apt install -y git && pip install --upgrade pip 
RUN pip install -r /tmp/pip-tmp/requirements.txt && rm -rf /tmp/pip-tmp

ENV NODE_VERSION=20.11.1
RUN apt install -y curl
RUN curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
ENV NVM_DIR=/root/.nvm
RUN . "$NVM_DIR/nvm.sh" && nvm install ${NODE_VERSION}
RUN . "$NVM_DIR/nvm.sh" && nvm use v${NODE_VERSION}
RUN . "$NVM_DIR/nvm.sh" && nvm alias default v${NODE_VERSION}
ENV PATH="/root/.nvm/versions/node/v${NODE_VERSION}/bin/:${PATH}"
RUN node --version
RUN npm --version
RUN npm install -g npm@10.8.1
#RUN npm i -g yo generator-easy-ui5

COPY *   $HOME_FOLDER/

CMD ["bash"]
