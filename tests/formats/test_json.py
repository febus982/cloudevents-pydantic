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
from typing import Any

import pytest
from cloudevents.sdk.event.attribute import SpecVersion
from jsonschema import validate

from cloudevents_pydantic.events import CloudEvent
from cloudevents_pydantic.formats.json import from_json, to_json

test_attributes = {
    "type": "com.example.string",
    "source": "https://example.com/event-producer",
    "id": "b96267e2-87be-4f7a-b87c-82f64360d954",
    "time": "2022-07-16T12:03:20.519216+04:00",
}
valid_json = '{"data":null,"source":"https://example.com/event-producer","id":"b96267e2-87be-4f7a-b87c-82f64360d954","type":"com.example.string","specversion":"1.0","time":"2022-07-16T12:03:20.519216+04:00","subject":null,"datacontenttype":null,"dataschema":null}'

with open(
    Path(__file__).parent.joinpath("cloudevents_jsonschema_1.0.2.json"),
    "r",
) as f:
    cloudevent_schema = json.load(f)


def test_from_json():
    event = from_json(valid_json)

    assert event.type == "com.example.string"
    assert event.source == "https://example.com/event-producer"
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
    event = CloudEvent(**test_attributes)
    json_repr = to_json(event)
    assert json_repr == valid_json
    validate(json.loads(json_repr), cloudevent_schema)


@pytest.mark.parametrize(
    ["data", "b64_expected"],
    [
        pytest.param("test", False, id="string"),
        pytest.param(b"test", True, id="bytes"),
        pytest.param(bytearray([2, 3, 5, 7]), True, id="bytearray"),
        pytest.param(memoryview(b"test"), True, id="memoryview"),
    ],
)
def test_to_json_base64(data: Any, b64_expected: bool):
    event = CloudEvent(**test_attributes)
    event.data = data

    json_repr = to_json(event)
    parsed_json = json.loads(json_repr)

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
def test_from_json_base64(b64_data: str, expected_value: type):
    json_string = (
        '{"data_base64":"'
        + b64_data
        + '","source":"https://example.com/event-producer","id":"b96267e2-87be-4f7a-b87c-82f64360d954","type":"com.example.string","specversion":"1.0","time":"2022-07-16T12:03:20.519216+04:00","subject":null,"datacontenttype":null,"dataschema":null}'
    )

    event = from_json(json_string)
    assert event.data == expected_value
