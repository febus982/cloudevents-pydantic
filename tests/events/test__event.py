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
from uuid import UUID

from cloudevents.sdk.event.attribute import SpecVersion

from cloudevents_pydantic.events import CloudEvent

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
    "specversion": "0.3",
    "subject": "some-subject",
    "time": "2022-07-16T12:03:20.519216+04:00",
    "type": "dummy.type",
}


def test_defaults_are_populated():
    event = CloudEvent(**test_attributes)

    # input data
    assert event.type == test_attributes["type"]
    assert event.source == test_attributes["source"]

    # defaults
    assert event.data is None
    assert isinstance(event.id, str)
    assert UUID(event.id) is not None
    assert event.specversion is SpecVersion.v1_0
    assert isinstance(event.time, datetime.datetime)
    assert event.subject is None
    assert event.datacontenttype is None
    assert event.dataschema is None


def test_all_values_can_be_submitted():
    event = CloudEvent(**test_full_attributes)

    assert event.type == test_full_attributes["type"]
    assert event.source == test_full_attributes["source"]
    assert event.data == test_full_attributes["data"]
    assert event.id == test_full_attributes["id"]
    assert event.specversion is SpecVersion.v0_3
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
    assert event.dataschema == test_full_attributes["dataschema"]


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
    event = CloudEvent(**(test_full_attributes | time_input))

    assert event.type == test_full_attributes["type"]
    assert event.source == test_full_attributes["source"]
    assert event.data == test_full_attributes["data"]
    assert event.id == test_full_attributes["id"]
    assert event.specversion is SpecVersion.v0_3
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
    assert event.dataschema == test_full_attributes["dataschema"]
