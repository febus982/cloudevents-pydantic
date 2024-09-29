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
from typing import Annotated, Any, Optional

from pydantic import Field

from ._attributes_field_metadata import (
    FieldData,
    FieldDataContentType,
    FieldDataSchema,
    FieldSource,
    FieldSpecVersion,
    FieldSubject,
    FieldTime,
    FieldTitle,
    FieldType,
)
from .field_types import URI, DateTime, SpecVersion, String, URIReference

DataAnnotation = Annotated[Any, Field(default=None), FieldData]
SourceAnnotation = Annotated[URIReference, FieldSource]
IdAnnotation = Annotated[String, FieldTitle]
TypeAnnotation = Annotated[String, FieldType]
SpecVersionAnnotation = Annotated[SpecVersion, FieldSpecVersion]
TimeAnnotation = Annotated[Optional[DateTime], Field(default=None), FieldTime]
SubjectAnnotation = Annotated[Optional[String], Field(default=None), FieldSubject]
DataContentTypeAnnotation = Annotated[
    Optional[String], Field(default=None), FieldDataContentType
]
DataSchemaAnnotation = Annotated[Optional[URI], Field(default=None), FieldDataSchema]
