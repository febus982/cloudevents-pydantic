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

from cloudevents_pydantic.events.fields.types import Boolean


@pytest.mark.parametrize(
    ["input", "serialized_output"],
    (
        (True, "true"),
        ("true", "true"),
        (False, "false"),
        ("false", "false"),
    ),
)
def test_bool_serialization(input, serialized_output):
    class BoolModel(BaseModel):
        value: Boolean

    m = BoolModel(value=input)

    assert m.model_dump() == {"value": serialized_output}
    assert m.model_dump_json() == '{"value":"' + serialized_output + '"}'
    assert isinstance(m.model_dump()["value"], str)


@pytest.mark.parametrize(
    ["input", "validated_input"],
    (
        ("true", True),
        (True, True),
        ("false", False),
        (False, False),
    ),
)
def test_bool_validation(input, validated_input):
    class BoolModel(BaseModel):
        value: Boolean

    assert isinstance(BoolModel(value=input).value, bool)
    assert BoolModel(value=input).value is validated_input


@pytest.mark.parametrize(
    ["input"],
    (
        (1,),
        ("1",),
        ("True",),
        ("non_boolean",),
    ),
)
def test_bool_validation_fails_with_invalid_input(input):
    class BoolModel(BaseModel):
        value: Boolean

    with pytest.raises(ValidationError):
        BoolModel(value=input)
