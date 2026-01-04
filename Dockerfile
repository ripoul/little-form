FROM python:3.13-slim-trixie
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
RUN mkdir /app
WORKDIR /app
COPY pyproject.toml uv.lock /app/
COPY little_form /app/little_form
RUN uv sync --extra prod
EXPOSE 8000
WORKDIR /app/little_form
CMD ["uv", "run", "gunicorn", "-b", "0.0.0.0:8000", "app:create_app()"]

