FROM python:3.10-slim

WORKDIR /app

# Add logging for better debugging
RUN echo "Starting build process for MCP server..." && \
    echo "Python version:" && python --version && \
    echo "Installed packages:" && pip list

# Install uv
RUN pip install --no-cache-dir uv

# Copy requirements first to leverage Docker caching
COPY requirements.txt .
COPY pyproject.toml .

# Use uv to install dependencies
RUN uv pip install  --system -r requirements.txt

# Copy server implementation
COPY mcp_server.py .
COPY .env.sh .

# Set executable permissions
RUN chmod +x .env.sh

# Default port for SSE transport
EXPOSE 8000

# Default to SSE transport
ENV TRANSPORT=sse

# Set the entrypoint
ENTRYPOINT ["/bin/bash", "-c", "source .env.sh && python mcp_server.py --transport=$TRANSPORT"]