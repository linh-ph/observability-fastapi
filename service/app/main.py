import asyncio
import logging
import requests
import random
import json

from fastapi import HTTPException, status, FastAPI
from opentelemetry import trace
from opentelemetry.trace.status import Status, StatusCode
from opentelemetry._logs import set_logger_provider
from opentelemetry.exporter.otlp.proto.grpc._log_exporter import (
    OTLPLogExporter,
)
from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (
    BatchSpanProcessor,
    ConsoleSpanExporter,
)
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from db import ClickHouseLogManager

tracer_provider = TracerProvider(
    resource=Resource.create(
        {
            "service.name": "app_demo",
            # "service.instance.id": "instance-12",
        }
    ),
)
otlp_exporter = OTLPSpanExporter(endpoint="collector:4317", insecure=True)
# trace.get_tracer_provider().add_span_processor(BatchSpanProcessor(ConsoleSpanExporter()))
tracer_provider.add_span_processor(BatchSpanProcessor(otlp_exporter))
trace.set_tracer_provider(tracer_provider)

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
# set_logger_provider(logger_provider)
set_logger_provider(logger_provider)

handler = LoggingHandler(level=logging.NOTSET, logger_provider=logger_provider)
print("handler", handler)

# # Set up logging
logger = logging.getLogger(__name__)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

app = FastAPI()

# Instrument FastAPI with OpenTelemetry
FastAPIInstrumentor.instrument_app(app)

# Endpoint đơn giản
tracer = trace.get_tracer(__name__)
with tracer.start_as_current_span("parent"):
    print("trace", tracer)
    print("Hello, World!")

@app.get("/")
async def read_root():
    # span = trace.get_tracer(__name__).start_span("root_span")
    span = trace.get_current_span()
    print("span", span)
    span.end()
    return {"message": "Hello 1111"}


@app.get("/ping")
async def health_check():
    return "pong"


@app.get("/items/{item_id}")
async def read_item(item_id: int, q: str = None):
    if item_id % 2 == 0:
        # mock io - wait for x seconds
        seconds = random.uniform(0, 3)
        await asyncio.sleep(seconds)
    return {"item_id": item_id, "q": q}


@app.get("/invalid")
async def invalid():
    raise ValueError("Invalid ")

@app.get("/exception")
async def exception():
    try:
        raise ValueError("sadness")
    except Exception as ex:
        span = trace.get_current_span()
        # generate random number
        seconds = random.uniform(0, 30)

        # record_exception converts the exception into a span event. 
        exception = IOError("Failed at " + str(seconds))
        span.record_exception(exception)
        span.set_attributes({'est': True})
        # Update the span status to failed.
        span.set_status(Status(StatusCode.ERROR, "internal error"))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Got sadness")

@app.get("/external-api")
def external_api():
    seconds = random.uniform(0, 3)
    response = requests.get(f"https://httpbin.org/delay/{seconds}")
    response.close()
    return "ok"



@app.get("/log")
def log():
    data = {
        "url": "https://example.com",
        "module": "Xtrend",
        "kind_of": "collection",
        "message": "Collect message"
    }
    logger.info(json.dumps(data))
    err = {
        "url": "https://example.com",
        "module": "Xtrend",
        "kind_of": "collection",
        "message": "Collect message"
    }
    logger.error(json.dumps(err))
    return "ok"

log_manager = ClickHouseLogManager()

@app.get("/create_table")
def create_table():
    log_manager.create_log_table()
    return "ok"

@app.get("/create_log")
def create_log():
    log_manager.insert_log_entry('ERROR', 'Error message', 'https://example.com', 'Xtrend', 'collection')
    return "ok"

@app.get("/logs")
def logs():
    log_manager.read_log_entries()
    return "ok"