from typing import Optional, TypeVar, Generic
from pydantic.generics import GenericModel
from humps import camelize
from pydantic import BaseModel

T = TypeVar("T")


def to_camel(string):
    return camelize(string)


class ResponseSchemaBase(BaseModel):
    __abstract__ = True

    code: str = ''
    message: str = ''

    def custom_response(self, code: str, message: str):
        self.code = code
        self.message = message
        return self

    def success_response(self):
        self.code = '000'
        self.message = 'Thành công'
        return self


class DataResponse(ResponseSchemaBase, GenericModel, Generic[T]):
    data: Optional[T] = None

    class Config:
        arbitrary_types_allowed = True

    def custom_response(self, code: str, message: str, data: T):
        self.code = code
        self.message = message
        self.data = data
        return self

    def success_response(self, data: T):
        self.code = '000'
        self.message = 'Thành công'
        self.data = data
        return self


class MappingByFieldName(BaseModel):
    class Config:
        orm_mode = True
        alias_generator = to_camel
        allow_population_by_field_name = True
        use_enum_values = True


class MetadataSchema(BaseModel):
    current_page: int
    page_size: int
    total_items: int
