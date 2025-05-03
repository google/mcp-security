FROM python:3.11-slim

WORKDIR /app

COPY . /app

RUN pip install .

CMD ["python", "-m", "secops_soar_mcp.server"]
