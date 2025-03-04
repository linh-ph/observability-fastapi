import asyncio
import logging
from fastapi import HTTPException, status, FastAPI
import requests
import random
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


# random.seed(54321)
trace.set_tracer_provider(TracerProvider())
otlp_exporter = OTLPSpanExporter(insecure=True)
# trace.get_tracer_provider().add_span_processor(BatchSpanProcessor(ConsoleSpanExporter()))
trace.get_tracer_provider().add_span_processor(BatchSpanProcessor(otlp_exporter))

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

app = FastAPI()

# Instrument FastAPI with OpenTelemetry
FastAPIInstrumentor.instrument_app(app)

@app.get("/")
async def read_root():
    return {"Hello": "World"}


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
        logger.error(ex, exc_info=True)
        span = trace.get_current_span()
        print("span", span)
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


# @app.get("/log")
# def log():
#     logger_provider = LoggerProvider(
#         resource=Resource.create(
#             {
#                 "service.name": "fastapiApp",
#                 "service.instance.id": "instance-12",
#             }
#         ),
#     )
#     set_logger_provider(logger_provider)

#     exporter = OTLPLogExporter(insecure=True)
#     logger_provider.add_log_record_processor(BatchLogRecordProcessor(exporter))
#     handler = LoggingHandler(level=logging.NOTSET, logger_provider=logger_provider)

#     # Attach OTLP handler to root logger
#     logging.getLogger().addHandler(handler)

#     # Create different namespaced loggers
#     # It is recommended to not use the root logger with OTLP handler
#     # so telemetry is collected only for the application
#     logger1 = logging.getLogger("myapp.area1")
#     logger2 = logging.getLogger("myapp.area2")

#     logger1.debug("Quick zephyrs blow, vexing daft Jim.")
#     logger1.info("How quickly daft jumping zebras vex.")
#     logger2.warning("Jail zesty vixen who grabbed pay from quack.")
#     logger2.error("The five boxing wizards jump quickly.")


#     # Trace context correlation
#     tracer = trace.get_tracer(__name__)
#     with tracer.start_as_current_span("foo"):
#         # Do something
#         logger2.error("Hyderabad, we have a major problem.")

#     logger_provider.shutdown()
#     return "ok"
