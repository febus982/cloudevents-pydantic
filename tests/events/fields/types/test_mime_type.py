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
import pytest
from pydantic import BaseModel, ValidationError

from cloudevents_pydantic.events.fields.types import MimeType


@pytest.mark.parametrize(
    ["valid_mime_type"],
    (
        ("application/something",),
        ("audio/something",),
        ("example/something",),
        ("font/something",),
        ("haptics/something",),
        ("image/something",),
        ("message/something",),
        ("model/something",),
        ("multipart/something",),
        ("text/something",),
        ("video/something",),
    ),
)
def test_validation_valid_mime(valid_mime_type):
    class MimeModel(BaseModel):
        value: MimeType

    MimeModel(value=valid_mime_type)


def test_validation_invalid_mime():
    class MimeModel(BaseModel):
        value: MimeType

    with pytest.raises(ValidationError):
        MimeModel(value="not-a-mime-type")


@pytest.mark.parametrize(
    ["valid_mime_type"],
    (
        ("application/something",),
        ("audio/something",),
        ("example/something",),
        ("font/something",),
        ("haptics/something",),
        ("image/something",),
        ("message/something",),
        ("model/something",),
        ("multipart/something",),
        ("text/something",),
        ("video/something",),
    ),
)
def test_serialization_valid_mime(valid_mime_type):
    class MimeModel(BaseModel):
        value: MimeType

    m = MimeModel(value=valid_mime_type)
    assert m.model_dump() == {"value": valid_mime_type}
    assert m.model_dump_json() == '{"value":"' + valid_mime_type + '"}'
    assert isinstance(m.model_dump()["value"], str)
