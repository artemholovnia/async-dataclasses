import dataclasses
from typing import Generic, TypeVar

T = TypeVar("T")


class Field(dataclasses.Field, Generic[T]):
    """
        TODO: docstring
        TODO: можливість додавати синхронні методи в якості обробників
    """

    __slots__ = (
        *dataclasses.Field.__slots__,
        "resolvers",
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.resolvers = []

    def resolver(self, aw):
        self.resolvers.append(aw)


def field(*args, **kwargs) -> Field:
    original_field_cls = dataclasses.Field
    try:
        dataclasses.Field = Field
        return dataclasses.field(*args, **kwargs)
    finally:
        dataclasses.Field = original_field_cls
