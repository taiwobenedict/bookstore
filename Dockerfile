
#import python Image

FROM python:3.12

# create director
WORKDIR /app

# Initiate virtual environment
RUN python -m venv env

# Copy and install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy all the projects
COPY . .

# Expose to port 8080
EXPOSE 8080

# Run migrations 
RUN python manage.py makemigrations && python manage.py migrate 


# Start app
CMD [ "gunicorn", "-k", "uvicorn.workers.UvicornWorker", "store.asgi:application", "--bind", "0.0.0.0:8080" ]