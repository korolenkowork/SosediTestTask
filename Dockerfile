FROM ghcr.io/astral-sh/uv:bookworm AS builder

# Environment variables
ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_PYTHON_INSTALL_DIR=/python \
    UV_PYTHON_PREFERENCE=only-managed \
    PYTHONUNBUFFERED=1 \
    PATH="/app/.venv/bin:$PATH"

# Install desired Python version
RUN uv python install 3.13

# Set working directory
WORKDIR /app

# Copy only what’s needed first for better cache performance
COPY pyproject.toml ./pyproject.toml
COPY uv.lock ./uv.lock

# Install prod dependencies
RUN uv sync --frozen --no-dev

# Copy full project files
COPY . .

# Ensure install script is executable
RUN chmod +x install.sh

# Expose Django port
EXPOSE 8000

# Entrypoint to run the install script (could start server, migrations, etc.)
ENTRYPOINT ["sh", "install.sh"]
