# pull official base image
FROM python:3.10-slim-bookworm
# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pipenv
COPY Pipfile Pipfile.lock ./
RUN pipenv install --system --deploy

# copy entrypoint.sh
COPY entrypoint.sh ./
RUN sed -i 's/\r$//g' /usr/src/app/entrypoint.sh
RUN chmod +x /usr/src/app/entrypoint.sh

# copy project
COPY . .

# run entrypoint.sh
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]