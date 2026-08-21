FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /workspace

COPY requirements.txt ./requirements.txt

RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

COPY conformance_platform ./conformance_platform
COPY architecture-rules ./architecture-rules
COPY apps ./apps

EXPOSE 8000

CMD ["python", "-m", "uvicorn", "conformance_platform.api.main:app", "--host", "0.0.0.0", "--port", "8000"]