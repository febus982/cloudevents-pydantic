from benchmark import eventfrom benchmark import http_handler

# HTTP binding

Using the HTTP binding handler is straightforward. Just remember to reuse the same
`HTTPHandler` multiple times.

/// tab | ✅ Good

```python
from cloudevents_pydantic.events import CloudEvent
from cloudevents_pydantic.bindings.http import HTTPHandler

class OrderCreated(CloudEvent):
    ...

http_handler = HTTPHandler(OrderCreated)

def do_something():
    http_handler.from_json("json_body")
```
///

/// tab | ❌ Bad
```python
from cloudevents_pydantic.events import CloudEvent
from cloudevents_pydantic.bindings.http import HTTPHandler

class OrderCreated(CloudEvent):
    ...

def do_something():
    http_handler = HTTPHandler(OrderCreated)
    http_handler.from_json("json_body")
```

///

/// admonition | Why you have to reuse the same object?
    type: tip

When the HTTPHandler instance is created it creates internally a Pydantic `TypeAdapter`
for the event class, to handle efficiently event batches. This is an expensive operation.
Check the [Pydantic documentation](https://docs.pydantic.dev/latest/concepts/performance/#typeadapter-instantiated-once)
about this.
///

## Serialize a JSON event

HTTP serialization returns header and body to be used in a HTTP request.

/// tab | Custom Event class
```python
from cloudevents_pydantic.events import CloudEvent
from cloudevents_pydantic.bindings.http import HTTPHandler

class OrderCreated(CloudEvent):
    ...

minimal_attributes = {
    "type": "order_created",
    "source": "https://example.com/event-producer",
    "id": "b96267e2-87be-4f7a-b87c-82f64360d954",
    "specversion": "1.0",
}

http_handler = HTTPHandler(OrderCreated)
event = OrderCreated.event_factory(**minimal_attributes)

# Single event
headers, body = http_handler.to_json(event)
# Batch (list) of events
headers, body = http_handler.to_json_batch([event])
```
///

/// tab | CloudEvent class
```python
from cloudevents_pydantic.events import CloudEvent
from cloudevents_pydantic.bindings.http import HTTPHandler

minimal_attributes = {
    "type": "order_created",
    "source": "https://example.com/event-producer",
    "id": "b96267e2-87be-4f7a-b87c-82f64360d954",
    "specversion": "1.0",
}

http_handler = HTTPHandler()
event = CloudEvent.event_factory(**minimal_attributes)

# Single event
json_string = http_handler.to_json(event)
# Batch (list) of events
json_batch_string = http_handler.to_json_batch([event])
```
///

## Deserialize a JSON event

HTTP deserialization parses the body to reconstruct the event.

/// tab | Custom Event class
```python
from cloudevents_pydantic.events import CloudEvent
from cloudevents_pydantic.bindings.http import HTTPHandler

class OrderCreated(CloudEvent):
    ...

single_event_json = '{"data":null,"source":"https://example.com/event-producer","id":"b96267e2-87be-4f7a-b87c-82f64360d954","type":"com.example.string","specversion":"1.0","time":"2022-07-16T12:03:20.519216+04:00","subject":null,"datacontenttype":null,"dataschema":null}'
batch_event_json = '[{"data":null,"source":"https://example.com/event-producer","id":"b96267e2-87be-4f7a-b87c-82f64360d954","type":"com.example.string","specversion":"1.0","time":"2022-07-16T12:03:20.519216+04:00","subject":null,"datacontenttype":null,"dataschema":null}]'

http_handler = HTTPHandler(OrderCreated)

# Single event
event = http_handler.from_json(single_event_json)
# Batch (list) of events
batch_of_events = http_handler.from_json_batch(batch_event_json)
```
///

/// tab | CloudEvent class
```python
from cloudevents_pydantic.events import CloudEvent
from cloudevents_pydantic.bindings.http import HTTPHandler

minimal_attributes = {
    "type": "order_created",
    "source": "https://example.com/event-producer",
    "id": "b96267e2-87be-4f7a-b87c-82f64360d954",
    "specversion": "1.0",
}

http_handler = HTTPHandler()
event = CloudEvent.event_factory(**minimal_attributes)

# Single event
event = http_handler.to_json(event)
# Batch (list) of events
batch_of_events = http_handler.to_json_batch([event])
```
///
