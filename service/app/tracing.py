import logging
from fastapi import FastAPI

from opentelemetry._logs import set_logger_provider, set_default_logger_provider
from opentelemetry.exporter.otlp.proto.grpc._log_exporter import (
    OTLPLogExporter,
)
from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
from opentelemetry.sdk.resources import Resource

from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

########## LOGGING ##########
# Create a logger provider
logger_provider = LoggerProvider(
    resource=Resource.create(
        {
            "service.name": "app_demo",
            # "service.instance.id": "instance-12",
        }
    ),
)

# Cấu hình logs provider cho logs
logger_provider.add_log_record_processor(
    BatchLogRecordProcessor(OTLPLogExporter(endpoint="collector:4317", insecure=True))
)
set_default_logger_provider(logger_provider)

handler = LoggingHandler(level=logging.DEBUG, logger_provider=logger_provider)

# # Set up logging
logger = logging.getLogger(__name__)
logger.addHandler(handler)

app = FastAPI()

# Instrument FastAPI with OpenTelemetry
FastAPIInstrumentor.instrument_app(app)


@app.get("/log")
def log():
    logger.info("infoinfoinfoinfo")
    # logger_provider.shutdown()
    return "ok"
