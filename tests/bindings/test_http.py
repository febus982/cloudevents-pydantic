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
from typing import List, Sequence
from unittest.mock import patch

import pytest
from pydantic import Field, TypeAdapter

from cloudevents_pydantic.bindings.http import HTTPHandler
from cloudevents_pydantic.events import CloudEvent
from cloudevents_pydantic.formats import json

test_attributes = {
    "type": "com.example.string",
    "source": "https://example.com/event-producer",
    "id": "b96267e2-87be-4f7a-b87c-82f64360d954",
    "time": "2022-07-16T12:03:20.519216+04:00",
}
valid_json = '{"data":null,"source":"https://example.com/event-producer","id":"b96267e2-87be-4f7a-b87c-82f64360d954","type":"com.example.string","specversion":"1.0","time":"2022-07-16T12:03:20.519216+04:00","subject":null,"datacontenttype":null,"dataschema":null}'
valid_json_batch = '[{"data":null,"source":"https://example.com/event-producer","id":"b96267e2-87be-4f7a-b87c-82f64360d954","type":"com.example.string","specversion":"1.0","time":"2022-07-16T12:03:20.519216+04:00","subject":null,"datacontenttype":null,"dataschema":null}]'


class SomeEvent(CloudEvent):
    some_attr: str = Field(default="some_value")


SomeAdapter = TypeAdapter(List[SomeEvent])

some_event_json = '{"data":null,"source":"https://example.com/event-producer","id":"b96267e2-87be-4f7a-b87c-82f64360d954","type":"com.example.string","specversion":"1.0","time":"2022-07-16T12:03:20.519216+04:00","subject":null,"datacontenttype":null,"dataschema":null,"some_attr":"some_value"}'
some_event_json_batch = '[{"data":null,"source":"https://example.com/event-producer","id":"b96267e2-87be-4f7a-b87c-82f64360d954","type":"com.example.string","specversion":"1.0","time":"2022-07-16T12:03:20.519216+04:00","subject":null,"datacontenttype":null,"dataschema":null,"some_attr":"some_value"}]'


@pytest.fixture
def type_adapter_init_mock():
    with patch.object(TypeAdapter, "__init__", return_value=None) as mocked_function:
        yield mocked_function


@pytest.fixture
def to_json_spy():
    f = json.to_json
    with patch("cloudevents_pydantic.formats.json.to_json", wraps=f) as mocked_function:
        yield mocked_function


@pytest.fixture
def to_json_batch_spy():
    f = json.to_json_batch
    with patch(
        "cloudevents_pydantic.formats.json.to_json_batch", wraps=f
    ) as mocked_function:
        yield mocked_function


@pytest.fixture
def from_json_spy():
    f = json.from_json
    with patch(
        "cloudevents_pydantic.formats.json.from_json", wraps=f
    ) as mocked_function:
        yield mocked_function


@pytest.fixture
def from_json_batch_spy():
    f = json.from_json_batch
    with patch(
        "cloudevents_pydantic.formats.json.from_json_batch", wraps=f
    ) as mocked_function:
        yield mocked_function


def test_initialization_defaults_to_cloudevents(type_adapter_init_mock):
    handler = HTTPHandler()
    assert handler.event_class is CloudEvent
    type_adapter_init_mock.assert_called_once_with(Sequence[CloudEvent])


def test_initialization_uses_provided_event_class(type_adapter_init_mock):
    handler = HTTPHandler(event_class=SomeEvent)
    assert handler.event_class is SomeEvent
    type_adapter_init_mock.assert_called_once_with(Sequence[SomeEvent])


@pytest.mark.parametrize(
    "event, expected_output",
    [
        (CloudEvent(**test_attributes), valid_json),
        (SomeEvent(**test_attributes), some_event_json),
    ],
)
def test_to_json(event, expected_output, to_json_spy):
    handler = HTTPHandler()

    headers, json_repr = handler.to_json(event)
    to_json_spy.assert_called_once_with(event)
    assert json_repr == expected_output


@pytest.mark.parametrize(
    "event, expected_output",
    [
        (CloudEvent(**test_attributes), valid_json_batch),
        (SomeEvent(**test_attributes), some_event_json_batch),
    ],
)
def test_to_json_batch(event, expected_output, to_json_batch_spy):
    handler = HTTPHandler()

    headers, json_repr = handler.to_json_batch([event])
    to_json_batch_spy.assert_called_once_with([event], handler.batch_adapter)
    assert json_repr == expected_output


def test_from_json(from_json_spy):
    handler = HTTPHandler(event_class=SomeEvent)
    event = handler.from_json(valid_json)

    from_json_spy.assert_called_once_with(valid_json, handler.event_class)
    assert event == SomeEvent(**test_attributes)
    assert event != CloudEvent(**test_attributes)
    assert isinstance(event, SomeEvent)


def test_from_json_batch(from_json_batch_spy):
    handler = HTTPHandler(event_class=SomeEvent)
    events = handler.from_json_batch(valid_json_batch)
    event = events[0]

    assert len(events) == 1
    from_json_batch_spy.assert_called_once_with(valid_json_batch, handler.batch_adapter)
    assert event == SomeEvent(**test_attributes)
    assert event != CloudEvent(**test_attributes)
    assert isinstance(event, SomeEvent)
