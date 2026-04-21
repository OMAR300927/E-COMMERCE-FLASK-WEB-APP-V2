FROM python:3.12-slim

WORKDIR /app

RUN pip install uv

COPY pyproject.toml uv.lock ./
COPY . .

RUN uv sync

EXPOSE 8000

CMD ["uv", "run", "gunicorn", "-w", "3", "-b", "0.0.0.0:8000", "run:app"]