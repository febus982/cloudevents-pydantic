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
from typing import (
    Dict,
    Generic,
    List,
    NamedTuple,
    Type,
    TypeVar,
    cast,
)

from pydantic import TypeAdapter

from cloudevents_pydantic.events import CloudEvent
from cloudevents_pydantic.formats import json

_T = TypeVar("_T", bound=CloudEvent)


class HTTPComponents(NamedTuple):
    headers: Dict[str, str]
    body: str


class HTTPHandler(Generic[_T]):
    event_adapter: TypeAdapter[_T]
    batch_adapter: TypeAdapter[List[_T]]

    def __init__(self, event_class: Type[_T] = cast(Type[_T], CloudEvent)) -> None:
        super().__init__()
        self.event_adapter = TypeAdapter(event_class)
        self.batch_adapter = TypeAdapter(List[event_class])  # type: ignore[valid-type]

    def to_json(self, event: _T) -> HTTPComponents:
        """
        Serializes an event in JSON format.

        :param event: The event object to serialize
        :type event: CloudEvent
        :return: The headers and the body representation of the event
        :rtype: HTTPComponents
        """
        headers = {"content-type": "application/cloudevents+json; charset=UTF-8"}
        body = json.to_json(event)
        return HTTPComponents(headers, body)

    def to_json_batch(self, events: List[_T]) -> HTTPComponents:
        """
        Serializes a list of events in JSON batch format.

        :param events: The event object to serialize
        :type events: List[CloudEvent]
        :return: The headers and the body representation of the event batch
        :rtype: HTTPComponents
        """
        headers = {"content-type": "application/cloudevents-batch+json; charset=UTF-8"}
        body = json.to_json_batch(events, self.batch_adapter)
        return HTTPComponents(headers, body)

    def from_json(
        self,
        body: str,
    ) -> CloudEvent:
        """
        Deserializes an event from JSON format.

        :param body: The JSON representation of the event
        :type body: str
        :return: The deserialized event
        :rtype: CloudEvent
        """
        return json.from_json(body, self.event_adapter)

    def from_json_batch(
        self,
        body: str,
    ) -> List[_T]:
        """
        Deserializes a list of events from JSON batch format.

        :param body: The JSON representation of the event batch
        :type body: str
        :return: The deserialized event batch
        :rtype: List[CloudEvent]
        """
        return json.from_json_batch(body, self.batch_adapter)
