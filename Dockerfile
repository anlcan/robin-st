# Use an official Python runtime as a parent image
FROM python:3.12-slim as base

# Set the working directory in the container to /app
WORKDIR /app


# Add the requirements file to the container
ADD requirements-server.txt /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements-server.txt

FROM python:3.12-slim
COPY --from=base /usr/local /usr/local

# Copy the current directory contents into the container at /app
COPY . /app

# Make port 8000 available to the world outside this container
EXPOSE 8000
WORKDIR /app

# Run server.py when the container launches
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8000"]
