from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter


# Service name is required for most backends
resource = Resource(attributes={
    SERVICE_NAME: "logger-service"
})

# create a tracer provider
tracer_provider = TracerProvider(resource=resource)

# create an OTLP trace exporter
url = 'http://localhost:5080/api/default/v1/traces'
headers = {
    "Authorization": "Basic YWRtaW5AYWRtaW4uY29tOkpVbTI4Tnl5UkkxR0M4RlY="}

exporter = OTLPSpanExporter(endpoint=url, headers=headers)

# create a span processor to send spans to the exporter
span_processor = BatchSpanProcessor(exporter)

# add the span processor to the tracer provider
tracer_provider.add_span_processor(span_processor)

# set the tracer provider as the global provider
trace.set_tracer_provider(tracer_provider)