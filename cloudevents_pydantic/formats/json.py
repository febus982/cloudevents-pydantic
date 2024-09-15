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
from typing import List, Type, TypeVar, overload

from pydantic import TypeAdapter

from ..events import CloudEvent
from ..events._event import CloudEventBatchAdapter

T = TypeVar("T", bound=CloudEvent)
LT = TypeVar("LT", bound=List[CloudEvent])


def to_json(event: CloudEvent) -> str:
    return event.model_dump_json()


# mypy issue: https://github.com/python/mypy/issues/3737
# https://stackoverflow.com/questions/75058589/annotating-function-with-typevar-and-default-value-results-in-union-type
@overload
def from_json(data: str) -> CloudEvent: ...
@overload
def from_json(data: str, model_class: Type[T]) -> T: ...
def from_json(data: str, model_class: Type[CloudEvent] = CloudEvent) -> CloudEvent:
    return model_class.model_validate_json(data)


def to_json_batch(events: List[CloudEvent]) -> str:
    return CloudEventBatchAdapter.dump_json(events).decode()


# mypy issue: https://github.com/python/mypy/issues/3737
# https://stackoverflow.com/questions/75058589/annotating-function-with-typevar-and-default-value-results-in-union-type
@overload
def from_json_batch(data: str) -> List[CloudEvent]: ...
@overload
def from_json_batch(data: str, batch_adapter: TypeAdapter[LT]) -> LT: ...
def from_json_batch(
    data: str, batch_adapter: TypeAdapter = CloudEventBatchAdapter
) -> List[CloudEvent]:
    return batch_adapter.validate_json(data)
