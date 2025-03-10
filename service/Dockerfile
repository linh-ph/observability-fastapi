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

# Install curl and grpcurl
RUN apt-get update && apt-get install -y curl && \
    apt-get install -y protobuf-compiler && \
    curl -L https://github.com/fullstorydev/grpcurl/releases/download/v1.8.7/grpcurl_1.8.7_linux_x86_64.tar.gz | tar -xz -C /usr/local/bin

# Set environment variables for OpenTelemetry
# ENV OTEL_RESOURCE_ATTRIBUTES=service.name=fastapiApp
# ENV OTEL_EXPORTER_OTLP_ENDPOINT=http://collector:4317
# ENV OTEL_EXPORTER_OTLP_PROTOCOL=grpc

# Init command
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5002", "--reload"]

# Init command
# CMD ["opentelemetry-instrument", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5002"]
