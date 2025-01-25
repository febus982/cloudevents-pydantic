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

from cloudevents_pydantic.events.fields.types import Integer


def test_integer_validation_behaves_as_signed_32bit():
    class IntModel(BaseModel):
        value: Integer

    with pytest.raises(ValidationError):
        IntModel(value=2147483649)
    with pytest.raises(ValidationError):
        IntModel(value=-2147483649)

    assert IntModel(value=2312534).value == 2312534
    assert IntModel(value=-2312534).value == -2312534


def test_integer_serialization():
    class IntModel(BaseModel):
        value: Integer

    m = IntModel(value=2312534)
    assert m.model_dump() == {"value": 2312534}
    assert m.model_dump_json() == '{"value":2312534}'
    assert isinstance(m.model_dump()["value"], int)

    m2 = IntModel(value=-2312534)
    assert m2.model_dump() == {"value": -2312534}
    assert m2.model_dump_json() == '{"value":-2312534}'
    assert isinstance(m2.model_dump()["value"], int)
