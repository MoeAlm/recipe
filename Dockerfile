FROM python:3.12.0
LABEL maintainer="moealm"

ENV PYTHONUNBUFFERED 1

# Copy requirements.txt to the working directory
COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt
COPY ./app /app
WORKDIR /app
EXPOSE 8000

ARG DEV=false
# Create a virtual environment and install dependencies
RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    if [ $DEV = "true" ]; then /py/bin/pip install -r /tmp/requirements.dev.txt; fi && \
    rm -rf /tmp && \
    /py/bin/flake8 --version && \
    adduser \
        --disabled-password \
        --no-create-home \
        django-user

# Set the working directory and expose port
WORKDIR /app
EXPOSE 8000

# Add the application code
COPY app /app

# Set the PATH to include the virtual environment
ENV PATH="/py/bin:$PATH"

# Switch to the django-user user
USER django-user
