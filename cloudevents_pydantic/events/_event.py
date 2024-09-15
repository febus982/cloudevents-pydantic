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
import typing

from cloudevents.pydantic.fields_docs import FIELD_DESCRIPTIONS
from cloudevents.sdk.event import attribute
from pydantic import BaseModel, ConfigDict, Field


class CloudEvent(BaseModel):  # type: ignore
    """
    A Python-friendly CloudEvent representation backed by Pydantic-modeled fields.
    """

    data: typing.Optional[typing.Any] = Field(
        title=FIELD_DESCRIPTIONS["data"].get("title"),
        description=FIELD_DESCRIPTIONS["data"].get("description"),
        examples=[FIELD_DESCRIPTIONS["data"].get("example")],
        default=None,
    )
    source: str = Field(
        title=FIELD_DESCRIPTIONS["source"].get("title"),
        description=FIELD_DESCRIPTIONS["source"].get("description"),
        examples=[FIELD_DESCRIPTIONS["source"].get("example")],
    )
    id: str = Field(
        title=FIELD_DESCRIPTIONS["id"].get("title"),
        description=FIELD_DESCRIPTIONS["id"].get("description"),
        examples=[FIELD_DESCRIPTIONS["id"].get("example")],
        default_factory=attribute.default_id_selection_algorithm,
    )
    type: str = Field(
        title=FIELD_DESCRIPTIONS["type"].get("title"),
        description=FIELD_DESCRIPTIONS["type"].get("description"),
        examples=[FIELD_DESCRIPTIONS["type"].get("example")],
    )
    specversion: attribute.SpecVersion = Field(
        title=FIELD_DESCRIPTIONS["specversion"].get("title"),
        description=FIELD_DESCRIPTIONS["specversion"].get("description"),
        examples=[FIELD_DESCRIPTIONS["specversion"].get("example")],
        default=attribute.DEFAULT_SPECVERSION,
    )
    time: typing.Optional[datetime.datetime] = Field(
        title=FIELD_DESCRIPTIONS["time"].get("title"),
        description=FIELD_DESCRIPTIONS["time"].get("description"),
        examples=[FIELD_DESCRIPTIONS["time"].get("example")],
        default_factory=attribute.default_time_selection_algorithm,
    )
    subject: typing.Optional[str] = Field(
        title=FIELD_DESCRIPTIONS["subject"].get("title"),
        description=FIELD_DESCRIPTIONS["subject"].get("description"),
        examples=[FIELD_DESCRIPTIONS["subject"].get("example")],
        default=None,
    )
    datacontenttype: typing.Optional[str] = Field(
        title=FIELD_DESCRIPTIONS["datacontenttype"].get("title"),
        description=FIELD_DESCRIPTIONS["datacontenttype"].get("description"),
        examples=[FIELD_DESCRIPTIONS["datacontenttype"].get("example")],
        default=None,
    )
    dataschema: typing.Optional[str] = Field(
        title=FIELD_DESCRIPTIONS["dataschema"].get("title"),
        description=FIELD_DESCRIPTIONS["dataschema"].get("description"),
        examples=[FIELD_DESCRIPTIONS["dataschema"].get("example")],
        default=None,
    )

    model_config = ConfigDict(
        extra="allow",  # this is the way we implement extensions
        json_schema_extra={
            "example": {
                "specversion": "1.0",
                "type": "com.github.pull_request.opened",
                "source": "https://github.com/cloudevents/spec/pull",
                "subject": "123",
                "id": "A234-1234-1234",
                "time": "2018-04-05T17:31:00Z",
                "comexampleextension1": "value",
                "comexampleothervalue": 5,
                "datacontenttype": "text/xml",
                "data": '<much wow="xml"/>',
            }
        },
    )
