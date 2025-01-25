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
from typing import Union

import pytest
from pydantic import BaseModel, ValidationError

from cloudevents_pydantic.events.fields.types import Binary


@pytest.mark.parametrize(
    ["data", "serialized_output"],
    [
        pytest.param(b"test", "dGVzdA==", id="bytes"),
        pytest.param(b"\x02\x03\x05\x07", "AgMFBw==", id="bytearray"),
    ],
)
def test_binary_serialization(
    data: Union[bytes, str],
    serialized_output: str,
):
    class BinaryModel(BaseModel):
        value: Binary

    m = BinaryModel(value=data)

    assert m.model_dump() == {"value": serialized_output}
    assert m.model_dump_json() == '{"value":"' + serialized_output + '"}'
    assert isinstance(m.model_dump()["value"], str)


@pytest.mark.parametrize(
    ["data", "validated_data"],
    [
        pytest.param("dGVzdA==", b"test", id="bytes_base64"),
        pytest.param(b"test", b"test", id="bytes"),
        pytest.param("AgMFBw==", b"\x02\x03\x05\x07", id="bytearray_base64"),
        pytest.param(b"\x02\x03\x05\x07", b"\x02\x03\x05\x07", id="bytearray"),
    ],
)
def test_binary_validation_accepts_strings_and_bytes(
    data: Union[bytes, str],
    validated_data: bytes,
):
    class BinaryModel(BaseModel):
        value: Binary

    model = BinaryModel(value=data)

    assert model.value == validated_data
    assert isinstance(model.value, bytes)


@pytest.mark.parametrize(
    ["data"],
    [
        pytest.param(99.99, id="float"),
        pytest.param("non?-/*base64-string", id="non_base_64_string"),
    ],
)
def test_binary_validation_fails_on_non_strings_and_bytes(data):
    class BinaryModel(BaseModel):
        value: Binary

    with pytest.raises(ValidationError):
        BinaryModel(value=data)
