FROM jenkins/jenkins:lts-jdk11

USER root

# Установка Docker CLI
RUN apt-get update && \
  apt-get install -y apt-transport-https ca-certificates curl gnupg2 software-properties-common && \
  curl -fsSL https://download.docker.com/linux/debian/gpg | apt-key add - && \
  add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/debian $(lsb_release -cs) stable" && \
  apt-get update && \
  apt-get install -y docker-ce-cli && \
  apt-get install docker-compose -y

RUN docker --version

# Установка плагинов Jenkins
COPY plugins.txt /usr/share/jenkins/ref/plugins.txt
RUN jenkins-plugin-cli --plugin-file /usr/share/jenkins/ref/plugins.txt