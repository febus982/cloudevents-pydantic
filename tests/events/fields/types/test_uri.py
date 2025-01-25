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
from urllib.parse import ParseResult

import pytest
from pydantic import BaseModel, ValidationError

from cloudevents_pydantic.events.fields.types import URI


@pytest.mark.parametrize(
    ["invalid_uri"],
    (
        ("non-uri",),
        ("/relative/uri",),
    ),
)
def test_validation_fails_with_invalid_uri(invalid_uri):
    class UriModel(BaseModel):
        value: URI

    with pytest.raises(ValidationError):
        UriModel(value=invalid_uri)


@pytest.mark.parametrize(
    ["valid_uri", "parsed_uri"],
    (
        (
            "https://github.com/cloudevents",
            ParseResult(
                scheme="https",
                netloc="github.com",
                path="/cloudevents",
                params="",
                query="",
                fragment="",
            ),
        ),
        (
            "mailto:cncf-wg-serverless@lists.cncf.io",
            ParseResult(
                scheme="mailto",
                netloc="",
                path="cncf-wg-serverless@lists.cncf.io",
                params="",
                query="",
                fragment="",
            ),
        ),
        (
            "urn:uuid:6e8bc430-9c3a-11d9-9669-0800200c9a66",
            ParseResult(
                scheme="urn",
                netloc="",
                path="uuid:6e8bc430-9c3a-11d9-9669-0800200c9a66",
                params="",
                query="",
                fragment="",
            ),
        ),
    ),
)
def test_validation_success_with_valid_uri(valid_uri, parsed_uri):
    class UriModel(BaseModel):
        value: URI

    m = UriModel(value=valid_uri)
    assert m.value == parsed_uri


@pytest.mark.parametrize(
    ["valid_uri"],
    (
        ("https://github.com/cloudevents",),
        ("mailto:cncf-wg-serverless@lists.cncf.io",),
        ("urn:uuid:6e8bc430-9c3a-11d9-9669-0800200c9a66",),
    ),
)
def test_serialization(valid_uri):
    class UriModel(BaseModel):
        value: URI

    m = UriModel(value=valid_uri)
    assert m.model_dump() == {"value": valid_uri}
    assert m.model_dump_json() == '{"value":"' + valid_uri + '"}'
    assert isinstance(m.model_dump()["value"], str)
