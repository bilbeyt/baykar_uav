FROM python:3.12-alpine

RUN mkdir /src
COPY av_builder /src

WORKDIR /src

RUN apk add --no-cache postgresql-libs poetry && \
    apk add --no-cache --virtual .build-deps gcc postgresql-dev musl-dev python3-dev && \
    poetry install --no-root && \
    apk --purge del .build-deps

ENV POSTGRES_HOST=db

ENTRYPOINT [ "./startup.sh" ]