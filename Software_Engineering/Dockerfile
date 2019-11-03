FROM python:3-alpine
RUN apk update --no-cache
RUN apk upgrade --no-cache
ENV PRODUCTION=true
WORKDIR /app
# do the dependencies first since these take awhile to complete and
# don't change as often - utilise the docker build cache (:
COPY requirements.txt /app
RUN pip install --upgrade pip
RUN apk add --no-cache openblas subversion lapack build-base \
  && pip install -r requirements.txt \
  && apk del --no-cache openblas subversion lapack build-base
RUN apk add --no-cache libstdc++
# then copy in the rest of the code to execute
COPY . /app/
EXPOSE 8080
CMD [ "python", "/app/run.py" ]
ENV PYTHONUNBUFFERED 1