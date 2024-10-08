# Event class

## The CloudEvent class and the pydantic TypeAdapter

The `CloudEvent` class is the core of the system using a Pydantic model.
It is responsible for all the validation and serialization of the canonic
types.

The class has some basic support for `data` which has the `Any` type.
Pydantic will use a best effort approach for the serialization process
and _no validation_.

You will usually use the `CloudEvent` class (or a subclass) it when\
creating an event from your application domain logic.

/// admonition | Use subclasses
    type: tip
It is recommended to create subclasses with your specific data types
so you can better control the serialization rules.
///

You can create an event in different ways:

/// tab | Factory method (recommended)
The class provides a nice factory method that takes care of providing
some default values for required fields.

```python
from cloudevents_pydantic.events import CloudEvent

# `source` and `type` are the minimal needed attributes when using the factory
attributes = {
    "source": "order:service",
    "type": "order.created",
}

my_event = CloudEvent.event_factory(**attributes)
```

The provided defaults are:

* `id`: Uses ULID (a sortable version of UUID)
* `time`: Simple `datetime.now()` in UTC timezone
* `specversion`: Hardcoded `1.0` (the only supported version for now)

/// admonition | Default values and the factory
    type: warning
We don't define defaults in the `CloudEvent` class for the mandatory fields.
In this way we can validate their presence when we receive an event from an
external source.

Do not override the model fields defaults when subclassing the `CloudEvent` class.
Override the `event_factory` as needed.
///

///

/// tab | Class constructor
Use the constructor from the model

```python
from cloudevents_pydantic.events import CloudEvent
import datetime

# Full set of attributes
attributes = {
    "data": {"data-key": "val"},
    "datacontenttype": "application/octet-stream",
    "dataschema": "http://some-dataschema.url",
    "id": "id-can-be-anything",
    "source": "dummy:source",
    "specversion": "1.0",
    "subject": "some-subject",
    "time": datetime.datetime(
            year=2020,
            month=7,
            day=16,
            hour=12,
            minute=3,
            second=20,
            microsecond=519216,
            tzinfo=datetime.timezone(datetime.timedelta(hours=4)),
    ),
    "type": "dummy.type",
}

my_event = CloudEvent(**attributes)
```

/// admonition | Default values and the factory
    type: tip
You can use either `str` values or python objects (see the `time` field)
///
///

## Best practices when creating your event classes

When you create event types in your app you will want to make sure to follow these best practices:

* Use `TypedDict` for structured data instead of nested pydantic models (as specified in
  [Pydantic performance](https://docs.pydantic.dev/latest/concepts/performance/#use-typeddict-over-nested-models)
  documentatin)
* Use the fields types defined in the `cloudevents_pydantic.events.field.types`. These types will
  be kept up to date and make sure their validation, serialization and deserialization rules
  will be compliant with the [CloudEvents spec](https://github.com/cloudevents/spec/tree/main).
* Write your own pydantic `Field` for data
* Use the fields available in the `cloudevents_pydantic.events.field.metadata` when overriding
  the cloudevent fields to inherit CloudEvents field descriptive metadata (i.e. title, description)
  will be populated in the schema.

Example:

```python
from typing import Annotated, Literal, TypedDict

from pydantic import Field

from cloudevents_pydantic.events import CloudEvent
from cloudevents_pydantic.events.fields import metadata, types


class OrderCreatedData(TypedDict):
    a_str: types.String
    an_int: types.Integer


OrderCreatedDataField = Field(
    title="An order representation",
    description="A nice new order has been created! OMG!",
    examples=["{'a_str': 'a nice string', 'an_int': 1}"],
)


class OrderCreated(CloudEvent):
    data: Annotated[OrderCreatedData, OrderCreatedDataField]
    type: Annotated[
        Literal["order_created"], Field(default="order_created"), metadata.FieldType
    ]
    source: Annotated[
        Literal["order_service"], Field(default="order_service"), metadata.FieldSource
    ]
```


/// admonition | Use subclasses
    type: warning
Be careful when overriding attributes for the `CloudEvent` fields, except for `data`,
you'll probably only need to override `type` and `source`.
///
