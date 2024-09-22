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
import pytest
from pydantic import BaseModel

from cloudevents_pydantic.events.field_types import (
    Binary,
    Boolean,
    URIReference,
)


@pytest.mark.parametrize(
    ["input", "serialized_output"],
    (
        (True, "true"),
        (False, "false"),
    ),
)
def test_bool_serialization(input, serialized_output):
    class BoolModel(BaseModel):
        value: Boolean

    assert BoolModel(value=input).model_dump()["value"] == serialized_output


@pytest.mark.parametrize(
    ["data", "expected_value"],
    [
        pytest.param("test", "dGVzdA==", id="string"),
        pytest.param(b"test", "dGVzdA==", id="bytes"),
        pytest.param(bytearray([2, 3, 5, 7]), "AgMFBw==", id="bytearray"),
    ],
)
def test_binary_data_is_b64encoded(data, expected_value):
    class BinaryModel(BaseModel):
        value: Binary

    assert BinaryModel(value=data).model_dump()["value"] == expected_value


@pytest.mark.parametrize(
    ["valid_uri"],
    (
        ("https://github.com/cloudevents",),
        ("mailto:cncf-wg-serverless@lists.cncf.io",),
        ("urn:uuid:6e8bc430-9c3a-11d9-9669-0800200c9a66",),
        ("/cloudevents/spec/pull/123",),
        ("/sensors/tn-1234567/alerts",),
        ("1-555-123-4567",),
        ("some-microservice",),
    ),
)
def test__uri_reference_serializer(valid_uri):
    class UriModel(BaseModel):
        value: URIReference

    assert UriModel(value=valid_uri).model_dump()["value"] == valid_uri
