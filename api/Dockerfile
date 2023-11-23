# Use the base Python image
FROM python:3.9

# Install the required system packages
RUN apt-get update && apt-get install -y \
    gcc \
    libc-dev

# Make /usr/src/app/ directory
RUN mkdir -p /usr/src/app/
#Copy all files
COPY . /usr/src/app/
# Set working directory
WORKDIR /usr/src/app/
RUN ls -la
# Expose the port on which the Flask API will run
EXPOSE 5001

# Install the required Python packages
RUN pip install --no-cache-dir -r requirements.txt

CMD python app.py run -h 0.0.0.0
