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
import base64
import datetime
import typing

from cloudevents.pydantic.fields_docs import FIELD_DESCRIPTIONS
from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    model_serializer,
    model_validator,
)
from pydantic_core.core_schema import ValidationInfo
from ulid import ULID

from .field_types import URI, DateTime, SpecVersion, String, URIReference
from .field_types._canonic_types import DEFAULT_SPECVERSION


class CloudEvent(BaseModel):  # type: ignore
    """
    A Python-friendly CloudEvent representation backed by Pydantic-modeled fields.
    """

    @classmethod
    def event_factory(
        cls,
        id: typing.Optional[str] = None,
        specversion: typing.Optional[SpecVersion] = None,
        time: typing.Optional[datetime.datetime] = None,
        **kwargs,
    ) -> "CloudEvent":
        return cls(
            id=id or str(ULID()),
            specversion=specversion or DEFAULT_SPECVERSION,
            time=time or datetime.datetime.now(datetime.timezone.utc),
            **kwargs,
        )

    data: typing.Optional[typing.Any] = Field(
        title=FIELD_DESCRIPTIONS["data"].get("title"),
        description=FIELD_DESCRIPTIONS["data"].get("description"),
        examples=[FIELD_DESCRIPTIONS["data"].get("example")],
        default=None,
    )

    # Mandatory fields
    source: URIReference = Field(
        title=FIELD_DESCRIPTIONS["source"].get("title"),
        description=FIELD_DESCRIPTIONS["source"].get("description"),
        examples=[FIELD_DESCRIPTIONS["source"].get("example")],
    )
    id: String = Field(
        title=FIELD_DESCRIPTIONS["id"].get("title"),
        description=FIELD_DESCRIPTIONS["id"].get("description"),
        examples=[FIELD_DESCRIPTIONS["id"].get("example")],
    )
    type: String = Field(
        title=FIELD_DESCRIPTIONS["type"].get("title"),
        description=FIELD_DESCRIPTIONS["type"].get("description"),
        examples=[FIELD_DESCRIPTIONS["type"].get("example")],
    )
    specversion: SpecVersion = Field(
        title=FIELD_DESCRIPTIONS["specversion"].get("title"),
        description=FIELD_DESCRIPTIONS["specversion"].get("description"),
        examples=[FIELD_DESCRIPTIONS["specversion"].get("example")],
    )

    # Optional fields
    time: typing.Optional[DateTime] = Field(
        title=FIELD_DESCRIPTIONS["time"].get("title"),
        description=FIELD_DESCRIPTIONS["time"].get("description"),
        examples=[FIELD_DESCRIPTIONS["time"].get("example")],
        default=None,
    )
    subject: typing.Optional[String] = Field(
        title=FIELD_DESCRIPTIONS["subject"].get("title"),
        description=FIELD_DESCRIPTIONS["subject"].get("description"),
        examples=[FIELD_DESCRIPTIONS["subject"].get("example")],
        default=None,
    )
    datacontenttype: typing.Optional[String] = Field(
        title=FIELD_DESCRIPTIONS["datacontenttype"].get("title"),
        description=FIELD_DESCRIPTIONS["datacontenttype"].get("description"),
        examples=[FIELD_DESCRIPTIONS["datacontenttype"].get("example")],
        default=None,
    )
    dataschema: typing.Optional[URI] = Field(
        title=FIELD_DESCRIPTIONS["dataschema"].get("title"),
        description=FIELD_DESCRIPTIONS["dataschema"].get("description"),
        examples=[FIELD_DESCRIPTIONS["dataschema"].get("example")],
        default=None,
    )

    model_config = ConfigDict(
        extra="forbid",
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

    """
    Having the JSON functionality here is a violation of the Single Responsibility
    Principle, however we want to get advantage of improved pydantic JSON performances.
    Using `orjson` could solve this, perhaps it could be a future improvement.
    """

    @model_serializer(when_used="json")
    def base64_json_serializer(self) -> typing.Dict[str, typing.Any]:
        """Takes care of handling binary data serialization into `data_base64`
        attribute.

        :param self: CloudEvent.

        :return: Event serialized as a standard CloudEvent dict with binary
                 data handled.
        """
        model_dict = self.model_dump()  # type: ignore

        if isinstance(self.data, (bytes, bytearray, memoryview)):
            model_dict["data_base64"] = (
                base64.b64encode(self.data)
                if isinstance(self.data, (bytes, bytearray, memoryview))
                else self.data
            )
            del model_dict["data"]

        return model_dict

    @model_validator(mode="before")
    @classmethod
    def base64_data_parser(cls, data: typing.Any, info: ValidationInfo) -> typing.Any:
        """Takes care of handling binary data deserialization from `data_base64`
        attribute.

        :param data: Input data for validation
        :param info: Pydantic validation context
        :return: input data, after handling data_base64
        """
        if info.mode == "json" and isinstance(data, dict) and data.get("data_base64"):
            data["data"] = base64.b64decode(data["data_base64"])
            del data["data_base64"]
        return data
