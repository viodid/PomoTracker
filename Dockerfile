# Use an official Python image as the base
FROM python:3.11-bullseye

# Set environment variables for Python
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Create and set the working directory
WORKDIR /app

# Copy and install Python dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . /app/

# Collect static files
RUN python manage.py collectstatic --noinput

# Migrate the database
RUN python manage.py migrate

# Install NGINX
RUN apt-get update && apt-get install -y nginx

# Remove default NGINX configuration
RUN rm /etc/nginx/sites-enabled/default

# Create the Nginx log folder
RUN mkdir -p /var/log/nginx/pomotracker && \
    touch /var/log/nginx/pomotracker/access.log && \
    touch /var/log/nginx/pomotracker/error.log

# Copy the custom NGINX configuration
COPY config/nginx/nginx.conf /etc/nginx/sites-enabled/

# Change default user NGINX conf
RUN sed -i 's/user www-data;/user root;/' /etc/nginx/nginx.conf

# Expose port for NGINX
EXPOSE 80

# Start Gunicorn and NGINX in the foreground
CMD gunicorn PomoTracker.wsgi:application --bind 0.0.0.0:8000 && nginx -g "daemon off;"