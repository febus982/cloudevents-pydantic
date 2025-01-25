# ==============================================================================
#  Copyright (c) 2025 Federico Busetti                                         =
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
from typing import Any, Dict
from urllib.parse import ParseResult

from cloudevents_pydantic.events import CloudEvent
from cloudevents_pydantic.events.fields.types import SpecVersion
from cloudevents_pydantic.formats.canonical import deserialize, serialize

test_attributes: Dict[str, Any] = {
    "type": "com.example.string",
    "source": "https://example.com/event-producer",
    "id": "b96267e2-87be-4f7a-b87c-82f64360d954",
    "specversion": "1.0",
    "time": "2022-07-16T12:03:20.519216+04:00",
    "data": "some_data",
    "subject": "some_subject",
    "datacontenttype": "text/plain;charset=utf-8",
    "dataschema": "https://example.com/event-schema",
}

# Pydantic is converting all inputs in the proper types
test_event = CloudEvent(**test_attributes)


def test_canonical_serialization():
    assert serialize(test_event) == test_attributes


def test_canonical_deserialization():
    event = deserialize(test_attributes)
    assert event == test_event
    assert event.type == "com.example.string"
    assert event.source == ParseResult(
        scheme="https",
        netloc="example.com",
        path="/event-producer",
        params="",
        query="",
        fragment="",
    )
    assert event.data == "some_data"
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
    assert event.subject == "some_subject"
    assert event.datacontenttype == "text/plain;charset=utf-8"
    assert event.dataschema == ParseResult(
        scheme="https",
        netloc="example.com",
        path="/event-schema",
        params="",
        query="",
        fragment="",
    )
