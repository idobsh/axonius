FROM python:3

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl wget gnupg libnss3 libnspr4 libatk1.0-0 \
    libatk-bridge2.0-0 libxcomposite1 libxdamage1 \
    libxfixes3 libxrandr2 libgbm1 libxkbcommon0 \
    libasound2 libatspi2.0-0 libdbus-1-3 \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /axonius

# Copy all project files
COPY . .

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip install playwright

# Install Playwright browsers
RUN playwright install --with-deps

# Run in unbuffered mode
ENV PYTHONUNBUFFERED=1

# Default command
CMD ["pytest", "-s"]
