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
import datetime
import json
from pathlib import Path
from typing import Any, Dict, Sequence
from urllib.parse import ParseResult

import pytest
from jsonschema import validate
from pydantic import TypeAdapter, ValidationError
from typing_extensions import TypedDict

from cloudevents_pydantic.events import CloudEvent
from cloudevents_pydantic.events.field_types import Binary, SpecVersion
from cloudevents_pydantic.formats.json import (
    from_json,
    from_json_batch,
    to_json,
    to_json_batch,
)

minimal_attributes = {
    "type": "com.example.string",
    "source": "https://example.com/event-producer",
    "id": "b96267e2-87be-4f7a-b87c-82f64360d954",
    "specversion": "1.0",
}
test_attributes: Dict[str, Any] = {
    "type": "com.example.string",
    "source": "https://example.com/event-producer",
    "id": "b96267e2-87be-4f7a-b87c-82f64360d954",
    "specversion": "1.0",
    "time": "2022-07-16T12:03:20.519216+04:00",
}
valid_json = '{"data":null,"source":"https://example.com/event-producer","id":"b96267e2-87be-4f7a-b87c-82f64360d954","type":"com.example.string","specversion":"1.0","time":"2022-07-16T12:03:20.519216+04:00","subject":null,"datacontenttype":null,"dataschema":null}'
valid_json_batch = f"[{valid_json}]"


with open(
    Path(__file__).parent.joinpath("cloudevents_jsonschema_1.0.2.json"),
    "r",
) as f:
    cloudevent_schema = json.load(f)


def test_from_json():
    event = from_json(valid_json)

    assert event.type == "com.example.string"
    assert event.source == ParseResult(
        scheme="https",
        netloc="example.com",
        path="/event-producer",
        params="",
        query="",
        fragment="",
    )
    assert event.data is None
    assert event.id == "b96267e2-87be-4f7a-b87c-82f64360d954"
    assert event.specversion is SpecVersion.v1_0
    assert event.time == datetime.datetime(
        year=2022,
        month=7,
        day=16,
        hour=12,
        minute=3,
        second=20,
        microsecond=519216,
        tzinfo=datetime.timezone(datetime.timedelta(hours=4)),
    )
    assert event.subject is None
    assert event.datacontenttype is None
    assert event.dataschema is None


@pytest.mark.parametrize(
    ["json_input"],
    (
        pytest.param(
            json.dumps(
                {
                    "type": None,
                    "source": "https://example.com/event-producer",
                    "id": "b96267e2-87be-4f7a-b87c-82f64360d954",
                    "specversion": "1.0",
                }
            ),
            id="null_type",
        ),
        pytest.param(
            json.dumps(
                {
                    "source": "https://example.com/event-producer",
                    "id": "b96267e2-87be-4f7a-b87c-82f64360d954",
                    "specversion": "1.0",
                }
            ),
            id="missing_type",
        ),
        pytest.param(
            json.dumps(
                {
                    "type": "com.example.string",
                    "source": None,
                    "id": "b96267e2-87be-4f7a-b87c-82f64360d954",
                    "specversion": "1.0",
                }
            ),
            id="null_source",
        ),
        pytest.param(
            json.dumps(
                {
                    "type": "com.example.string",
                    "id": "b96267e2-87be-4f7a-b87c-82f64360d954",
                    "specversion": "1.0",
                }
            ),
            id="missing_source",
        ),
        pytest.param(
            json.dumps(
                {
                    "type": "com.example.string",
                    "source": "https://example.com/event-producer",
                    "id": None,
                    "specversion": "1.0",
                }
            ),
            id="null_id",
        ),
        pytest.param(
            json.dumps(
                {
                    "type": "com.example.string",
                    "source": "https://example.com/event-producer",
                    "specversion": "1.0",
                }
            ),
            id="missing_id",
        ),
        pytest.param(
            json.dumps(
                {
                    "type": "com.example.string",
                    "source": "https://example.com/event-producer",
                    "id": "b96267e2-87be-4f7a-b87c-82f64360d954",
                    "specversion": None,
                }
            ),
            id="null_specversion",
        ),
        pytest.param(
            json.dumps(
                {
                    "type": "com.example.string",
                    "source": "https://example.com/event-producer",
                    "id": "b96267e2-87be-4f7a-b87c-82f64360d954",
                }
            ),
            id="missing_specversion",
        ),
    ),
)
def test_from_json_and_from_json_batch_fail_if_mandatory_field_null_or_missing(
    json_input,
):
    with pytest.raises(ValidationError):
        from_json(json_input)

    with pytest.raises(ValidationError):
        from_json_batch(json_input)


