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
from typing import Union

import pytest
from pydantic import BaseModel

from cloudevents_pydantic.events.fields.types import Timestamp


@pytest.mark.parametrize(
    ["data", "serialized_output"],
    [
        (
            "2020-07-16T12:03:20.519216+04:00",
            "2020-07-16T12:03:20.519216+04:00",
        ),
        (
            datetime.datetime(
                year=2020,
                month=7,
                day=16,
                hour=12,
                minute=3,
                second=20,
                microsecond=519216,
                tzinfo=datetime.timezone(datetime.timedelta(hours=4)),
            ),
            "2020-07-16T12:03:20.519216+04:00",
        ),
        (
            datetime.datetime(
                year=2020,
                month=7,
                day=16,
                hour=12,
                minute=3,
                second=20,
                microsecond=519216,
                # UTC time zone
                tzinfo=datetime.timezone(datetime.timedelta(0)),
            ),
            "2020-07-16T12:03:20.519216+00:00",
        ),
        (
            datetime.datetime(
                year=2020,
                month=7,
                day=16,
                hour=12,
                minute=3,
                second=20,
            ),
            "2020-07-16T12:03:20",
        ),
        (
            datetime.date(year=2020, month=7, day=16),
            "2020-07-16T00:00:00",
        ),
    ],
)
def test_timestamp_serialization(
    data: Union[datetime.datetime, datetime.date, str],
    serialized_output: str,
):
    class TimestampModel(BaseModel):
        value: Timestamp

    model = TimestampModel(value=data)

    assert isinstance(model.value, datetime.datetime)
    assert model.model_dump() == {"value": serialized_output}
    assert model.model_dump_json() == '{"value":"' + serialized_output + '"}'
    assert isinstance(model.model_dump()["value"], str)
