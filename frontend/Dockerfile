# Pull base image
FROM python:3.8.3-alpine

# Set work directory
WORKDIR /usr/src/frontend

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install psycopg2 dependencies
RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev

# Install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# copy entrypoint.sh
COPY ./entrypoint.sh .

# Copy project
COPY . .

# run entrypoint.sh
ENTRYPOINT ["/usr/src/frontend/entrypoint.sh"]