def test_from_json_and_from_json_batch_successful_with_minimal_required_attrs():
    json_input = json.dumps(minimal_attributes)
    from_json(json_input)
    from_json_batch("[" + json_input + "]")


def test_from_json_batch():
    events = from_json_batch(valid_json_batch)
    assert isinstance(events, list)
    assert len(events) == 1

    event = events[0]
    assert event.type == "com.example.string"
    assert event.source == ParseResult(
        scheme="https",
        netloc="example.com",
        path="/event-producer",
        params="",
        query="",
        fragment="",
    )
    assert event.data is None
    assert event.id == "b96267e2-87be-4f7a-b87c-82f64360d954"
    assert event.specversion is SpecVersion.v1_0
    assert event.time == datetime.datetime(
        year=2022,
        month=7,
        day=16,
        hour=12,
        minute=3,
        second=20,
        microsecond=519216,
        tzinfo=datetime.timezone(datetime.timedelta(hours=4)),
    )
    assert event.subject is None
    assert event.datacontenttype is None
    assert event.dataschema is None


def test_to_json():
    event = CloudEvent.event_factory(**test_attributes)
    json_repr = to_json(event)
    assert json_repr == valid_json
    validate(json.loads(json_repr), cloudevent_schema)


def test_to_json_batch():
    event = CloudEvent.event_factory(**test_attributes)
    json_repr = to_json_batch([event])
    assert json.loads(json_repr) == json.loads(valid_json_batch)
    validate(json.loads(json_repr)[0], cloudevent_schema)


@pytest.mark.parametrize(
    ["data", "b64_expected"],
    [
        pytest.param("test", False, id="string"),
        pytest.param(b"test", True, id="bytes"),
        pytest.param(bytearray([2, 3, 5, 7]), True, id="bytearray"),
        pytest.param(memoryview(b"test"), True, id="memoryview"),
    ],
)
@pytest.mark.parametrize(
    "batch", [pytest.param(True, id="batch"), pytest.param(False, id="single")]
)
def test_to_json_base64_with_any_type(
    data: Any,
    b64_expected: bool,
    batch: bool,
):
    event = CloudEvent.event_factory(**test_attributes)
    event.data = data

    json_repr = to_json_batch([event]) if batch else to_json(event)
    parsed_json = json.loads(json_repr)
    if batch:
        parsed_json = parsed_json[0]

    assert ('"data_base64":' in json_repr) is b64_expected
    assert ('"data":' not in json_repr) is b64_expected
    validate(parsed_json, cloudevent_schema)
    assert ("data_base64" in parsed_json) is b64_expected
    assert ("data" not in parsed_json) is b64_expected


@pytest.mark.parametrize(
    ["b64_data", "expected_value"],
    [
        pytest.param("dGVzdA==", b"test", id='b"test"'),
        # It's impossible to automatically infer if the data is meant to be a bytearray
        pytest.param("AgMFBw==", b"\x02\x03\x05\x07", id="bytearray([2, 3, 5, 7])"),
        # b64encode serializes the memory view using the value
        # (good for security, we don't want to send memory info around)
        pytest.param("dGVzdA==", b"test", id='memoryview(b"test")'),
    ],
)
@pytest.mark.parametrize(
    "batch", [pytest.param(True, id="batch"), pytest.param(False, id="single")]
)
def test_from_json_base64_with_any_type(
    b64_data: str, expected_value: type, batch: bool
):
    json_string = (
        '{"data_base64":"'
        + b64_data
        + '","source":"https://example.com/event-producer","id":"b96267e2-87be-4f7a-b87c-82f64360d954","type":"com.example.string","specversion":"1.0","time":"2022-07-16T12:03:20.519216+04:00","subject":null,"datacontenttype":null,"dataschema":null}'
    )

    if batch:
        event = from_json_batch("[" + json_string + "]")[0]
    else:
        event = from_json(json_string)
    assert event.data == expected_value


