# Use an NVIDIA CUDA base image to ensure GPU support for the AI model
# The specific version should be chosen based on the model's requirements.
# Using 12.1.1 as a robust, recent choice.
FROM nvidia/cuda:12.1.1-runtime-ubuntu22.04

# Set up a non-root user and working directory
WORKDIR /app
RUN groupadd -r appuser && useradd -r -g appuser appuser
COPY . /app
RUN chown -R appuser:appuser /app
USER appuser

# Install Python and pip
RUN apt-get update && \
    apt-get install -y python3 python3-pip && \
    rm -rf /var/lib/apt/lists/*

# Copy application code
COPY . .

# Install Python dependencies
# This step can be very long due to the AI model's dependencies (PyTorch, etc.)
RUN python3 -m pip install --no-cache-dir -r requirements.txt

# Expose the port the app will run on
EXPOSE 5008

# Define the command to run the application
CMD ["gunicorn", "--bind", "0.0.0.0:5008", "app:app"]
