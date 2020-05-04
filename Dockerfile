FROM python:3.9-rc-alpine3.11
LABEL maintainer="Jason LI"

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt
RUN apk add --update --no-cache postgresql-client jpeg-dev
RUN apk add --update --no-cache --virtual .tmp-build-deps \
    gcc libc-dev linux-headers postgresql-dev python3-dev musl-dev zlib zlib-dev && \
    pip install --upgrade pip && \
    pip install -r /requirements.txt
    # apk del .tmp-build-deps

RUN mkdir /app
WORKDIR /app
COPY ./app /app

# RUN mkdir -p /vol/web/media
# RUN mkdir -p /vol/web/static
RUN adduser -D user
# RUN chown -R user:user /vol/
# RUN chmod -R 755 /vol/web
USER user
