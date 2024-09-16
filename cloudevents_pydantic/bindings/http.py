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
    Sequence,
    Tuple,
    Type,
    cast,
)

from pydantic import TypeAdapter
from typing_extensions import TypeVar

from cloudevents_pydantic.events import CloudEvent
from cloudevents_pydantic.formats import json

_T = TypeVar("_T", bound=CloudEvent, default=CloudEvent)


class HTTPHandler(Generic[_T]):
    event_class: Type[_T]
    batch_adapter: TypeAdapter[Sequence[_T]]

    def __init__(self, event_class: Type[_T] = cast(Type[_T], CloudEvent)) -> None:
        super().__init__()
        self.event_class = event_class
        self.batch_adapter = TypeAdapter(Sequence[event_class])  # type: ignore[valid-type]

    def to_json(self, event: _T) -> Tuple[Dict[str, str], str]:
        headers = {"Content-Type": "application/cloudevents+json; charset=UTF-8"}
        data = json.to_json(event)
        return headers, data

    def to_json_batch(self, events: Sequence[_T]) -> Tuple[Dict[str, str], str]:
        headers = {"Content-Type": "application/cloudevents-batch+json; charset=UTF-8"}
        data = json.to_json_batch(events, self.batch_adapter)
        return headers, data

    def from_json(
        self,
        body: str,
    ) -> CloudEvent:
        return json.from_json(body, self.event_class)

    def from_json_batch(
        self,
        body: str,
    ) -> Sequence[_T]:
        return json.from_json_batch(body, self.batch_adapter)
