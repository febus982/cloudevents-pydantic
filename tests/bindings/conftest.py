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
from unittest.mock import patch

import pytest

from cloudevents_pydantic.formats import canonical, json


@pytest.fixture
def json_serialize_spy():
    f = json.serialize
    with patch(
        "cloudevents_pydantic.formats.json.serialize", wraps=f
    ) as mocked_function:
        yield mocked_function


@pytest.fixture
def json_serialize_batch_spy():
    f = json.serialize_batch
    with patch(
        "cloudevents_pydantic.formats.json.serialize_batch", wraps=f
    ) as mocked_function:
        yield mocked_function


@pytest.fixture
def json_deserialize_spy():
    f = json.deserialize
    with patch(
        "cloudevents_pydantic.formats.json.deserialize", wraps=f
    ) as mocked_function:
        yield mocked_function


@pytest.fixture
def json_deserialize_batch_spy():
    f = json.deserialize_batch
    with patch(
        "cloudevents_pydantic.formats.json.deserialize_batch", wraps=f
    ) as mocked_function:
        yield mocked_function


@pytest.fixture
def canonical_serialize_spy():
    f = canonical.serialize
    with patch(
        "cloudevents_pydantic.formats.canonical.serialize", wraps=f
    ) as mocked_function:
        yield mocked_function


@pytest.fixture
def canonical_serialize_batch_spy():
    f = canonical.serialize_batch
    with patch(
        "cloudevents_pydantic.formats.canonical.serialize_batch", wraps=f
    ) as mocked_function:
        yield mocked_function


@pytest.fixture
def canonical_deserialize_spy():
    f = canonical.deserialize
    with patch(
        "cloudevents_pydantic.formats.canonical.deserialize", wraps=f
    ) as mocked_function:
        yield mocked_function


@pytest.fixture
def canonical_deserialize_batch_spy():
    f = canonical.deserialize_batch
    with patch(
        "cloudevents_pydantic.formats.canonical.deserialize_batch", wraps=f
    ) as mocked_function:
        yield mocked_function