@pytest.mark.parametrize(
    ["data", "b64_expected"],
    [
        pytest.param("test", True, id="string"),
        pytest.param(b"test", True, id="bytes"),
        pytest.param(bytearray([2, 3, 5, 7]), True, id="bytearray"),
    ],
)
@pytest.mark.parametrize(
    "batch", [pytest.param(True, id="batch"), pytest.param(False, id="single")]
)
def test_to_json_base64_with_binary_type(
    data: Any,
    b64_expected: bool,
    batch: bool,
):
    class BinaryDataEvent(CloudEvent):
        data: Binary

    input_attrs = test_attributes.copy()
    input_attrs["data"] = data
    event = BinaryDataEvent.event_factory(**input_attrs)

    json_repr = to_json_batch([event]) if batch else to_json(event)
    parsed_json = json.loads(json_repr)
    if batch:
        parsed_json = parsed_json[0]

    assert ('"data_base64":' in json_repr) is b64_expected
    assert ('"data":' not in json_repr) is b64_expected
    validate(parsed_json, cloudevent_schema)
    assert ("data_base64" in parsed_json) is b64_expected
    assert ("data" not in parsed_json) is b64_expected


@pytest.mark.parametrize(
    ["b64_data", "expected_value"],
    [
        pytest.param("dGVzdA==", b"test", id='b"test"'),
        # It's impossible to automatically infer if the data is meant to be a bytearray
        pytest.param("AgMFBw==", b"\x02\x03\x05\x07", id="bytearray([2, 3, 5, 7])"),
        # b64encode serializes the memory view using the value
        # (good for security, we don't want to send memory info around)
        pytest.param("dGVzdA==", b"test", id='memoryview(b"test")'),
    ],
)
@pytest.mark.parametrize(
    "batch", [pytest.param(True, id="batch"), pytest.param(False, id="single")]
)
def test_from_json_base64_with_binary_type(
    b64_data: str, expected_value: type, batch: bool
):
    class BinaryDataEvent(CloudEvent):
        data: Binary

    json_string = (
        '{"data_base64":"'
        + b64_data
        + '","source":"https://example.com/event-producer","id":"b96267e2-87be-4f7a-b87c-82f64360d954","type":"com.example.string","specversion":"1.0","time":"2022-07-16T12:03:20.519216+04:00","subject":null,"datacontenttype":null,"dataschema":null}'
    )

    if batch:
        event = from_json_batch(
            "[" + json_string + "]",
            batch_adapter=TypeAdapter(Sequence[BinaryDataEvent]),
        )[0]
    else:
        event = from_json(json_string, BinaryDataEvent)
    assert event.data == expected_value
    assert isinstance(event, BinaryDataEvent)


def test_nested_binary_fields_correctly_serialized():
    class SomeData(TypedDict):
        # Using `data` to verify it doesn't become `data_base64` when nested
        data: Binary
        test: str

    class BinaryNestedEvent(CloudEvent):
        data: SomeData

    input_attrs = test_attributes.copy()
    input_attrs["data"] = {
        "data": b"\x02\x03\x05\x07",
        "test": "test",
    }
    event = BinaryNestedEvent.event_factory(**input_attrs)
    assert (
        to_json(event)
        == '{"data":{"data":"AgMFBw==","test":"test"},"source":"https://example.com/event-producer","id":"b96267e2-87be-4f7a-b87c-82f64360d954","type":"com.example.string","specversion":"1.0","time":"2022-07-16T12:03:20.519216+04:00","subject":null,"datacontenttype":null,"dataschema":null}'
    )


def test_nested_binary_fields_correctly_deserialized():
    json_input = '{"data":{"data":"AgMFBw==","test":"test"},"source":"https://example.com/event-producer","id":"b96267e2-87be-4f7a-b87c-82f64360d954","type":"com.example.string","specversion":"1.0","time":"2022-07-16T12:03:20.519216+04:00","subject":null,"datacontenttype":null,"dataschema":null}'

    class SomeData(TypedDict):
        # Using `data` to verify it doesn't become `data_base64` when nested
        data: Binary
        test: str

    class BinaryNestedEvent(CloudEvent):
        data: SomeData

    event: BinaryNestedEvent = from_json(json_input, BinaryNestedEvent)
    assert event.data["data"] == b"\x02\x03\x05\x07"
