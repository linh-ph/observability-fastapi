FROM tiangolo/uvicorn-gunicorn:python3.11

# open port
EXPOSE 5002

WORKDIR /app

# add requirements
COPY ./requirements.txt /requirements.txt

# copy source code
COPY app/ ./

# install requirements
RUN pip install --no-cache-dir -r /requirements.txt

RUN opentelemetry-bootstrap --action=install

# Set environment variables for OpenTelemetry
# ENV OTEL_RESOURCE_ATTRIBUTES=service.name=fastapiApp
# ENV OTEL_EXPORTER_OTLP_ENDPOINT=http://collector:4317
# ENV OTEL_EXPORTER_OTLP_PROTOCOL=grpc

# Init command
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5002"]

# Init command
# CMD ["opentelemetry-instrument", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5002"]
