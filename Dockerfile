FROM python:3

# Install required system packages
RUN apt-get update && apt-get install -y wget gnupg curl && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /axonius

# Copy everything into the container
COPY . .

# Install Python dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# Install Playwright and its dependencies
RUN pip install playwright
RUN playwright install --with-deps

# Set environment variable to enforce headless mode
ENV PYTHONUNBUFFERED=1 \
    PLAYWRIGHT_BROWSERS_PATH=0 \
    DISPLAY=:99

# Default command
CMD ["pytest"]
