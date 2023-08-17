FROM python:3.10-slim-bullseye

# Set the working directory
WORKDIR /app

# Copy the project files to the container
COPY . .

# Install the package using setup.py
RUN pip install -e .

# Install dependencies
RUN pip install pip -U && \
    pip install --no-cache-dir -r requirements.txt

# Set the environment variable
ARG OPENAI_API_KEY
ENV OPENAI_API_KEY=$OPENAI_API_KEY

# Expose the necessary ports
EXPOSE 8000

# Run the application
# CMD ["uvicorn", "agents.main:app", "--host", "0.0.0.0", "--port", "8000"]
