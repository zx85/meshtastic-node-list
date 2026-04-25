FROM ghcr.io/astral-sh/uv:alpine
WORKDIR /app

# Copy application
COPY . .

# Install Python dependencies
RUN uv sync

# Set environment variables
ENV FLASK_APP=app.py
ENV FLASK_ENV=development
# ENV FLASK_ENV=production

EXPOSE 5000
CMD ["uv", "run", "python", "app.py"]   
