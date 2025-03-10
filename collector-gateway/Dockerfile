FROM otel/opentelemetry-collector-contrib:latest

# Copy your configuration file into the container
COPY config.yaml /etc/otelcol-contrib/config.yaml

# Set the entrypoint to run the Collector with your configuration
ENTRYPOINT ["/otelcol-contrib", "--config=/etc/otelcol-contrib/config.yaml"]

# Define a health check
HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
  CMD curl -f http://localhost:13133/ || exit 1