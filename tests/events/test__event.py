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
from urllib.parse import ParseResult

import pytest
from pydantic import ValidationError
from ulid import ULID

from cloudevents_pydantic.events import CloudEvent
from cloudevents_pydantic.events.fields.types import SpecVersion

test_attributes = {
    "type": "com.example.string",
    "source": "https://example.com/event-producer",
}
test_full_attributes = {
    "data": {"data-key": "val"},
    "datacontenttype": "application/octet-stream",
    "dataschema": "http://some-dataschema.url",
    "id": "id-can-be-anything",
    "source": "dummy:source",
    "specversion": "1.0",
    "subject": "some-subject",
    "time": "2022-07-16T12:03:20.519216+04:00",
    "type": "dummy.type",
}


def test_defaults_are_populated_when_using_factory():
    event = CloudEvent.event_factory(**test_attributes)

    # input data
    assert event.type == test_attributes["type"]
    assert event.source == ParseResult(
        scheme="https",
        netloc="example.com",
        path="/event-producer",
        params="",
        query="",
        fragment="",
    )

    # defaults
    assert event.data is None
    assert isinstance(event.id, str)
    assert ULID.from_str(event.id) is not None
    assert event.specversion is SpecVersion.v1_0
    assert isinstance(event.time, datetime.datetime)
    assert event.subject is None
    assert event.datacontenttype is None
    assert event.dataschema is None


def test_all_values_can_be_submitted_as_string():
    event = CloudEvent(**test_full_attributes)

    assert event.type == test_full_attributes["type"]
    assert event.source == ParseResult(
        scheme="dummy", netloc="", path="source", params="", query="", fragment=""
    )
    assert event.data == test_full_attributes["data"]
    assert event.id == test_full_attributes["id"]
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
    assert event.subject == test_full_attributes["subject"]
    assert event.datacontenttype == test_full_attributes["datacontenttype"]
    assert event.dataschema == ParseResult(
        scheme="http",
        netloc="some-dataschema.url",
        path="",
        params="",
        query="",
        fragment="",
    )


def test_can_submit_datetime_object():
    time_input = {
        "time": datetime.datetime(
            year=2020,
            month=7,
            day=16,
            hour=12,
            minute=3,
            second=20,
            microsecond=519216,
            tzinfo=datetime.timezone(datetime.timedelta(hours=4)),
        )
    }
    attrs = test_full_attributes.copy()
    attrs.update(time_input)
    event = CloudEvent(**attrs)

    assert event.type == test_full_attributes["type"]
    assert event.source == ParseResult(
        scheme="dummy", netloc="", path="source", params="", query="", fragment=""
    )
    assert event.data == test_full_attributes["data"]
    assert event.id == test_full_attributes["id"]
    assert event.specversion is SpecVersion.v1_0
    assert event.time == datetime.datetime(
        year=2020,
        month=7,
        day=16,
        hour=12,
        minute=3,
        second=20,
        microsecond=519216,
        tzinfo=datetime.timezone(datetime.timedelta(hours=4)),
    )
    assert event.subject == test_full_attributes["subject"]
    assert event.datacontenttype == test_full_attributes["datacontenttype"]
    assert event.dataschema == ParseResult(
        scheme="http",
        netloc="some-dataschema.url",
        path="",
        params="",
        query="",
        fragment="",
    )


def test_can_submit_specversion_enum():
    time_input = {"specversion": SpecVersion.v1_0}
    attrs = test_full_attributes.copy()
    attrs.update(time_input)
    event = CloudEvent(**attrs)

    assert event.type == test_full_attributes["type"]
    assert event.source == ParseResult(
        scheme="dummy", netloc="", path="source", params="", query="", fragment=""
    )
    assert event.data == test_full_attributes["data"]
    assert event.id == test_full_attributes["id"]
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
    assert event.subject == test_full_attributes["subject"]
    assert event.datacontenttype == test_full_attributes["datacontenttype"]
    assert event.dataschema == ParseResult(
        scheme="http",
        netloc="some-dataschema.url",
        path="",
        params="",
        query="",
        fragment="",
    )


def test_data_base64_validation_fails_if_not_json():
    json_string = '{"data_base64":"dGVzdA==","source":"https://example.com/event-producer","id":"b96267e2-87be-4f7a-b87c-82f64360d954","type":"com.example.string","specversion":"1.0","time":"2022-07-16T12:03:20.519216+04:00","subject":null,"datacontenttype":null,"dataschema":null}'
    attributes = json.loads(json_string)

    with pytest.raises(ValidationError):
        CloudEvent.model_validate(attributes)

    event = CloudEvent.model_validate_json(json_string)
    assert event.data == b"test"
