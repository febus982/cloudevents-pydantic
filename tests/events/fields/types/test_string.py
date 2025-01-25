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

from cloudevents_pydantic.events.fields.types import String


def test_string_validation_allows_valid_unicode_chars():
    class StrModel(BaseModel):
        value: String

    # Testing from surrogates pairs is probably unnecessary
    str_from_surrogates = "test_\ud83e\udd26_string".encode(
        "utf-16", errors="surrogatepass"
    ).decode("utf-16", errors="surrogatepass")
    assert StrModel(value=str_from_surrogates).value == "test_🤦_string"
    assert StrModel(value="test_🤦_string").value == "test_🤦_string"
    assert StrModel(value="🤦_string").value == "🤦_string"
    assert StrModel(value="test_🤦").value == "test_🤦"


# https://github.com/cloudevents/spec/blob/v1.0.2/cloudevents/spec.md#type-system
@pytest.mark.parametrize(
    ["control_char"],
    list(map(chr, range(ord("\u0000"), ord("\u001f") + 1)))
    + list(map(chr, range(ord("\u007f"), ord("\u009f") + 1))),
)
def test_string_validation_fails_if_control_chars(control_char):
    class StrModel(BaseModel):
        value: String

    with pytest.raises(ValidationError):
        StrModel(value=control_char)
    with pytest.raises(ValidationError):
        StrModel(value="test_" + control_char)
    with pytest.raises(ValidationError):
        StrModel(value=control_char + "_string")


# https://github.com/cloudevents/spec/blob/v1.0.2/cloudevents/spec.md#type-system
@pytest.mark.parametrize(
    ["malformed_surrogate"],
    [
        *list(map(chr, range(ord("\ud800"), ord("\udbff") + 1))),
        *list(map(chr, range(ord("\udc00"), ord("\udfff") + 1))),
    ],
)
def test_string_validation_fails_if_malformed_surrogates(malformed_surrogate):
    class StrModel(BaseModel):
        value: String

    with pytest.raises(ValidationError):
        StrModel(value="test_" + malformed_surrogate + "_string")
    with pytest.raises(ValidationError):
        StrModel(value=malformed_surrogate + "_string")
    with pytest.raises(ValidationError):
        StrModel(value="test_" + malformed_surrogate)


# https://www.unicode.org/faq/private_use.html#noncharacters
@pytest.mark.parametrize(
    ["unicode_noncharacter"],
    [
        *list(map(chr, range(ord("\ufdd0"), ord("\ufdef") + 1))),
        "\ufffe",
        "\uffff",
        # These are to be enabled when AsyncAPI regex issue is fixed
        # https://github.com/asyncapi/asyncapi-react/issues/1071
        # "\U0001fffe",
        # "\U0001ffff",
        # "\U0002fffe",
        # "\U0002ffff",
        # "\U0003fffe",
        # "\U0003ffff",
        # "\U0004fffe",
        # "\U0004ffff",
        # "\U0005fffe",
        # "\U0005ffff",
        # "\U0006fffe",
        # "\U0006ffff",
        # "\U0007fffe",
        # "\U0007ffff",
        # "\U0008fffe",
        # "\U0008ffff",
        # "\U0009fffe",
        # "\U0009ffff",
        # "\U000afffe",
        # "\U000affff",
        # "\U000bfffe",
        # "\U000bffff",
        # "\U000cfffe",
        # "\U000cffff",
        # "\U000dfffe",
        # "\U000dffff",
        # "\U000efffe",
        # "\U000effff",
        # "\U000ffffe",
        # "\U000fffff",
        # "\U0010fffe",
        # "\U0010ffff",
    ],
)
def test_string_validation_fails_on_unicode_noncharacters(unicode_noncharacter):
    class StrModel(BaseModel):
        value: String

    with pytest.raises(ValidationError):
        StrModel(value="test_" + unicode_noncharacter + "_string")
