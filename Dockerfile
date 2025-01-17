# FROM python:3.11.3 # switch back to this if you need to remove packages
FROM us.gcr.io/pinogy-websites/pinogy-new-base:1023
ENV PYTHONUNBUFFERED=1

EXPOSE 8000
RUN rm -rf /app && mkdir /app
WORKDIR /app

# add credentials on build
ARG SSH_PRIVATE_KEY
ARG IMAGE_NAME
ARG IMAGE_BUILD
RUN mkdir -p /root/.ssh/
RUN echo "${SSH_PRIVATE_KEY}" > /root/.ssh/id_rsa
RUN echo "${IMAGE_NAME}" > /app/IMAGE_NAME.txt
RUN echo "${IMAGE_BUILD}" > /app/IMAGE_BUILD.txt

# make sure your domain is accepted
RUN touch /root/.ssh/known_hosts
#RUN ssh-keyscan bitbucket.org >> /root/.ssh/known_hosts
RUN ssh-keygen -R bitbucket.org && curl https://bitbucket.org/site/ssh >> /root/.ssh/known_hosts
RUN chmod 400 /root/.ssh/id_rsa

RUN git clone --branch shop-development git@bitbucket.org:pinogycorp/pinogy_shop.git

COPY ./requirements/base.txt /app/base.txt
COPY ./requirements/production.txt /app/requirements.txt

RUN set -ex \
    && buildDeps=" \
       build-essential \
       libpq-dev \
       gcc \
    " \
    && deps=" \
       python-dev-is-python3 \
       libpcre3 \
       libpcre3-dev \
       gettext \
       postgresql-client \
    " \
    && apt-get update && apt-get install -y $buildDeps $deps --no-install-recommends \
    && pip install --upgrade pip && pip install -U -r /app/requirements.txt \
    && apt-get purge -y --auto-remove $buildDeps \
       $(! command -v gpg > /dev/null || echo 'gnupg dirmngr') \
    && rm -rf /var/lib/apt/lists/*
    
COPY ./ /app
RUN pip install --upgrade sentry-sdk
CMD mkdir -p ./pinogy_app/static && python manage.py prepare_launch && uwsgi --ini=/app/uwsgi.ini