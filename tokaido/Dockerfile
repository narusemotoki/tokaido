FROM python:3.6.3

ENV APPDIR /srv
WORKDIR ${APPDIR}

COPY . ${APPDIR}
RUN pip3 install -U pip setuptools
RUN python3 setup.py install

EXPOSE 8080

ENTRYPOINT /srv/run.sh
