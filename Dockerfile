# Use the official Python image
FROM python:3.11-slim 

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /code

# Copy only the Pipfile and Pipfile.lock into the container
COPY Pipfile Pipfile.lock /code/

# Install pipenv
RUN pip install pipenv

# Install dependencies using pipenv
RUN pipenv install --deploy --system

# Copy the current directory contents into the container at /code
COPY . /code/

# Run migrations before starting the server
CMD ["bash", "-c", "python manage.py makemigrations && python manage.py migrate && python manage.py collectstatic --noinput && python manage.py runserver 0.0.0.0:4554"]