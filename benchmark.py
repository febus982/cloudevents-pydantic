# ==============================================================================
#  Copyright (c) 2024 Federico Busetti                                         =
#  <729029+febus982@users.noreply.github.com>                                  =
#                                                                              =
#  Permission is hereby granted, free of charge, to any person obtaining a     =
#  copy of this software and associated documentation files (the "Software"),  =
#  to deal in the Software without restriction, including without limitation   =
#  the rights to use, copy, modify, merge, publish, distribute, sublicense,    =
#  and/or sell copies of the Software, and to permit persons to whom the       =
#  Software is furnished to do so, subject to the following conditions:        =
#                                                                              =
#  The above copyright notice and this permission notice shall be included in  =
#  all copies or substantial portions of the Software.                         =
#                                                                              =
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR  =
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,    =
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL     =
#  THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER  =
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING     =
#  FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER         =
#  DEALINGS IN THE SOFTWARE.                                                   =
# ==============================================================================
import base64
import json
from timeit import timeit

from cloudevents.conversion import to_json
from cloudevents.http import (
    CloudEvent as HTTPOfficialCloudEvent,
)
from cloudevents.http import (
    from_json as from_json_http,
)
from cloudevents.pydantic import (
    CloudEvent as PydanticOfficialCloudEvent,
)
from cloudevents.pydantic import (
    from_json as from_json_pydantic,
)
from pydantic import Field

from cloudevents_pydantic.bindings.http import HTTPHandler
from cloudevents_pydantic.events import CloudEvent
from cloudevents_pydantic.events.fields.types import Binary

valid_json = '{"data_base64":"dGVzdA==","source":"https://example.com/event-producer","id":"b96267e2-87be-4f7a-b87c-82f64360d954","type":"com.example.string","specversion":"1.0","time":"2022-07-16T12:03:20.519216+04:00","subject":null,"datacontenttype":null,"dataschema":null}'
test_iterations = 1000000


class BinaryEvent(CloudEvent):
    data: Binary = Field(Binary, alias="data_base64")


def json_deserialization():
    CloudEvent.model_validate_json(valid_json)


def json_deserialization_official_sdk_pydantic():
    from_json_pydantic(valid_json)


def json_deserialization_official_sdk_cloudevent():
    from_json_http(valid_json)


print("==== 1M iterations benchmark ====")
print("Timings for HTTP JSON deserialization:")
print("This package: " + str(timeit(json_deserialization, number=test_iterations)))
print(
    "Official SDK using pydantic model: "
    + str(timeit(json_deserialization_official_sdk_pydantic, number=test_iterations))
)
print(
    "Official SDK using http model: "
    + str(timeit(json_deserialization_official_sdk_cloudevent, number=test_iterations))
)

attributes = json.loads(valid_json)
data = base64.b64decode(attributes["data_base64"])
del attributes["data_base64"]
event = CloudEvent(**attributes, data=data)
http_handler = HTTPHandler()
official_pydantic_event = PydanticOfficialCloudEvent.create(
    attributes=attributes, data=data
)
official_http_event = HTTPOfficialCloudEvent.create(attributes=attributes, data=data)


def json_serialization():
    http_handler.to_json(event)


def json_serialization_official_sdk_pydantic():
    to_json(official_pydantic_event)


def json_serialization_official_sdk_cloudevent():
    to_json(official_http_event)


print("")
print("Timings for HTTP JSON serialization:")
print("This package: " + str(timeit(json_serialization, number=test_iterations)))
print(
    "Official SDK using pydantic model: "
    + str(timeit(json_serialization_official_sdk_pydantic, number=test_iterations))
)
print(
    "Official SDK using http model: "
    + str(timeit(json_serialization_official_sdk_cloudevent, number=test_iterations))
)
